import os

import pytest

from sort import big_data_sorter


@pytest.fixture()
def sorter_one_file():
    return big_data_sorter.Big_Data_Sorter(('./test_files/1.txt',))


@pytest.fixture()
def sorter_many_files():
    return big_data_sorter.Big_Data_Sorter(('./test_files/1.txt', './test_files/2.txt'))


@pytest.fixture()
def sorter_big_file():
    return big_data_sorter.Big_Data_Sorter(('./test_files/100000.txt',))


@pytest.fixture()
def result_one_file(sorter_one_file):
    yield '0\n1\n10\n2\n3\n4\n5\n6\n7\n8\n9'
    # os.remove(sorter_one_file.result_file)


@pytest.fixture()
def result_many_files(sorter_many_files):
    yield '0\n1\n10\n2\n3\n4\n5\n6\n7\n8\n9\nananas\ncourse\ntask\ntest\nvideo\n'
    # os.remove(sorter_many_files.result_file)


# @pytest.fixture()
# def clean_files(sorter_big_file):
#     yield
#     try:
#         os.remove(sorter_big_file.result_file)
#     except FileNotFoundError:
#         pass
#     for file in sorter_big_file.tmp_files:
#         try:
#             os.remove(file)
#             os.remove(sorter_big_file.result_file)
#         except FileNotFoundError:
#             pass
