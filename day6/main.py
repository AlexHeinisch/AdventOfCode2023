from typing import List, Tuple
from typer import Typer
from functools import reduce
import re
import math

app = Typer()

#### naive implementation
#def get_num_of_ways_to_beat_race(time: int, min_distance: int):
#    num = 0
#    for i in range(1,time-1):
#        if (time - i) * i > min_distance:
#            num += 1
#    return num

# min_distance = (time - t) * t
# 0 = -t**2 + time*t - min_distance
# x1/2 = (-time +- sqrt(time**2 - 4*min_distance)) / -2
def get_num_of_ways_to_beat_race(time: int, min_distance: int) -> int:
    x1 = (- time + math.sqrt(time**2 - 4 * min_distance)) / -2
    x2 = (- time - math.sqrt(time**2 - 4 * min_distance)) / -2
    return math.floor(x2) - math.ceil(x1) + 1

def get_races_from_input(inp: str, challenge_type: int) -> List[Tuple[int, int]]:
    if challenge_type == 1:
        s = re.sub(' +', ' ', inp)
        lines = s.split('\n')
        times = [int(w) for w in lines[0].split(' ')[1:]]
        min_dist = [int(w) for w in lines[1].split(' ')[1:]]
        return list(zip(times, min_dist))
    else:
        s = re.sub(' +', '', inp) # remove all whitespaces
        lines = s.split('\n')
        time = int(lines[0].split(':')[1])
        min_dist = int(lines[1].split(':')[1])
        return [(time, min_dist)]

def solution(input: str, stage: int) -> int:
    return reduce(
        lambda x,y: x * y, 
        [get_num_of_ways_to_beat_race(*r) for r in get_races_from_input(input, stage)]
    )

def run_with_input_file(input_file_path: str, stage: int) -> None:
    with open(input_file_path, 'r') as file:
        input = file.read()
    print(solution(input, stage=stage))

@app.command()
def run_stage1_sample():
    run_with_input_file('res/stage1_sample.txt', stage=1)

@app.command()
def run_stage2_sample():
    run_with_input_file('res/stage1_sample.txt', stage=2)

@app.command()
def run_stage1_challenge():
    run_with_input_file('res/stage1_challenge.txt', stage=1)

@app.command()
def run_stage2_challenge():
    run_with_input_file('res/stage1_challenge.txt', stage=2)

@app.command()
def run_custom(file_path: str, stage: int):
    run_with_input_file(file_path, stage)

if __name__ == '__main__':
    app()
