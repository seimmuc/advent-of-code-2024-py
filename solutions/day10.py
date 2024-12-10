from common import Day, line_iterator, Grid, Vector, DIRECTIONS_CARDINAL


class Day10(Day):
    @staticmethod
    def parse_input(input_str: str) -> tuple[Grid[int], list[Vector]]:
        height_map: Grid[int] = Grid()
        trailheads: list[Vector] = []
        for y, s_line in enumerate(line_iterator(input_str)):
            line = list(int(c) for c in s_line)
            height_map.add_line(line)
            for x, h in enumerate(line):
                if h == 0:
                    trailheads.append(Vector(x, y))
        return height_map, trailheads

    @staticmethod
    def calc_trailhead_score_and_rating(height_map: Grid[int], trailhead: Vector) -> tuple[int, int]:
        summits = {}
        steps: list[Vector] = [trailhead]
        while steps:
            cl = steps.pop()
            ch = height_map.get_cell(cl)
            for l, h in height_map.look_around(cl, DIRECTIONS_CARDINAL):
                if h == ch + 1:
                    if h == 9:
                        summits[l] = summits.get(l, 0) + 1
                    else:
                        steps.append(l)
        return len(summits), sum(summits.values())


    def solve_part1(self, input_str: str) -> str:
        height_map, trailheads = self.parse_input(input_str)
        total_score = 0
        for th in trailheads:
            score, _ = Day10.calc_trailhead_score_and_rating(height_map, th)
            total_score += score
        return str(total_score)

    def solve_part2(self, input_str: str) -> str:
        height_map, trailheads = self.parse_input(input_str)
        total_rating = 0
        for th in trailheads:
            _, rating = Day10.calc_trailhead_score_and_rating(height_map, th)
            total_rating += rating
        return str(total_rating)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=10, part=1, s_class=Day10, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=10, part=2, s_class=Day10, path_prefix='..', input_file='example_input.txt')
