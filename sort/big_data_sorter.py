import heapq
import os
import sys
import tempfile
from sort import config


class Big_Data_Sorter():
    def __init__(self, filenames):
        self.filenames = filenames
        self.tmp_files_count = 0
        self.tmp_file_names = []
        self.start_dir = os.getcwd()
        self.tmp_dir = tempfile.mkdtemp()
        self.result_file = ''
        self.already_merged = 0

    def sort(self):
        if self.filenames:
            self.process_files()
        elif not sys.stdin.isatty():
            self.process_data(sys.stdin.readlines())
        self.merge_tmp_files()
        self.delete_tmp_dir()

    def process_files(self):
        for filename in self.filenames:
            with open(filename, 'r') as file:
                self.process_data(file)

    def process_data(self, data):
        os.chdir(self.tmp_dir)
        current_lines, tmp_text = 0, ''
        for line in data:
            line = line.rstrip().replace('"', '').split('\\n')
            for i in line:
                if current_lines != 0:
                    tmp_text += "\n"
                current_lines += 1
                tmp_text += i

            if current_lines == config.MAX_LINES_COUNT:
                self.process_tmp_file(tmp_text)
                current_lines, tmp_text = 0, ''
        if tmp_text != '':
            self.process_tmp_file(tmp_text)
        os.chdir(self.start_dir)

    def process_tmp_file(self, text):
        with open(str(self.tmp_files_count) + ".txt", 'w') as tmp_file:
            self.tmp_files_count += 1
            self.tmp_file_names.append(tmp_file.name)
            tmp_text = self.sort_text(text)
            tmp_file.write(tmp_text)

    def sort_text(self, text):
        tmp_text = text.split('\n')
        tmp_text.sort()
        return '\n'.join(tmp_text)

    def merge_tmp_files(self):
        if len(self.tmp_file_names) == 1:
            self.result_file = self.tmp_file_names[0]
        else:
            os.chdir(self.tmp_dir)
            while len(self.tmp_file_names) - self.already_merged > 1:
                count_of_merging = min(config.MERGE_FILES_COUNT, len(self.tmp_file_names) - self.already_merged)
                self.merge_part_of_tmp_files(count_of_merging)
                self.already_merged += count_of_merging
            os.chdir(self.start_dir)

    def merge_part_of_tmp_files(self, count):
        result_file = open(str(self.tmp_files_count) + ".txt", 'w')
        self.tmp_file_names.append(result_file.name)
        self.tmp_files_count += 1

        files = []

        for i in range(count):
            with open(self.tmp_file_names[self.already_merged + i], 'r') as f:
                tmp = list(reversed([line.replace('\n', '') for line in f.readlines()]))
                tmp.sort()
                files.append(tmp)
        result = heapq.merge(*files)
        for line in result:
            result_file.write(line)
            result_file.write('\n')
        self.result_file = result_file.name
        result_file.close()

    def delete_tmp_dir(self):  # pragma: no cover
        self.make_result_file()
        for i in self.tmp_file_names:
            path = os.path.join(self.tmp_dir, i)
            os.remove(path)
        os.rmdir(self.tmp_dir)

    def make_result_file(self):  # pragma: no cover
        os.chdir(self.tmp_dir)
        with open(self.result_file, 'r') as result_file:
            os.chdir(self.start_dir)
            with open(config.RESULT_FILE_NAME, 'w') as input_file:
                for line in result_file:
                    input_file.write(line)
        self.result_file = config.RESULT_FILE_NAME

    def print_res(self):  # pragma: no cover
        with open(self.result_file, 'r') as file:
            for line in file.readlines():
                print(line.replace('\n', ''))
        os.remove(self.result_file)
