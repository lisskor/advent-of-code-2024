from argument_parser import make_parser


def read_file(file_name: str) -> list[tuple[int, list[int]]]:
    output = []
    with open(file_name, 'r', encoding='utf8') as fh:
        for line in fh.readlines():
            result, equation = line.strip().split(":")
            result = int(result)
            equation = [int(num) for num in equation.strip().split(" ")]
            output.append((result, equation))
    return output


def valid_equations_sum(file_name: str, concat: bool=False) -> int:
    total = 0
    input_data = read_file(file_name)
    for result, equation in input_data:
        if try_equation(result, equation, concat):
            total += result
    return total


def try_equation(result: int, equation: list[int], concat: bool=False) -> bool:
    level_lists = [[] for _ in range(len(equation))]
    level = 0
    level_lists[0].append(equation[0])
    for next_num in equation[1:]:
        level += 1
        level_lists[level].extend([num + next_num for num in level_lists[level - 1]])
        level_lists[level].extend([num * next_num for num in level_lists[level - 1]])
        if concat:
            level_lists[level].extend([int(str(num) + str(next_num)) for num in level_lists[level - 1]])
    if result in level_lists[level]:
        return True
    else:
        return False


if __name__ == '__main__':
    args = make_parser().parse_args()
    if args.part == 1:
        print(valid_equations_sum(args.input, concat=False))
    elif args.part == 2:
        print(valid_equations_sum(args.input, concat=True))
