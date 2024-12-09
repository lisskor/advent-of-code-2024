from argument_parser import make_parser


def read_file(file_name: str) -> tuple[list[tuple[int, ...]], list[list[int]]]:
    rules, updates = [], []
    reading_rules = 1
    with open(file_name, 'r', encoding='utf8') as fh:
        for line in fh.readlines():
            if reading_rules:
                if not line.strip():
                    reading_rules = 0
                    continue
                rules.append((int(line.strip().split("|")[0]), int(line.strip().split("|")[1])))
            else:
                updates.append([int(num) for num in line.strip().split(",")])
    return rules, updates


class SafetyManual:
    def __init__(self, rules: list[tuple[int, int]]):
        self.pages = dict()
        self.add_page_rules(rules)

    def add_page_rules(self, rules: list[tuple[int, int]]):
        for rule in rules:
            from_node, to_node = rule
            self.pages.setdefault(from_node, [])
            self.pages.setdefault(to_node, [])
            self.pages[from_node].append(to_node)

    def order_correct(self, update: list[int]) -> bool:
        for i in range(len(update) - 1):
            if update[i+1] in self.pages[update[i]]:
                continue
            else:
                return False
        return True


def part1(rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    manual = SafetyManual(rules)
    total = 0

    for update in updates:
        if manual.order_correct(update):
            total += update[len(update)//2]
    return total


def part2(rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    manual = SafetyManual(rules)
    total = 0

    for update in updates:
        if not manual.order_correct(update):
            while not manual.order_correct(update):
                for i in range(len(update)-1):
                    if update[i] in manual.pages[update[i+1]]:
                        update[i], update[i+1] = update[i+1], update[i]
            total += update[len(update)//2]

    return total


if __name__ == '__main__':
    args = make_parser().parse_args()
    input_rules, input_updates = read_file(args.input)
    if args.part == 1:
        print(part1(input_rules, input_updates))
    elif args.part == 2:
        print(part2(input_rules, input_updates))
