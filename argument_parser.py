import argparse


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        type=str,
        help='Input file')
    parser.add_argument(
        '--part',
        type=int,
        help='Task part (1 or 2)')

    return parser
