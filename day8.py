from itertools import combinations

from argument_parser import make_parser


def read_file(file_name: str) -> list[list[str]]:
    with open(file_name, 'r', encoding='utf8') as fh:
        lines = [[char for char in line.strip()] for line in fh.readlines()]
    return lines


class AntennaMap:
    def __init__(self, input_list: list[list[str]], part: int=1):
        self.antennas = self.save_antennas(input_list)
        self.height = len(input_list)
        self.width = len(input_list[0])
        self.part = part
        self.antinodes = self.add_antinodes()

    @staticmethod
    def save_antennas(input_list: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
        result = dict()
        for row, line in enumerate(input_list):
            for col, char in enumerate(line):
                if char != ".":
                    result.setdefault(char, [])
                    result[char].append((row, col))
        return result

    def add_antinodes(self) -> dict[str, list[tuple[int, int]]]:
        antinodes = dict()
        steps = 2 if self.part == 1 else max(self.width, self.height)

        for node_type in self.antennas:
            antinodes[node_type] = []
            pairs = combinations(self.antennas[node_type], 2)
            for node_one, node_two in pairs:
                row_diff = node_one[0] - node_two[0]
                col_diff = node_one[1] - node_two[1]
                for sign in [1, -1]:
                    for step in range(steps):
                        for node in [node_one, node_two]:
                            antinode = (node[0] + step * sign * row_diff, node[1] + step * sign * col_diff)
                            if (
                                    antinode != node_one and antinode != node_two and
                                    -1 < antinode[0] < self.height and -1 < antinode[1] < self.width and
                                    antinode not in antinodes[node_type]
                            ):
                                antinodes[node_type].append(antinode)
        return antinodes


    def unique_antinode_locations(self) -> int:
        all_antinodes = []
        for antinode_type in self.antinodes:
            all_antinodes.extend(self.antinodes[antinode_type])
            if self.part == 2:
                all_antinodes.extend(self.antennas[antinode_type])
        return len(set(all_antinodes))


if __name__ == '__main__':
    args = make_parser().parse_args()
    my_map = AntennaMap(read_file(args.input), args.part)
    my_map.add_antinodes()
    print(my_map.unique_antinode_locations())
