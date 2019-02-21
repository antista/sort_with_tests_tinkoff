import argparse

from sort import sorter


def get_args():
    parser = argparse.ArgumentParser(
        description='Sort lines in files or from stdin.')
    parser.add_argument('filenames', nargs='*', help='files for sorting')
    return parser.parse_args()


def main():
    filenames = get_args().filenames
    sorter.sort(filenames)
