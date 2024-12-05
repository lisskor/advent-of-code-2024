import argparse


def read_file(file_name):
    with open(file_name, 'r', encoding='utf8') as fh:
        for line in fh:
            report = [int(num) for num in line.strip().split()]
            yield report


def report_is_safe(report: list[int]):
    diffs = [report[i + 1] - report[i] for i in range(len(report) - 1)]
    if max(diffs) > 3 or min(diffs) < -3 or 0 in diffs:
        return False
    if abs(sum(diffs)) != sum([abs(num) for num in diffs]):
        return False
    return True


def safe_reports_part1(file_name):
    return sum([report_is_safe(report) for report in read_file(file_name)])


def safe_reports_part2(file_name):
    total = 0
    for report in read_file(file_name):
        if report_is_safe(report):
            total += 1
            continue
        for i in range(len(report)):
            modified_report = report[:i] + report[i+1:]
            if report_is_safe(modified_report):
                total += 1
                break
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
    if args.part == 1:
        print(safe_reports_part1(args.input))
    elif args.part == 2:
        print(safe_reports_part2(args.input))
