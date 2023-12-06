from typer import Typer

app = Typer()

digit_dictionary = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'zero': '0'
}

def solution(input: str) -> int:
    sum = 0
    for line in input.split('\n'):
        first = None
        last = None
        for i,c in enumerate(line):
            # check if line[i] is digit... aka 0,1,2,...
            if c.isdigit():
                if not first:
                    first = c
                last = c
            # loop through all written out digits...
            for ds,d in digit_dictionary.items():
                # ... and check if the line from i to end starts with the digit
                if line[i:].startswith(ds):
                    if not first:
                        first = d
                    last = d
        # combine both digits
        sum += int(first + last)
    return sum

def run_with_input_file(input_file_path: str) -> None:
    with open(input_file_path, 'r') as file:
        input = file.read()
    print(solution(input))

@app.command()
def run_stage1_sample():
    run_with_input_file('res/stage1_sample.txt')

@app.command()
def run_stage2_sample():
    run_with_input_file('res/stage2_sample.txt')

@app.command()
def run_stage1_challenge():
    run_with_input_file('res/stage1_challenge.txt')

@app.command()
def run_stage2_challenge():
    run_with_input_file('res/stage2_challenge.txt')

@app.command()
def run_custom(file_path: str):
    run_with_input_file(file_path)

if __name__ == '__main__':
    app()