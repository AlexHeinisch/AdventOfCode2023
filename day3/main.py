from typer import Typer
from typing import List, Callable, Dict, Tuple
from functools import partial
import math

app = Typer()

def check_if_symbol(row: int, col: int, matrix: List[str]) -> bool:
    try:
        return matrix[row][col] not in '.0123456789'
    except:
        return False

# check if character at position [row, col] is next to a symbol
def has_symbol_in_proximity(matrix: List[str], row: int, col: int) -> bool:
    check = partial(check_if_symbol, matrix=matrix)
    return check(row-1, col-1) or check(row-1, col) or check(row-1, col+1) \
        or check(row, col-1) or check(row, col+1) \
        or check(row+1, col-1) or check(row+1, col) or check(row+1, col+1)
    

def solution_stage1(input_string: str) -> int:
    matrix: List[str] = input_string.split('\n')

    # variable to store results
    sum_part_nums = 0

    for row,line in enumerate(matrix):
        is_part_num = False # defined by a number having a symbol in its proximity
        current_num = 0 # variable to build current number
        for col,char in enumerate(line):
            if char.isdigit():
                # extend current number digit by digit
                # e.g. if number 34 is stored and the next digit found is 6
                # 34*10=340 340+6 = 346
                current_num = current_num * 10 + int(char)

                # check if digit has a symbol in its proximity, if yes set the flag for this number
                is_part_num = is_part_num or has_symbol_in_proximity(matrix, row, col)
            elif current_num != 0: # if number is finished
                if is_part_num: # only add to sum of part nums if it is a part number
                    sum_part_nums += current_num
                    is_part_num = False
                current_num = 0

        # edge case where number is at end of line
        if current_num != 0:
            if is_part_num:
                sum_part_nums += current_num
                is_part_num = False
            current_num = 0
    return sum_part_nums

# check if character at location [row,col] has digits in its proximity, returning their positions
def get_digit_locations_in_proximity(matrix: List[str], row: int, col: int) -> List[Tuple[int, int]]:
    lst = []
    def add_if_digit(r, c):
        if matrix[r][c].isdigit():
            lst.append((r,c))
    for row_idx in [-1, 0, 1]:
        for col_idx in [-1, 0, 1]:
            add_if_digit(row_idx + row, col_idx + col)
    return lst

def solution_stage2(input_string: str) -> int:
    matrix: List[str] = input_string.split('\n')

    # 'Hashmap' containing all found values within the blueprint
    # If a value is 2 digits long, it will have 2 different entries
    # with the same ID
    # They are stored in the format:
    # Key: Tuple[col, row]
    # Value: Tuple[ID, value]
    # The id is necessary to check if entries in the dict with the same value
    # correspond to the same number or are actually different numbers with equal values
    num_dict: Dict[Tuple[int, int], int] = dict()
    num_id = 0

    # get all the numbers in the blueprint and put them in a hashmap
    for row,line in enumerate(matrix):
        current_num = 0
        for col,char in enumerate(line):
            if char.isdigit():
                current_num = current_num * 10 + int(char)
            elif current_num != 0:
                # put all positions the number is on in the hashmap aka dict
                for i in range(math.floor(math.log10(current_num))+1):
                    num_dict[(row, col-i-1)] = (num_id, current_num)
                num_id += 1
                current_num = 0

        # compute case where number is at end of line
        if current_num != 0:
            for i in range(math.floor(math.log10(current_num))+1):
                num_dict[(row, col-i)] = (num_id, current_num)
            num_id += 1
            current_num = 0
    
    sum_gear_ratios = 0
    # find all * characters and find the digits in their proximity
    for row,line in enumerate(matrix):
        for col,char in enumerate(line):
            if char == '*':
                # 1.: get all the digit locations in the proximity of the * character
                # 2.: get the corresponding complete number value for each digit from the hashmap
                # 3.: create set to get rid of duplicates, aka. the same number being detected multiple times
                # 4.: create list for ease of computation
                nums = list(set(map(lambda t: num_dict.get(t), get_digit_locations_in_proximity(matrix, row, col))))
                if len(nums) == 2: # exactly two numbers
                    sum_gear_ratios += nums[0][1] * nums[1][1]
    return sum_gear_ratios

    


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