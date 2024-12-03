import re

from common import Day

regex = re.compile(r"(mul|do|don't)\(((?:\d+,?)*)\)")


class Day3(Day):
    @staticmethod
    def parse_input(input_str: str) -> list[tuple[str, list[int]]]:
        instructions: list[tuple[str, list[int] | None]] = []
        for m in regex.finditer(input_str):
            instr = m[1]
            params = None
            if instr == 'mul':
                params = list(int(s) for s in m[2].split(','))
                if len(params) != 2:
                    continue
            instructions.append((instr, params))
        return instructions

    def solve_part1(self, input_str: str) -> str:
        d = self.parse_input(input_str)
        total = 0
        for instr, params in d:
            if instr == 'mul':
                total += params[0] * params[1]
        return str(total)

    def solve_part2(self, input_str: str) -> str:
        d = self.parse_input(input_str)
        total = 0
        enabled = True
        for instr, params in d:
            if instr == 'mul':
                if enabled:
                    total += params[0] * params[1]
            elif instr == 'do':
                enabled = True
            else:
                enabled = False
        return str(total)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=3, part=1, s_class=Day3, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=3, part=2, s_class=Day3, path_prefix='..', input_file='example_input.txt')
