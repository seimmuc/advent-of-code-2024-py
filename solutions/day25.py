import itertools

from common import Day, line_iterator, Grid


class Day25(Day):
    @staticmethod
    def parse_input(input_str: str) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
        locks: list[tuple[int, ...]] = []
        keys: list[tuple[int, ...]] = []
        g: Grid[str] = Grid()
        for line in itertools.chain(line_iterator(input_str), ['']):
            if line != '':
                g.add_line(line)
                continue
            lst = locks if g.lines[0][0] == '#' else keys
            heights: tuple[int, ...] = tuple(sum(int(c == '#') for _, c in g.scan_column(x)) - 1 for x in range(g.width))
            lst.append(heights)
            g = Grid()
        return locks, keys

    @staticmethod
    def can_fit(lock: tuple[int, ...], key: tuple[int, ...]) -> int:
        for i in range(5):
            if lock[i] + key[i] > 5:
                return False
        return True

    def solve_part1(self, input_str: str) -> str:
        locks, keys = self.parse_input(input_str)
        result = 0
        for lock, key in itertools.product(locks, keys):
            if Day25.can_fit(lock, key):
                result += 1
        return str(result)

    def solve_part2(self, input_str: str) -> str:
        d = self.parse_input(input_str)
        return None


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=25, part=1, s_class=Day25, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=25, part=2, s_class=Day25, path_prefix='..', input_file='example_input.txt')
