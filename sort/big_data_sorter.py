import sys
import heapq
import tempfile
from sort import config


class Big_Data_Sorter():
    def __init__(self, filenames):
        self.filenames = filenames
        self.tmp_files = []
        self.result_file = ''
        self.already_merged = 0

    def sort(self):
        if self.filenames:
            self.process_files()
        elif not sys.stdin.isatty():
            self.process_data(sys.stdin.readlines())
        self.merge_tmp_files()

    def process_files(self):
        for filename in self.filenames:
            with open(filename, 'r') as file:
                self.process_data(file)

    def process_data(self, data):
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

    def process_tmp_file(self, text):
        tmp_file = tempfile.TemporaryFile(mode='w+')
        self.tmp_files.append(tmp_file)
        tmp_text = self.sort_text(text)
        tmp_file.write(tmp_text)

    def sort_text(self, text):
        tmp_text = text.split('\n')
        tmp_text.sort()
        return '\n'.join(tmp_text)

    def merge_tmp_files(self):
        if len(self.tmp_files) == 1:
            self.result_file = self.tmp_files[0]
        else:
            while len(self.tmp_files) - self.already_merged > 1:
                count_of_merging = min(config.MERGE_FILES_COUNT, len(self.tmp_files) - self.already_merged)
                self.merge_part_of_tmp_files(count_of_merging)
                self.already_merged += count_of_merging

    def merge_part_of_tmp_files(self, count):
        result_file = tempfile.TemporaryFile(mode='w+')
        self.tmp_files.append(result_file)

        files = []

        for i in range(count):
            self.tmp_files[self.already_merged + i].seek(0, 0)
            tmp = list(
                reversed([line.replace('\n', '') for line in self.tmp_files[self.already_merged + i].readlines()]))

            self.tmp_files[self.already_merged + i].seek(0, 0)
            tmp.sort()
            files.append(tmp)
        result = heapq.merge(*files)
        for line in result:
            result_file.write(line)
            result_file.write('\n')
        self.result_file = result_file

    def make_result_file(self):  # pragma: no cover
        input_file = tempfile.NamedTemporaryFile()
        for line in self.result_file:
            input_file.write(line)
        self.result_file = input_file

    def print_res(self):  # pragma: no cover
        self.result_file.seek(0, 0)
        for line in self.result_file.readlines():
            print(line.replace('\n', ''))
