from typer import Typer
from pydantic import BaseModel
from typing import List, Callable
import re

app = Typer()

class Game(BaseModel):
    id: int
    red_cubes_pulled: List[int]
    blue_cubes_pulled: List[int]
    green_cubes_pulled: List[int]

    def validate_max_green(self, max_num: int) -> bool:
        return all([i <= max_num for i in self.green_cubes_pulled])

    def validate_max_red(self, max_num: int) -> bool:
        return all([i <= max_num for i in self.red_cubes_pulled])

    def validate_max_blue(self, max_num: int) -> bool:
        return all([i <= max_num for i in self.blue_cubes_pulled])

    def validate_all(self, max_green: int, max_blue: int, max_red: int) -> bool:
        return self.validate_max_green(max_green) and self.validate_max_blue(max_blue) and self.validate_max_red(max_red)

    def pow_of_min_req_cubes(self) -> int:
        return max(self.blue_cubes_pulled) * max(self.red_cubes_pulled) * max(self.green_cubes_pulled)

    @staticmethod
    def from_game_line(line: str) -> 'Game':
        idx = line.find(':')
        game = Game(
            id=int(line[:idx].split(' ')[1]),
            red_cubes_pulled=[],
            blue_cubes_pulled=[],
            green_cubes_pulled=[]
        )
        for pull in line[idx+1:].split(';'):
            blue = re.search(r'(\d+) blue', pull)
            game.blue_cubes_pulled.append(0 if not blue else int(blue.group(1)))
            red = re.search(r'(\d+) red', pull)
            game.red_cubes_pulled.append(0 if not red else int(red.group(1)))
            green = re.search(r'(\d+) green', pull)
            game.green_cubes_pulled.append(0 if not green else int(green.group(1)))
        return game
            
def solution_stage1(input_string: str) -> int:
    games: List[Game] = []
    for line in input_string.split('\n'):
        games.append(Game.from_game_line(line))
    return sum([g.id for g in games if g.validate_all(max_red=12, max_green=13, max_blue=14)])
    
def solution_stage2(input_string: str) -> int:
    games: List[Game] = []
    for line in input_string.split('\n'):
        games.append(Game.from_game_line(line))
    return sum(g.pow_of_min_req_cubes() for g in games)


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