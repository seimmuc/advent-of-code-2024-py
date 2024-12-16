from collections import deque
from typing import Tuple, Self, Iterable

from common import Day, line_iterator, Grid, GridSearch, Vector, LGrid, DIRECTIONS_CARDINAL, Direction, \
    DIRECTION_TURN_CARDINAL


DIR_INDEX: dict[Direction, int]  = dict((d, i) for i, d in enumerate(DIRECTIONS_CARDINAL))


class MazeStep:
    __slots__ = ['loc', 'dir', 'score', 'prev', 'next', 'bad']

    def __init__(self, loc: Vector, d: Direction, score: int, prev: Self | None):
        self.loc = loc
        self.dir = d
        self.score = score
        self.prev: Self | None | list[Self] = prev
        self.next: list[Self] = []
        self.bad = False

    def add_prev(self, prev_step: Self):
        if self.prev is None:
            self.prev = prev_step
            return
        if type(self.prev) != list:
            self.prev = [self.prev]
        self.prev.append(prev_step)

    def add_next(self, next_step: Self):
        self.next.append(next_step)

    def mark_as_bad(self):
        self.bad = True
        for ns in self.next:
            ns.mark_as_bad()

    def next_steps(self) -> Iterable[Self]:
        yield MazeStep(self.loc + self.dir, self.dir, self.score + 1, self)
        yield MazeStep(self.loc, DIRECTION_TURN_CARDINAL[self.dir]['right'], self.score + 1000, self)
        yield MazeStep(self.loc, DIRECTION_TURN_CARDINAL[self.dir]['left'], self.score + 1000, self)


class Day16(Day):
    @staticmethod
    def parse_input(input_str: str) -> tuple[Grid[bool], Vector, Vector]:
        maze: Grid[bool] = Grid()
        start_search = GridSearch(search_char='S', replace_char='.', max_count=1)
        end_search = GridSearch(search_char='E', replace_char='.', max_count=1)
        for y, line in enumerate(line_iterator(input_str)):
            line = start_search.search_line(line, y)
            line = end_search.search_line(line, y)
            maze.add_line(list(c == '.' for c in line))
        return maze, start_search.single_result(), end_search.single_result()

    @staticmethod
    def find_best_paths(maze: Grid[bool], start: Vector, end: Vector) -> list[MazeStep]:
        overlay: LGrid[list[MazeStep | None]] = LGrid()
        for y in range(maze.height):
            overlay.add_line(list([None, None, None, None] for _ in range(maze.width)))
        steps: deque[MazeStep] = deque([MazeStep(loc=start, d=Direction.Right, score=0, prev=None)])
        while steps:
            step = steps.popleft()
            if step.bad:
                continue
            for ns in step.next_steps():
                if not maze.get_cell(ns.loc):
                    continue
                cell_scores = overlay.get_cell(ns.loc)
                di = DIR_INDEX[ns.dir]
                if cell_scores[di] is None or cell_scores[di].score > ns.score:
                    if cell_scores[di] is not None and not cell_scores[di].bad:
                        cell_scores[di].mark_as_bad()
                    cell_scores[di] = ns
                    steps.append(ns)
                    step.add_next(ns)
                elif cell_scores[di].score == ns.score:
                    cell_scores[di].add_prev(step)
        end_steps: list[MazeStep] = list(s for s in overlay.get_cell(end) if s is not None and not s.bad)
        best_score = min(s.score for s in end_steps)
        end_steps = list(s for s in end_steps if s.score == best_score)
        return end_steps

    def solve_part1(self, input_str: str) -> str:
        maze, start, end = self.parse_input(input_str)
        best_paths = self.find_best_paths(maze, start, end)
        return str(best_paths[0].score)

    def solve_part2(self, input_str: str) -> str:
        maze, start, end = self.parse_input(input_str)
        best_paths = self.find_best_paths(maze, start, end)
        bp_tiles: set[Vector] = set()
        for bp in best_paths:
            steps = [bp]
            while steps:
                s = steps.pop()
                bp_tiles.add(s.loc)
                if s.prev is not None:
                    if type(s.prev) == list:
                        steps.extend(s.prev)
                    else:
                        steps.append(s.prev)
        return str(len(bp_tiles))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=16, part=1, s_class=Day16, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=16, part=2, s_class=Day16, path_prefix='..', input_file='example_input.txt')
