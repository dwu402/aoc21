input_file = 'test.input'
# input_file = 'inputs/day_00.input'

def parse(datafile=input_file):
    with open(datafile, 'r') as fp:
        data = fp.read().strip().split('\n')

    return data

def part_a():
    pass

def part_b():
    pass

if __name__ == "__main__":
    print(part_a())
    print(part_b())