import argparse
from collections import Counter


def read_file(file_name):
    with open(file_name, 'r', encoding='utf8') as fh:
        number_pairs = [line.strip().split() for line in fh.readlines()]
    left = sorted([int(pair[0]) for pair in number_pairs])
    right = sorted([int(pair[1]) for pair in number_pairs])
    return left, right


def total_distance(left, right):
    total = 0
    for left_num, right_num in zip(left, right):
        total += abs(left_num - right_num)
    return total


def similarity_score(left, right):
    total = 0
    right_counts = Counter(right)
    for num in left:
        total += num * right_counts[num]
    return total


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        type=str,
        help='Input file')
    parser.add_argument(
        '--part',
        type=int,
        help='Task part (1 or 2)')

    args = parser.parse_args()
    left_list, right_list = read_file(args.input)
    if args.part == 1:
        print(total_distance(left_list, right_list))
    elif args.part == 2:
        print(similarity_score(left_list, right_list))
