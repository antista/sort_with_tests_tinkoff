import argparse  # pragma: no cover

from sort import sorter  # pragma: no cover


def get_args():  # pragma: no cover
    parser = argparse.ArgumentParser(
        description='Sort lines in files or from stdin.')
    parser.add_argument('filenames', nargs='*', help='files for sorting')
    return parser.parse_args()


def main():  # pragma: no cover
    filenames = get_args().filenames
    sorter.sort(filenames)
