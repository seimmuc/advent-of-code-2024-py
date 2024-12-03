from typing import Sequence

from common import Day, line_iterator


class Day2(Day):
    @staticmethod
    def parse_input(input_str: str) -> list[list[int]]:
        reports: list[list[int]] = []
        for line in line_iterator(input_str):
            reports.append(list(int(s) for s in line.split()))
        return reports

    @staticmethod
    def diff_direction(num1: int, num2: int) -> int:
        if num1 < num2:
            return 1
        elif num1 > num2:
            return -1
        else:
            return 0

    @staticmethod
    def is_safe(report: Sequence[int]) -> bool:
        mn, mx = (1, 3) if report[0] < report[1] else (-3, -1)
        for i in range(0, len(report) - 1):
            d = report[i + 1] - report[i]
            if d < mn or d > mx:
                return False
        return True

    @staticmethod
    def is_safe_tol(report: list[int], tolerance: int) -> bool:
        # catches most safe reports with single iteration, but misses some like [1, 3, 2, 3] with tolerance of 1
        dd = Day2.diff_direction(report[0], report[-1])
        it = iter(report)
        prev_num = next(it)
        for cur_num in it:
            d = abs(prev_num - cur_num)
            if d < 1 or d > 3 or Day2.diff_direction(prev_num, cur_num) != dd:
                tolerance -= 1
                if tolerance < 0:
                    return False
            else:
                prev_num = cur_num
        return True

    def solve_part1(self, input_str: str) -> str:
        reports = self.parse_input(input_str)
        safe_count = 0
        for report in reports:
            if Day2.is_safe(report):
                safe_count += 1
        return str(safe_count)

    def solve_part2(self, input_str: str) -> str:
        reports = self.parse_input(input_str)
        safe_count = 0
        for report in reports:
            if Day2.is_safe(report) or Day2.is_safe_tol(report, 1):
                safe_count += 1
            else:
                for i in range(len(report)):
                    rc = report.copy()
                    rc.pop(i)
                    if Day2.is_safe(rc):
                        safe_count += 1
                        break
        return str(safe_count)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=2, part=1, s_class=Day2, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=2, part=2, s_class=Day2, path_prefix='..', input_file='example_input.txt')
