import numpy as np

from argument_parser import make_parser


def read_file(file_name: str) -> np.ndarray:
    with open(file_name, 'r', encoding='utf8') as fh:
        lines = [[num for num in line.strip()] for line in fh.readlines()]
    number_lines = [[int(num) for num in line] for line in lines]
    return np.array(number_lines)


class Map:
    def __init__(self, input_array: np.ndarray):
        self.elevation_map = input_array
        self.height, self.width = self.elevation_map.shape

    def valid_next(self, start_row: int, start_col: int) -> list[tuple[int, int]]:
        valid_neighbours = []
        for neighbour_row, neighbour_col in [
            [start_row, start_col-1], [start_row, start_col+1], [start_row-1, start_col], [start_row+1, start_col]
        ]:
            if -1 < neighbour_row < self.height and -1 < neighbour_col < self.width:
                if self.elevation_map[neighbour_row, neighbour_col] == self.elevation_map[start_row, start_col] + 1:
                    valid_neighbours.append((neighbour_row, neighbour_col))
        return valid_neighbours

    def bfs(self, start_row: int, start_col: int, goal: int=9) -> list[tuple[int, int]]:
        reachable_nines = []
        q = [(start_row, start_col)]
        explored = [(start_row, start_col)]
        while q:
            v = q.pop(0)
            if self.elevation_map[v[0], v[1]] == goal:
                reachable_nines.append(v)
            for neighbour in self.valid_next(v[0], v[1]):
                if neighbour not in explored:
                    explored.append(neighbour)
                    q.append(neighbour)
        return reachable_nines

    def find_all_routes(self, start_row: int, start_col: int, end_row: int, end_col: int) -> int:
        routes = 0
        q = [(start_row, start_col)]
        while q:
            v = q.pop(0)
            if v[0] == end_row and v[1] == end_col:
                routes += 1
            for neighbour in self.valid_next(v[0], v[1]):
                q.append(neighbour)
        return routes

    def trailhead_score(self) -> int:
        # find all possible trailheads (zeros)
        trailheads = np.argwhere(self.elevation_map == 0)
        return sum([len(self.bfs(trailhead[0], trailhead[1])) for trailhead in trailheads])

    def trailhead_rating(self) -> int:
        # find all possible trailheads (zeros)
        trailheads = np.argwhere(self.elevation_map == 0)
        # sum up number of paths to each reachable 9
        return sum(
            [sum([self.find_all_routes(trailhead[0], trailhead[1], end[0], end[1])
                  for end in self.bfs(trailhead[0], trailhead[1])])
             for trailhead in trailheads]
        )


if __name__ == '__main__':
    args = make_parser().parse_args()
    my_map = Map(read_file(args.input))
    if args.part == 1:
        print(my_map.trailhead_score())
    elif args.part == 2:
        print(my_map.trailhead_rating())
