from typing import Iterator

from common import Day, line_iterator, Grid, Vector, DIRECTIONS_ALL, Direction


class Day4(Day):
    @staticmethod
    def parse_input(input_str: str) -> Grid:
        grid = Grid()
        for line in line_iterator(input_str):
            grid.add_line(line)
        return grid

    @staticmethod
    def iter_starting_points(grid: Grid, letter: str) -> Iterator[Vector]:
        for pos, l in grid.scan_all():
            if l == letter:
                yield pos

    def solve_part1(self, input_str: str) -> str:
        grid = self.parse_input(input_str)
        xmas = 'XMAS'
        xmas_l = len(xmas)
        count = 0
        for start_pos in self.iter_starting_points(grid, 'X'):
            for d in DIRECTIONS_ALL:
                p = start_pos + d
                i = 1
                while grid.is_in_bounds(p) and grid.get_cell(p) == xmas[i]:
                    i += 1
                    if i >= xmas_l:
                        count += 1
                        break
                    p += d
        return str(count)

    @staticmethod
    def is_cell(grid: Grid, pos: Vector, test_val: str) -> bool:
        return grid.is_in_bounds(pos) and grid.get_cell(pos) == test_val

    def solve_part2(self, input_str: str) -> str:
        grid = self.parse_input(input_str)
        d_pairs = [(Direction.UpLeft, Direction.DownRight), (Direction.DownLeft, Direction.UpRight)]
        count = 0
        for start_pos in self.iter_starting_points(grid, 'A'):
            match = True
            for dp in d_pairs:
                if not ((Day4.is_cell(grid, start_pos + dp[0], 'M') and
                         Day4.is_cell(grid, start_pos + dp[1], 'S')) or
                        (Day4.is_cell(grid, start_pos + dp[1], 'M') and
                         Day4.is_cell(grid, start_pos + dp[0], 'S'))):
                    match = False
                    break
            if match:
                count += 1
        return str(count)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=4, part=1, s_class=Day4, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=4, part=2, s_class=Day4, path_prefix='..', input_file='example_input.txt')
