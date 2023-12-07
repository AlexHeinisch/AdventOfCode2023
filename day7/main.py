from typer import Typer
from typing import List, Callable
from functools import partial

app = Typer()

card_values_stage1 = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'J': 10,
    'Q': 11,
    'K': 12,
    'A': 13
}

card_values_stage2 = {
    'J': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'Q': 11,
    'K': 12,
    'A': 13
}

def compute_value(hand: str, stage: int) -> int:
    card_values = card_values_stage2 if stage == 2 else card_values_stage1

    # get how often each card is presented in the hand
    # dict contains hard and how often it occured
    # can at maximum contain 5 unique keys
    occurences = dict()
    for card in hand:
        if card not in occurences:
            occurences[card] = 1
        else:
            occurences[card] += 1
    
    num_jokers = 0
    # === STAGE 2 ONLY ===
    # treat jokers differently
    if stage == 2 and 'J' in occurences:
        num_jokers = occurences['J']
        del occurences['J']
    # ===

    # build occurence string from dict by taking the values and sorting
    # use this for general ranking based on patterns
    # them in descending order e.g. 32 for full-house or 2111 for 1 pair
    # stage2: Jokers are ommited
    vals = list(occurences.values())
    vals.sort(reverse=True)
    occ_str = ''.join([str(i) for i in vals])

    # num_jokers only apply to stage 2

    if num_jokers == 5 or occ_str == str(5-num_jokers): # five of a kind
        value = 7_00_00_00_00_00
    elif occ_str.startswith(str(4-num_jokers)): # four of a kind
        value = 6_00_00_00_00_00
    elif occ_str == '32' or (num_jokers == 1 and occ_str == '22'): # full house
        value = 5_00_00_00_00_00
    elif occ_str.startswith(str(3-num_jokers)): # three of a kind
        value = 4_00_00_00_00_00
    elif occ_str == '221': # joker doesnt help with 2 pairs 
        value = 3_00_00_00_00_00
    elif occ_str.startswith(str(2-num_jokers)): # one pair
        value = 2_00_00_00_00_00
    else: # highest card
        value = 1_00_00_00_00_00
    # now add the values of each card in hand by prioritizing
    # the first card most to apply secondary ranking
    for i,c in enumerate(hand):
        value += (10**(8-2*i))*card_values[c]
    return value
    

def solution(input_string: str, stage: int) -> int:
    hand_bid_pairs = []
    for line in input_string.split('\n'):
        splt = line.split(' ')
        hand_bid_pairs.append((splt[0], splt[1], compute_value(splt[0], stage=stage)))
    hand_bid_pairs.sort(key=lambda x: x[2]) # from weakest to highest by assigned value
    sum = 0
    for i,r in enumerate(hand_bid_pairs):
        sum += (i+1) * int(r[1])
    return sum


def run_with_input_file(input_file_path: str, solution: Callable):
    with open(input_file_path, 'r') as file:
        input = file.read()
    print(solution(input))

@app.command()
def run_stage1_sample():
    run_with_input_file('res/stage1_sample.txt', solution=partial(solution, stage=1))

@app.command()
def run_stage1_challenge():
    run_with_input_file('res/stage1_challenge.txt', solution=partial(solution, stage=1))

@app.command()
def run_stage2_sample():
    run_with_input_file('res/stage1_sample.txt', solution=partial(solution, stage=2))

@app.command()
def run_stage2_challenge():
    run_with_input_file('res/stage1_challenge.txt', solution=partial(solution, stage=2))

@app.command()
def run_custom(input_file_path: str, stage: int):
    run_with_input_file(input_file_path, solution=partial(solution, stage=stage))

if __name__ == '__main__':
    app()