import os

import pytest
from sort import sorter, big_data_sorter, config


@pytest.mark.parametrize('filenames',
                         [['./test_files/1.txt'],
                          ['./test_files/2.txt'],
                          ['./test_files/1.txt', './test_files/2.txt'],
                          ['./test_files/10000.txt'],
                          ['./test_files/million.txt']])
def test_is_not_big_data(filenames):
    assert not sorter.is_big_data(filenames)


@pytest.mark.parametrize('filenames',
                         [['./test_files/million.txt', './test_files/million.txt',
                           './test_files/million.txt', './test_files/million.txt',
                           './test_files/million.txt', './test_files/million.txt',
                           './test_files/million.txt', './test_files/million.txt']])
def test_is_big_data_file(filenames):
    assert sorter.is_big_data(filenames)


def test_is_big_data(mocker):
    mocker.patch('os.path.getsize', return_value=config.OPERATIVE_MEMORY_SIZE + 20)
    assert sorter.is_big_data('..')


@pytest.mark.parametrize(('filenames', 'lines_len'),
                         [[('./test_files/1.txt',), 11],
                          [('./test_files/2.txt',), 5],
                          [('./test_files/1.txt', 'test_files/2.txt'), 16],
                          [('./test_files/10000.txt',), 10000],
                          [('./test_files/million.txt',), 1000000]])
def test_read_files(filenames, lines_len):
    assert len(sorter.read_files(filenames)) == lines_len


@pytest.mark.parametrize('filenames',
                         [['./test_files/1.txt'],
                          ['./test_files/2.txt'],
                          ['./test_files/1.txt', './test_files/2.txt'],
                          ['./test_files/10000.txt'],
                          ['./test_files/million.txt']])
def test_small_sort(mocker, filenames):
    mocker.patch('sort.sorter.read_files')
    sorter.sort(filenames)
    sorter.read_files.assert_called_once_with(filenames)


@pytest.mark.parametrize('filenames',
                         [['./test_files/million.txt', './test_files/million.txt',
                           './test_files/million.txt', './test_files/million.txt',
                           './test_files/million.txt', './test_files/million.txt',
                           './test_files/million.txt', './test_files/million.txt']])
def test_big_sort(mocker, filenames):
    mocker.patch('sort.big_data_sorter.Big_Data_Sorter.sort')
    mocker.patch('sort.big_data_sorter.Big_Data_Sorter.print_res')
    sorter.sort(filenames)
    big_data_sorter.Big_Data_Sorter.sort.assert_called_once_with()


def test_stdin(mocker, data=('4\n7\n1\n0',)):
    mocker.patch('os.chdir')
    mocker.patch('builtins.open')
    mocker.patch('sys.stdin.readlines', return_value=data)
    mocker.patch('sort.big_data_sorter.Big_Data_Sorter.sort_text')
    mocker.patch('sort.big_data_sorter.Big_Data_Sorter.merge_tmp_files')
    mocker.patch('sort.big_data_sorter.Big_Data_Sorter.print_res')
    mocker.patch('tempfile.TemporaryFile')
    sorter.sort([])
    big_data_sorter.Big_Data_Sorter.sort_text.assert_called_once_with(data[0])
