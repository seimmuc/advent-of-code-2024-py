import re
from collections import deque

from common import Day, line_iterator


connection_regex = re.compile(r'([a-z]+)-([a-z]+)')


class LanComputer:
    def __init__(self, name: str):
        self.name: str = name
        self.connections: set[str] = set()


class Day23(Day):
    @staticmethod
    def parse_input(input_str: str) -> tuple[dict[str, LanComputer], list[tuple[str, str]]]:
        computers: dict[str, LanComputer] = {}
        connections: list[tuple[str, str]] = []
        for line in line_iterator(input_str):
            match = connection_regex.fullmatch(line)
            con = (match[1], match[2])
            connections.append(con)
            for c1, c2 in (con, (con[1], con[0])):
                if c1 not in computers:
                    computers[c1] = LanComputer(c1)
                c = computers[c1]
                c.connections.add(c2)
        return computers, connections

    def solve_part1(self, input_str: str) -> str:
        computers, _ = self.parse_input(input_str)
        three_sets: set[tuple[str, ...]] = set()
        for c1 in computers.values():
            for c1c in c1.connections:
                c2 = computers[c1c]
                for c2c in c2.connections:
                    if c2c in c1.connections:
                        three_sets.add(tuple(sorted((c1.name, c2.name, c2c))))
        result = 0
        for ts in three_sets:
            if any(cn.startswith('t') for cn in ts):
                result += 1
        return str(result)

    def solve_part2(self, input_str: str) -> str:
        computers, connections = self.parse_input(input_str)
        largest_network: tuple[str, ...] | None = None
        for conn in connections:
            conn_computers: list[str] = []
            discovered: set[str] = set()
            crawl_queue = deque([computers[conn[0]], computers[conn[1]]])
            while crawl_queue:
                c = crawl_queue.popleft()
                if all(cc in c.connections for cc in conn_computers):
                    conn_computers.append(c.name)
                for dc in c.connections:
                    if dc not in discovered:
                        crawl_queue.append(computers[dc])
                        discovered.add(dc)
            if len(conn_computers) > 2 and (largest_network is None or len(conn_computers) > len(largest_network)):
                largest_network = tuple(sorted(conn_computers))
        return ','.join(largest_network)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=23, part=1, s_class=Day23, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=23, part=2, s_class=Day23, path_prefix='..', input_file='example_input.txt')
