import pytest
from sort import big_data_sorter


def test_sort_text(sorter_one_file, result_one_file):
    sorter_one_file.sort()
    sorter_one_file.result_file.seek(0, 0)
    assert ''.join(sorter_one_file.result_file.readlines()) == result_one_file


def test_sort_more_text(sorter_many_files, result_many_files):
    sorter_many_files.sort()
    sorter_many_files.result_file.seek(0, 0)
    assert ''.join(sorter_many_files.result_file.readlines()) == result_many_files


def test_sort_big_text(sorter_big_file):
    sorter_big_file.sort()
    sorter_big_file.result_file.seek(0, 0)
    assert sorter_big_file.result_file.read(5) == "'sbod"


def test_process_file(sorter_one_file, mocker):
    mocker.patch('builtins.open')
    mocker.patch('sort.big_data_sorter.Big_Data_Sorter.process_data')
    sorter_one_file.process_files()
    big_data_sorter.Big_Data_Sorter.process_data.assert_called_once()


def test_process_files(sorter_many_files, mocker):
    mocker.patch('builtins.open')
    mocker.patch('sort.big_data_sorter.Big_Data_Sorter.process_data')
    sorter_many_files.process_files()
    big_data_sorter.Big_Data_Sorter.process_data.assert_called()


def test_process_data(sorter_one_file, mocker):
    mocker.patch('sort.big_data_sorter.Big_Data_Sorter.process_tmp_file')
    sorter_one_file.process_data('smth')
    big_data_sorter.Big_Data_Sorter.process_tmp_file.assert_called_once()


def test_process_big_data(sorter_big_file, mocker):
    mocker.patch('sort.big_data_sorter.Big_Data_Sorter.process_tmp_file')
    sorter_big_file.process_files()
    big_data_sorter.Big_Data_Sorter.process_tmp_file.assert_called()


def test_process_tmp_file(sorter_one_file, mocker):
    mocker.patch('builtins.open')
    mocker.patch('tempfile.TemporaryFile')
    mocker.patch('sort.big_data_sorter.Big_Data_Sorter.sort_text')
    sorter_one_file.process_tmp_file('smth')
    big_data_sorter.Big_Data_Sorter.sort_text.assert_called_once()


def test_merge_tmp_files(sorter_one_file, mocker):
    mocker.patch('sort.big_data_sorter.Big_Data_Sorter.merge_part_of_tmp_files')
    sorter_one_file.process_files()
    sorter_one_file.merge_tmp_files()
    assert len(sorter_one_file.tmp_files) == 1
    big_data_sorter.Big_Data_Sorter.merge_part_of_tmp_files.assert_not_called()


def test_merge_many_tmp_files(sorter_big_file, mocker):
    mocker.patch('sort.big_data_sorter.Big_Data_Sorter.merge_part_of_tmp_files')
    sorter_big_file.process_files()
    sorter_big_file.merge_tmp_files()
    assert len(sorter_big_file.tmp_files) != 1
    big_data_sorter.Big_Data_Sorter.merge_part_of_tmp_files.assert_called()
