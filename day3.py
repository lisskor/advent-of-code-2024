import re

from argument_parser import make_parser


def read_file(file_name):
    with open(file_name, 'r', encoding='utf8') as fh:
        lines = [line.strip() for line in fh.readlines()]
    return lines


def multiply(line):
    matches = [m for m in re.findall(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)", line)]
    return sum([int(match[0]) * int(match[1]) for match in matches])


def part_1(lines):
    return sum([multiply(line) for line in lines])


def part_2(lines):
    total = 0
    enabled = True
    for line in lines:
        to_process = line
        while to_process:
            if enabled:
                disabled_start = to_process.find("don't()")
                if disabled_start == -1:
                    total += multiply(to_process)
                    break
                else:
                    total += multiply(to_process[:disabled_start+7])
                    to_process = to_process[disabled_start+7:]
                    enabled = False
            if not enabled:
                disabled_end = to_process.find("do()")
                if disabled_end == -1:
                    break
                else:
                    to_process = to_process[disabled_end+4:]
                    enabled = True
    return total


if __name__ == '__main__':
    args = make_parser().parse_args()
    input_lines = read_file(args.input)
    if args.part == 1:
        print(part_1(input_lines))
    elif args.part == 2:
        print(part_2(input_lines))
