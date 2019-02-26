import os
from sort import big_data_sorter, config


def is_big_data(filenames):
    total_size = 0
    for file in filenames:
        total_size += os.path.getsize(file)
        if total_size > config.OPERATIVE_MEMORY_SIZE:
            return True
    return False


def read_files(filenames):
    lines = []
    for file in filenames:
        with open(file, 'r') as f:
            for line in f.readlines():
                lines.append(line)
    return lines


def sort(filenames):
    if filenames and not is_big_data(filenames):
        lines = read_files(filenames)
        lines.sort()
        for line in lines:
            print(line,end='')  # pragma: no cover
    else:
        sorter = big_data_sorter.Big_Data_Sorter(filenames)
        sorter.sort()
        sorter.print_res()
