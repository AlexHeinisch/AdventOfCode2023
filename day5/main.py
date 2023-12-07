from typer import Typer
from typing import List, Callable, Dict, Tuple
import re

app = Typer()

class Map:
    _transformer: Callable[[int],int]

    def __init__(self, mapper_func: Callable[[int], int] | None = None) -> None:
        if mapper_func:
            self._transformer = mapper_func
        else:
            self._transformer = lambda x: x

    @staticmethod
    def from_map_block(block: str) -> 'Map':
        map = Map()
        for line in block.split('\n'):
            print(line)
            destination_range_start, source_range_start, range_length = [int(w) for w in line.split(' ')]
            def new_transformer(src: int) -> int:
                old = map.get_destination_from_source
                if src >= source_range_start and src < source_range_start + range_length:
                    return destination_range_start + (source_range_start - src)
                else:
                    old(src)
            map = Map(new_transformer)
        return map

    def get_destination_from_source(self, source: int) -> int:
        return self._transformer(source)


def solution_stage1(input_string: str) -> int:
    seeds = [int(s) for s in re.search(r'seeds:(.*?)\n', input_string).group(1).strip().split(' ')]
    print(seeds)
    seed_to_soil_map = Map.from_map_block(re.search(r'seed-to-soil map:\n(.*?)\n\n', flags=re.DOTALL, string=input_string).group(1))
    for i in range(100):
        print(i, seed_to_soil_map.get_destination_from_source(i))
    return 0
    
def solution_stage2(input_string: str) -> int:
    ...

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