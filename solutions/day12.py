from collections.abc import Iterator

from common import Day, line_iterator, Grid, LGrid, Vector, DIRECTIONS_CARDINAL, DIRECTION_TURN_CARDINAL


class Day12(Day):
    @staticmethod
    def parse_input(input_str: str) -> Grid[str]:
        garden: Grid[str] = Grid()
        for line in line_iterator(input_str):
            garden.add_line(line)
        return garden

    def solve_part1(self, input_str: str) -> str:
        garden = self.parse_input(input_str)
        overlay: LGrid[bool] = LGrid()
        for y in range(garden.height):
            overlay.add_line([False] * garden.width)
        total_price = 0
        for ol, ov in overlay.scan_all():
            if ov is True:
                continue
            r_area = 0
            r_per = 0
            r_type = garden.get_cell(ol)
            cells = [ol]
            overlay.set_cell(ol, True)
            while cells:
                rv = cells.pop()
                r_area += 1
                for d in DIRECTIONS_CARDINAL:
                    v = rv + d
                    if (not garden.is_in_bounds(v)) or garden.get_cell(v) != r_type:
                        r_per += 1
                    elif overlay.get_cell(v) is False:
                        cells.append(v)
                        overlay.set_cell(v, True)
            total_price += r_area * r_per
        return str(total_price)

    def solve_part2(self, input_str: str) -> str:
        garden = self.parse_input(input_str)
        overlay: LGrid[int] = LGrid()   # 0 = unseen, 1: queued, 2: processed
        for y in range(garden.height):
            overlay.add_line([0] * garden.width)
        total_price = 0
        for ol, ov in overlay.scan_all():
            if ov > 0:
                continue
            r_area = 0
            r_sides = 0
            r_type = garden.get_cell(ol)
            cells = [ol]
            overlay.set_cell(ol, 1)
            while cells:
                rv = cells.pop()
                overlay.set_cell(rv, 2)
                r_area += 1
                for d in DIRECTIONS_CARDINAL:
                    v = rv + d
                    if (not garden.is_in_bounds(v)) or garden.get_cell(v) != r_type:
                        add_sides = 1
                        for t in ('left', 'right'):
                            nei_loc = rv + DIRECTION_TURN_CARDINAL[d][t]
                            nei_wcl = nei_loc + d
                            if garden.is_in_bounds(nei_loc) and overlay.get_cell(nei_loc) == 2 and\
                                    garden.get_cell(nei_loc) == r_type and\
                                    ((not garden.is_in_bounds(nei_wcl)) or garden.get_cell(nei_wcl) != r_type):
                                add_sides -= 1
                        if add_sides != 0:
                            r_sides += add_sides
                    elif overlay.get_cell(v) == 0:
                        cells.append(v)
                        overlay.set_cell(v, 1)
            total_price += r_area * r_sides
        return str(total_price)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=12, part=1, s_class=Day12, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=12, part=2, s_class=Day12, path_prefix='..', input_file='example_input.txt')
