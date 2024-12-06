import re

from common import Day, line_iterator


or_regex = re.compile(r'(\d+)\|(\d+)')


class Day5(Day):
    @staticmethod
    def parse_input(input_str: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
        order_rules: list[tuple[int, int]] = []
        updates: list[list[int]] = []
        li = line_iterator(input_str)
        for line in li:
            line = line.strip()
            if line == '':
                break
            rule_match = or_regex.fullmatch(line)
            order_rules.append((int(rule_match[1]), int(rule_match[2])))
        for line in li:
            updates.append(list(int(s.strip()) for s in line.split(',')))
        return order_rules, updates

    @staticmethod
    def check_rule(update: list[int], rule: tuple[int, int]) -> bool:
        hit_last = False
        for page in update:
            if page == rule[0]:
                return not hit_last
            if page == rule[1]:
                hit_last = True
        return True

    @staticmethod
    def check_all_rules(update: list[int], rules: list[tuple[int, int]]) -> bool:
        return all(Day5.check_rule(update, rule) for rule in rules)

    @staticmethod
    def get_middle(update: list[int]) -> int:
        if len(update) % 2 == 0:
            raise RuntimeError('update length must be odd')
        return update[len(update) // 2]

    def solve_part1(self, input_str: str) -> str:
        rules, updates = self.parse_input(input_str)
        result = 0
        for upd in updates:
            if Day5.check_all_rules(upd, rules):
                result += Day5.get_middle(upd)
        return str(result)

    @staticmethod
    def rule_applies(update: list[int], rule: tuple[int, int]) -> bool:
        return rule[0] in update and rule[1] in update

    @staticmethod
    def apply_rule(update: list[int], rule: tuple[int, int]):
        i0 = update.index(rule[0])
        i1 = update.index(rule[1])
        if i0 < i1:
            return
        r = update[i0]
        update[i0] = update[i1]
        update[i1] = r

    def solve_part2(self, input_str: str) -> str:
        rules, updates = self.parse_input(input_str)
        result = 0
        for upd in updates:
            if Day5.check_all_rules(upd, rules):
                continue
            s_rules = list(r for r in rules if Day5.rule_applies(upd, r))
            while True:
                for rule in s_rules:
                    Day5.apply_rule(upd, rule)
                if Day5.check_all_rules(upd, rules):
                    break
            result += Day5.get_middle(upd)
        return str(result)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=5, part=1, s_class=Day5, path_prefix='..', input_file='example_input.txt')
    run_puzzle(day=5, part=2, s_class=Day5, path_prefix='..', input_file='example_input.txt')
