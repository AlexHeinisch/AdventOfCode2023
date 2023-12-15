from typing import Callable, Dict, List, Tuple
from typer import Typer

app = Typer()

def hash_string(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h

def solution(input: str) -> int:
    return sum([hash_string(s) for s in input.strip().split(',')])

def add_lens(boxes: Dict[int,List[Tuple[str,int]]], label: str, focal_length: int, box_num: int):
    if not box_num in boxes:
        boxes[box_num] = [(label, focal_length)]
        return
    box = boxes[box_num]
    if label in [t[0] for t in box]:
        for i,lens in enumerate(box):
            if lens[0] == label:
                boxes[box_num][i] = (label, focal_length)
    else:
        boxes[box_num].append((label, focal_length))

def remove_lens(boxes: Dict[int,List[Tuple[str,int]]], label: str, box_num: int):
    if box_num in boxes:
        for lens in boxes[box_num]:
            if lens[0] == label:
                boxes[box_num].remove(lens)

def solution2(input: str) -> int:
    boxes = dict()
    for command in input.strip().split(','):
        if '-' in command:
            lines = command.split('-')
            label = lines[0]
            box_num = 1+hash_string(label)
            remove_lens(boxes, label, box_num)
        else:
            lines = command.split('=')
            label = lines[0]
            lens_focal_length = int(lines[1])
            box_num = 1+hash_string(label)
            add_lens(boxes, label, lens_focal_length, box_num)
    total_focal_power = 0
    for box_num,box in boxes.items():
        for slot_num,lens in enumerate(box):
            #print(lens[0], box_num, slot_num+1, lens[1], box_num * (slot_num+1) * lens[1])
            total_focal_power += (box_num) * (slot_num+1) * lens[1]
    return total_focal_power

def run_with_input_file(input_file_path: str, solution: Callable[[str],int]) -> None:
    with open(input_file_path, 'r') as file:
        input = file.read()
    print(solution(input))

@app.command()
def run_stage1_sample():
    run_with_input_file('res/stage1_sample.txt', solution)

@app.command()
def run_stage2_sample():
    run_with_input_file('res/stage1_sample.txt', solution2)

@app.command()
def run_stage1_challenge():
    run_with_input_file('res/stage1_challenge.txt', solution)

@app.command()
def run_stage2_challenge():
    run_with_input_file('res/stage1_challenge.txt', solution2)

@app.command()
def run_custom(file_path: str, stage: int):
    run_with_input_file(file_path, solution if stage == 1 else solution2)

if __name__ == '__main__':
    app()
