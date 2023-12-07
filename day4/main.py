from typer import Typer
from typing import List, Callable, Dict, Tuple
from pydantic import BaseModel

app = Typer()

class ScratchCard(BaseModel):
    id: int
    winning_numbers: List[int]
    your_numbers: List[int]

    def get_num_matching_numbers(self) -> int:
        num_winning = 0
        for num in self.your_numbers:
            if num in self.winning_numbers:
                num_winning += 1
        return num_winning


    def get_value(self) -> int:
        num_winning = self.get_num_matching_numbers()
        return 2 ** (num_winning-1) if num_winning > 0 else 0

    @staticmethod
    def from_input_line(line: str) -> 'ScratchCard':
        main = line.split('|')
        secondary_split = main[0].split(':')
        return ScratchCard(
            id=int(secondary_split[0].split(' ')[-1]),
            winning_numbers=[int(w) for w in secondary_split[1].split(' ') if w != ''],
            your_numbers=[int(w) for w in main[1].split(' ') if w != '']
        )

def solution_stage1(input_string: str) -> int:
    return sum([c.get_value() for c in [ScratchCard.from_input_line(line) for line in input_string.split('\n')]])
    
def solution_stage2(input_string: str) -> int:
    cards = [ScratchCard.from_input_line(line) for line in input_string.split('\n')]
    # keep track of the number of each card in possession / won
    # since we can only win numbers of higher id we only need to iterate through all
    # starting cards, aka. O(n)
    num_cards = {c.id: 1 for c in cards}
    for card in cards:
        num_winning_numbers = card.get_num_matching_numbers()
        num_cards = num_cards[card.id]
        if num_winning_numbers > 0:
            for i in range(1,num_winning_numbers+1):
                num_cards[card.id + i] += num_cards
    return sum([c for c in num_cards.values()])



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