import itertools
from collections import defaultdict
from collections.abc import Iterable, Callable

from common import Day, line_iterator, Grid, Vector


class Day8(Day):
    @staticmethod
    def parse_input(input_str: str) -> tuple[Grid[str], dict[str, list[Vector]]]:
        city: Grid[str] = Grid()
        # noinspection PyTypeChecker
        antennas: dict[str, list[Vector]] = defaultdict(list)
        for y, line in enumerate(line_iterator(input_str)):
            city.add_line(line)
            for x, c in enumerate(line):
                if c == '.':
                    continue
                if not c.isalnum():
                    raise RuntimeError('Invalid antenna character in the input')
                al = antennas[c]
                al.append(Vector(x, y))
        return city, antennas

    @staticmethod
    def find_antinodes_p1(a1: Vector, a2: Vector, bounds_grid: Grid) -> Iterable[Vector]:
        dv = Vector(a1.x - a2.x, a1.y - a2.y)
        return filter(bounds_grid.is_in_bounds, (a1 + dv, a2 - dv))

    @staticmethod
    def find_antinodes_p2(a1: Vector, a2: Vector, bounds_grid: Grid) -> Iterable[Vector]:
        dv = Vector(a1.x - a2.x, a1.y - a2.y)
        v = a1
        while bounds_grid.is_in_bounds(v):
            yield v
            v += dv
        v = a2
        while bounds_grid.is_in_bounds(v):
            yield v
            v -= dv

    @staticmethod
    def solve(city: Grid[str], antennas: dict[str, list[Vector]], antinode_func: Callable[[Vector, Vector, Grid], Iterable[Vector]]) -> int:
        antinode_locs: set[Vector] = set()
        for a_type, a_list in antennas.items():
            for a_pair in itertools.permutations(a_list, 2):
                for av in antinode_func(a_pair[0], a_pair[1], city):
                    antinode_locs.add(av)
        return len(antinode_locs)

    def solve_part1(self, input_str: str) -> str:
        city, antennas = self.parse_input(input_str)
        return str(self.solve(city=city, antennas=antennas, antinode_func=self.find_antinodes_p1))

    def solve_part2(self, input_str: str) -> str:
        city, antennas = self.parse_input(input_str)
        return str(self.solve(city=city, antennas=antennas, antinode_func=self.find_antinodes_p2))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=8, part=1, s_class=Day8, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=8, part=2, s_class=Day8, path_prefix='..', input_file='example_input.txt')
