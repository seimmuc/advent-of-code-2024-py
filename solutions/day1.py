from collections import Counter

from common import Day, line_iterator


class Day1(Day):
    @staticmethod
    def parse_input(input_str: str):
        l1 = []
        l2 = []
        for line in line_iterator(input_str):
            line = line.split()
            l1.append(int(line[0]))
            l2.append(int(line[1]))
        return l1, l2

    def solve_part1(self, input_str: str) -> str:
        l1, l2 = self.parse_input(input_str)
        l1.sort()
        l2.sort()
        dist = 0
        for n1, n2 in zip(l1, l2):
            dist += abs(n1 - n2)
        return str(dist)

    def solve_part2(self, input_str: str) -> str:
        l1, l2 = self.parse_input(input_str)
        c = Counter(l2)
        sim_score = 0
        for n1 in l1:
            sim_score += n1 * c[n1]
        return str(sim_score)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=1, part=1, s_class=Day1, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=1, part=2, s_class=Day1, path_prefix='..', input_file='example_input.txt')
