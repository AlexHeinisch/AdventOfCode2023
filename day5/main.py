from functools import wraps
from typer import Typer
from typing import List, Callable, Dict, Tuple
import re
import tqdm

app = Typer()

def create_mapper_func(map_configurator_string: str) -> Callable[[int],int]:
    func = lambda x: x

    def transformer(func: Callable[[int],int], destination_range_start: int, source_range_start: int, range_length: int) -> Callable[[int],int]:
        @wraps(func)
        def new_func(x: int) -> int:
            if source_range_start <= x < source_range_start + range_length:
                return destination_range_start + (x - source_range_start)
            else:
                return func(x)
        return new_func

    for line in map_configurator_string.split('\n'):
        destination_range_start, source_range_start, range_length = [int(stmt) for stmt in line.split(' ')]
        func = transformer(func, destination_range_start, source_range_start, range_length)

    return func

def solution_stage1(input_string: str) -> int:
    seeds: List[int] = [int(s) for s in re.search(r'seeds:(.*?)\n', input_string).group(1).strip().split(' ')]
    mapper_dict: Dict[Tuple[str,str],Callable[[int],int]] = dict()

    # generate all provided mappers
    for match in re.findall(r'([a-z]*?)-to-(.*?) map:\n((?:\d+\s\d+\s\d+\n)*)', flags=re.DOTALL, string=input_string):
        mapper_dict[(match[0],match[1])] = create_mapper_func(match[2].strip())

    def concat_funcs(f1: Callable[[int], int], f2: Callable[[int],int]) -> Callable[[int],int]:
        @wraps(f2)
        def new_func(x: int):
            return f2(f1(x))
        return new_func

    # build transitive closure over given elements
    while True:
        new_mappers = {(a[0],b[1]): concat_funcs(fa, fb) for a,fa in mapper_dict.items() for b,fb in mapper_dict.items() if a[1] == b[0] and (a[0],b[1]) not in mapper_dict.keys()}
        if len(new_mappers) == 0:
            break
        mapper_dict.update(new_mappers)

    # get mapping function from seed to location
    # needs to be in mapper since transitive relation is mandatory for this assignment to work
    seed2loc = mapper_dict[('seed', 'location')]
    locations = [seed2loc(seed) for seed in seeds]
    return min(locations)
    
def solution_stage2(input_string: str) -> int:
# ideas: graph theoretic limit checking... e.g. only check the edge cases for each interval
# inverse-map: count up and find matching seed -> more easy with less mathematical thinking


def run_with_input_file(input_file_path: str, solution: Callable):
    with open(input_file_path, 'r') as file:
        input = file.read()
    print(solution(input))

@app.command()
def run_stage1_sample():
    run_with_input_file('res/stage1_sample.txt', solution=solution_stage1)

@app.command()
def run_stage1_challenge():
    run_with_input_file('res/stage1_challenge.txt', solution=solution_stage1)

@app.command()
def run_stage2_sample():
    run_with_input_file('res/stage1_sample.txt', solution=solution_stage2)

@app.command()
def run_stage2_challenge():
    run_with_input_file('res/stage1_challenge.txt', solution=solution_stage2)

if __name__ == '__main__':
    app()
