import sys
import time
from importlib import import_module
from pathlib import Path
from timeit import timeit
from types import ModuleType, NoneType
from typing import Literal, Dict, Type, Protocol

from common import Day


dir_names = {'inputs': 'inputs', 'solutions': 'solutions'}


class SolutionMethod(Protocol):
    def __call__(self, input_str: str) -> str:
        pass


def generate_new_day(args: list[str]):
    if len(args) < 1:
        print('Error: must specify day number')
        return
    try:
        day_num = int(args[0])
    except ValueError:
        print(f'Error: day number must be an integer ({args[0]})')
        return
    py_path = Path(dir_names['solutions'], f'day{day_num}.py')
    in_path = Path(dir_names['inputs'], f'd{day_num}.txt')
    tm_path = Path('day_template')
    if py_path.exists():
        print(f'Error: {py_path} already exists!')
        return
    with tm_path.open(mode='rt', encoding='utf8', newline='\n') as ft,\
         py_path.open(mode='wt', encoding='utf8', newline='\n') as fp:
        fp.write(ft.read().replace('{{day_num}}', str(day_num)))
    if in_path.exists():
        print(f'Warning: {in_path} already exists, it will not be recreated')
    else:
        in_path.touch(exist_ok=True)


def run_puzzle(day: int, part: Literal[1, 2], version: str = None, s_module: str | ModuleType = None,
               s_class: str | Type[Day] = None, s_inst_kwargs: Dict = None, s_instance: Day = None,
               input_file: str = None, path_prefix: str = '', time_iters: int | None = None):
    if part not in (1, 2):
        raise ValueError(f'Invalid part: {part}')
    if s_instance is None:
        if isinstance(s_class, (str, NoneType)):
            if not isinstance(s_module, ModuleType):
                if s_module is None:
                    s_module = f'day{day}'
                s_module = import_module(f'{dir_names["solutions"]}.{s_module}')
            if s_class is None:
                s_class = f'Day{day}'
                if version:
                    s_class += f'V{version}'
            s_class = getattr(s_module, s_class)
        day_class: Type[Day] = s_class
        # noinspection PyArgumentList
        s_instance = day_class(**({} if s_inst_kwargs is None else s_inst_kwargs))
    solve_method: SolutionMethod = s_instance.solve_part1 if part == 1 else s_instance.solve_part2

    if input_file is None:
        input_file = f'd{day}.txt'
    else:
        print(f'using alternative input file "{input_file}"')
    in_path = Path(path_prefix, dir_names['inputs'], input_file)
    if not in_path.is_file():
        print(f'Error: no input file found at "{in_path}"')
        return
    with in_path.open(mode='rt', encoding='utf8', newline='\n') as f:
        puzzle_input = f.read()
    if time_iters is not None and time_iters > 0:
        print(f'Benchmarking day {day} part {part}', '' if version is None else f' (ver {version})', sep='')
        t = timeit(stmt=lambda: solve_method(input_str=puzzle_input), number=time_iters)
        iter_ms = t * (1000 / time_iters)
        print(f'Ran {time_iters} iterations in {t:.3f}s')
        print(f'Iteration time: {iter_ms:.6f}ms')
    else:
        print(f'Solving day {day} part {part}', '' if version is None else f' (ver {version})', sep='')
        start_time = time.time()
        # noinspection PyArgumentList
        solution_output = solve_method(input_str=puzzle_input)
        elapsed_time = time.time() - start_time
        if isinstance(solution_output, str):
            print(f'Done in {elapsed_time:.3f}s, printing answer')
            print('=======================')
            print(solution_output)
            print('=======================')
        else:
            print(f'Error: solution output is of invalid type: {type(solution_output)}')


def run(args: list[str]):
    day = 1
    part: Literal[1, 2] = 1
    ver: str | None = None
    example_input = False
    time_iters = None
    for arg in args:
        arg = arg.lower()
        if arg.startswith('d'):
            day = int(arg[1:])
        elif arg.startswith('p'):
            # noinspection PyTypeChecker
            part = int(arg[1:])
            if part not in (1, 2):
                print(f'Error: part must equal 1 or 2 ({part})')
                return
        elif arg.startswith('ver'):
            ver = arg[3:]
        elif arg == 'e' or arg == 'exampleinput':
            example_input = True
        elif arg.startswith('t'):
            if arg == 't' or arg == 'time':
                time_iters = 100
            else:
                time_iters = int(arg[1:])
    in_file = 'example_input.txt' if example_input else None
    run_puzzle(day=day, part=part, version=ver, input_file=in_file, time_iters=time_iters)


if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) > 0:
        if argv[0].lower() == 'new':
            generate_new_day(argv[1:])
        elif argv[0].lower() == 'run':
            run(argv[1:])
        else:
            print(f'Unknown command: {argv[0]}')
    else:
        run([])
