from collections import deque, defaultdict

from common import Day, line_iterator


def get_next_secret(sn: int) -> int:
    sn = (sn ^ (sn * 64)) % 16777216
    sn = (sn ^ (sn // 32)) % 16777216
    return (sn ^ (sn * 2048)) % 16777216


class Day22(Day):
    @staticmethod
    def parse_input(input_str: str) -> list[int]:
        initial_secrets: list[int] = list(int(s.strip()) for s in line_iterator(input_str))
        return initial_secrets

    def solve_part1(self, input_str: str) -> str:
        initial_secrets = self.parse_input(input_str)
        result = 0
        for sn in initial_secrets:
            for _ in range(2000):
                sn = get_next_secret(sn)
            result += sn
        return str(result)

    def solve_part2(self, input_str: str) -> str:
        initial_secrets = self.parse_input(input_str)
        sequences: dict[tuple[int, ...], list[int | None]] = defaultdict(lambda: [None] * len(initial_secrets))
        for i, sn in enumerate(initial_secrets):
            old_price = sn % 10
            diffs: deque[int] = deque(maxlen=4)
            for _ in range(3):
                sn = get_next_secret(sn)
                price = sn % 10
                diffs.append(price - old_price)
                old_price = price
            for _ in range(1997):
                sn = get_next_secret(sn)
                price = sn % 10
                diffs.append(price - old_price)
                old_price = price
                seq = tuple(diffs)
                seq_list = sequences[seq]
                if seq_list[i] is None:
                    seq_list[i] = price
        result = 0
        for seq, prices in sequences.items():
            ps = sum(p for p in prices if p is not None)
            if ps > result:
                result = ps
        if False:
            import sys
            sequences_mem_usage = sys.getsizeof(sequences)
            for k, v in sequences.items():
                sequences_mem_usage += sys.getsizeof(k) + sys.getsizeof(v)
            print(f'memory usage: {sequences_mem_usage} bytes')
        return str(result)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=22, part=1, s_class=Day22, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=22, part=2, s_class=Day22, path_prefix='..', input_file='example_input.txt')
