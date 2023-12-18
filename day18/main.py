from typing import Callable, List, Tuple
from typer import Typer

app = Typer()

def expand_plan(plan: List[List[str]], x: int, y: int, direction: str, num_expand) -> Tuple[int, int]:
    if direction in ['R', 'L']:
        for r_idx in range(len(plan)):
            if direction == 'L':
                for _ in range(num_expand):
                    plan[r_idx].insert(0, '.')
                x += num_expand
            else: # R
                for _ in range(num_expand):
                    plan[r_idx].append('.')
    else: # 'D' or 'U'
        if direction == 'D':
            for _ in range(num_expand):
                plan.append(['.' for _ in range(len(plan[0]))])
        else: # 'U'
            for _ in range(num_expand):
                plan.insert(0, ['.' for _ in range(len(plan[0]))])
            y += num_expand
    return x,y

def move_digger(command_line: str, plan: List[List[str]], x: int, y: int) -> Tuple[int, int]:
    ...

def solution(input: str) -> int:
    x, y = 0,0
    plan = [['.']]
    for line in input.strip().split('\n'):
        if line:
            x, y = move_digger(line, plan, x, y)
    print(plan)
    return 0

def run_with_input_file(input_file_path: str, solution: Callable[[str],int]) -> None:
    with open(input_file_path, 'r') as file:
        input = file.read()
    print(solution(input))

@app.command()
def run_stage1_sample():
    run_with_input_file('res/stage1_sample.txt', solution)

@app.command()
def run_stage2_sample():
    run_with_input_file('res/stage1_sample.txt', solution)

@app.command()
def run_stage1_challenge():
    run_with_input_file('res/stage1_challenge.txt', solution)

@app.command()
def run_stage2_challenge():
    run_with_input_file('res/stage1_challenge.txt', solution)

@app.command()
def run_custom(file_path: str, stage: int):
    run_with_input_file(file_path, solution if stage == 1 else solution2)

if __name__ == '__main__':
    app()
