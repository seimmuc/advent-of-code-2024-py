from typing import Tuple, List

from common import Day, line_iterator, Grid, Vector, Direction, LGrid


MOVE_DIRS: dict[str, Direction] = {'^': Direction.Up, 'v': Direction.Down, '<': Direction.Left, '>': Direction.Right}


class Day15(Day):
    @staticmethod
    def parse_input(input_str: str) -> tuple[LGrid[str], Vector, list[Direction]]:
        warehouse: LGrid[str] = LGrid()
        robot_loc: Vector | None = None
        moves: list[Direction] = []
        li = line_iterator(input_str)
        for y, line in enumerate(li):
            if line == '':
                break
            if '@' in line:
                if robot_loc is not None:
                    raise RuntimeError('multiple robots')
                x = line.index('@')
                robot_loc = Vector(x, y)
                line = line.replace('@', '.')
            warehouse.add_line(list(line))
        if robot_loc is None:
            raise RuntimeError('robot not found')
        for line in li:
            for m in line:
                moves.append(MOVE_DIRS[m])
        return warehouse, robot_loc, moves

    @staticmethod
    def move_p1(warehouse: LGrid[str], from_loc: Vector, d: Direction) -> bool:
        item = warehouse.get_cell(from_loc)
        if item == '.':
            return True
        if item == '#':
            return False
        if item == 'O':
            new_loc = from_loc + d
            if Day15.move_p1(warehouse, new_loc, d):
                warehouse.set_cell(new_loc, item)
                warehouse.set_cell(from_loc, '.')
                return True
            return False
        raise RuntimeError(f'unknown item "{item}"')

    @staticmethod
    def calc_box_gps_sum(warehouse: LGrid[str]) -> int:
        result = 0
        for loc, item in warehouse.scan_all():
            if item == 'O' or item == '[':
                result += loc.y * 100 + loc.x
        return result

    def solve_part1(self, input_str: str) -> str:
        warehouse, robot_loc, moves = self.parse_input(input_str)
        for d in moves:
            nl = robot_loc + d
            if Day15.move_p1(warehouse, nl, d):
                robot_loc = nl
        return str(self.calc_box_gps_sum(warehouse))

    @staticmethod
    def widen(warehouse: LGrid[str]) -> LGrid[str]:
        nw: LGrid[str] = LGrid()
        for old in warehouse.lines:
            new = []
            for item in old:
                if item == '.' or item == '#':
                    new.extend([item] * 2)
                elif item == 'O':
                    new.extend(('[', ']'))
                else:
                    raise RuntimeError(f'unknown item "{item}"')
            nw.add_line(new)
        return nw

    @staticmethod
    def can_move_p2(warehouse: LGrid[str], from_loc: Vector, d: Direction, double_box=True) -> bool:
        item = warehouse.get_cell(from_loc)
        if item == '.':
            return True
        if item == '#':
            return False
        if item == '[' or item == ']':
            if double_box and d in (Direction.Up, Direction.Down):
                other = from_loc + (Direction.Right if item == '[' else Direction.Left)
                return Day15.can_move_p2(warehouse, from_loc, d, False) and Day15.can_move_p2(warehouse, other, d, False)
            new_loc = from_loc + d
            return Day15.can_move_p2(warehouse, new_loc, d)
        raise RuntimeError(f'unknown item "{item}"')

    @staticmethod
    def do_move_p2(warehouse: LGrid[str], from_loc: Vector, d: Direction):
        item = warehouse.get_cell(from_loc)
        if item == '[' or item == ']':
            all_items: list[Vector] = [from_loc]
            if d in (Direction.Up, Direction.Down):
                other = from_loc + (Direction.Right if item == '[' else Direction.Left)
                all_items.insert(0, other)
            for l in all_items:
                nl = l + d
                Day15.do_move_p2(warehouse, nl, d)
                warehouse.set_cell(nl, warehouse.get_cell(l))
                warehouse.set_cell(l, '.')
        if item == '#':
            raise RuntimeError('cannot move wall')

    def solve_part2(self, input_str: str) -> str:
        warehouse, robot_loc, moves = self.parse_input(input_str)
        warehouse = self.widen(warehouse)
        robot_loc = robot_loc.move_in(Direction.Right, robot_loc.x)
        for d in moves:
            nl = robot_loc + d
            if Day15.can_move_p2(warehouse, nl, d):
                Day15.do_move_p2(warehouse, nl, d)
                robot_loc = nl
        return str(self.calc_box_gps_sum(warehouse))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=15, part=1, s_class=Day15, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=15, part=2, s_class=Day15, path_prefix='..', input_file='example_input.txt')
