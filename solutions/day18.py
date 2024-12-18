import re
from collections import deque
from typing import Any

from common import Day, line_iterator, Vector, LGrid, DIRECTIONS_CARDINAL


coord_regex = re.compile(r'(\d+),(\d+)')


class Day18(Day):
    @staticmethod
    def parse_input(input_str: str) -> tuple[list[Vector], LGrid[Any], int]:
        byte_positions: list[Vector] = []
        for line in line_iterator(input_str):
            m = coord_regex.fullmatch(line)
            byte_positions.append(Vector(int(m[1]), int(m[2])))
        mem_space = LGrid()
        example = len(byte_positions) == 25
        w, h = (7, 7) if example else (71, 71)
        sim_length = 12 if example else 1024
        for _ in range(h):
            mem_space.add_line(['.'] * w)
        return byte_positions, mem_space, sim_length

    @staticmethod
    def find_a_shortest_path(mem_space: LGrid[str]) -> list[Vector] | None:
        end = Vector(mem_space.width - 1, mem_space.height - 1)
        reached_locations: dict[Vector, int] = {}
        steps: deque[tuple[Vector, list[Vector]]] = deque(((Vector(0, 0), []),))
        result: list[Vector] | None = None
        while steps:
            loc, path = steps.popleft()
            for nl, nv in mem_space.look_around(loc, DIRECTIONS_CARDINAL):
                if nv != '.':
                    continue
                step_count = len(path) + 1
                if nl in reached_locations and reached_locations[nl] <= step_count:
                    continue
                reached_locations[nl] = step_count
                path = path + [nl]
                if nl != end:
                    steps.append((nl, path))
                elif result is None or len(result) > len(path):
                    result = path
        return result

    @staticmethod
    def is_valid_path(mem_space: LGrid[str], path: list[Vector]) -> bool:
        for loc in path:
            if mem_space.get_cell(loc) != '.':
                return False
        return True

    def solve_part1(self, input_str: str) -> str:
        byte_positions, mem_space, sim_length = self.parse_input(input_str)
        for i in range(sim_length):
            mem_space.set_cell(byte_positions[i], '#')
        return str(len(Day18.find_a_shortest_path(mem_space)))

    def solve_part2(self, input_str: str) -> str:
        byte_positions, mem_space, sim_length = self.parse_input(input_str)
        for i in range(sim_length):
            mem_space.set_cell(byte_positions[i], '#')
        result = None
        last_path = set(Day18.find_a_shortest_path(mem_space))
        for i in range(sim_length, len(byte_positions)):
            bp = byte_positions[i]
            mem_space.set_cell(bp, '#')
            if bp not in last_path:
                continue
            lp = Day18.find_a_shortest_path(mem_space)
            if lp is None:
                result = f'{bp.x},{bp.y}'
                break
            last_path = set(lp)
        return result


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=18, part=1, s_class=Day18, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=18, part=2, s_class=Day18, path_prefix='..', input_file='example_input.txt')
