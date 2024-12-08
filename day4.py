import numpy as np

from argument_parser import make_parser


def read_file(file_name: str) -> np.ndarray:
    with open(file_name, 'r', encoding='utf8') as fh:
        lines = [[char for char in line.strip()] for line in fh.readlines()]
    # replace letters with numbers
    letter_to_number = {"X": 1, "M": 2, "A": 3, "S": 4}
    number_lines = [[letter_to_number[char] for char in line] for line in lines]
    return np.array(number_lines)


class XMasMatrix:
    def __init__(self, array: np.ndarray):
        self.array = array
        self.height, self.width = self.array.shape
        self.start_points = np.transpose(np.where(self.array == 1))
        self.center_points = np.transpose(np.where(self.array == 3))

    def words_from_start_new(self, coordinates: tuple[int, int]) -> int:
        row, col = coordinates

        words = [
            self.array[row,col-3:col+1][::-1],                             # left
            self.array[row - 3:row + 1, col - 3:col + 1].diagonal()[::-1], # left + up
            np.rot90(self.array[row:row + 4, col - 3:col + 1]).diagonal(), # left + down
            self.array[row, col:col + 4],                                  # right
            np.rot90(self.array[row-3:row+1,col:col+4]).diagonal()[::-1],  # right + up
            self.array[row:row+4,col:col+4].diagonal(),                    # right + down
            self.array[row - 3:row + 1, col][::-1],                        # up
            self.array[row:row + 4, col]                                   # down
        ]

        return len(
            [word for word in words if word.shape == (4,) and np.allclose(word, np.array([1, 2, 3, 4]))]
        )

    def center_possible(self, coordinates: tuple[int, int]) -> bool:
        if 0 < coordinates[0] < self.height - 1 and 0 < coordinates[1] < self.width - 1:
            return True
        return False

    def count_xmas_part1(self):
        return sum([self.words_from_start_new(start_point) for start_point in self.start_points])

    def count_xmas_part2(self) -> int:
        total = 0
        for center_point in self.center_points:
            if self.center_possible(center_point):
                row, col = center_point
                main_diagonal = [self.array[row-1,col-1].item(), self.array[row+1,col+1].item()]
                secondary_diagonal = [self.array[row-1,col+1].item(), self.array[row+1,col-1].item()]
                if set(main_diagonal) == set(secondary_diagonal) == {2, 4}:
                    total += 1
        return total


if __name__ == '__main__':
    args = make_parser().parse_args()
    matrix = XMasMatrix(read_file(args.input))
    if args.part == 1:
        print(matrix.count_xmas_part1())
    elif args.part == 2:
        print(matrix.count_xmas_part2())
