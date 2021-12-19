# input_file = 'test.input'
input_file = 'inputs/day_13.input'

class Instruction():
    def __init__(self, direction, value):
        self.direction = direction
        self.value = value

    def __repr__(self):
        return f"Instruction({repr(self.direction)}, {repr(self.value)})"

def parse(input_file):
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    dots = set()
    instructions = []
    for ln in data:
        if ln == '':
            continue
        elif not ln.startswith('fold'):
            coord = tuple(int(x.strip()) for x in ln.split(','))
            dots.add(coord)
        else:
            direction = ln[11]
            value = int(ln[13:])
            instructions.append(Instruction(direction, value))
    return dots, instructions

def pprint(dots):
    nx = max(d[0] for d in dots) + 1
    ny = max(d[1] for d in dots) + 1
    A = [['.' for _ in range(nx)] for _ in range(ny)]
    for x,y in dots:
        A[y][x] = '#'
    for row in A:
        print(''.join(row))
    print('')


def part_a():
    dots, instructions = parse(input_file)
    # pprint(dots)
    instruction = instructions[0]

    temp = set()
    if instruction.direction == 'y':
        for dot in dots:
            if dot[1] > instruction.value:
                temp.add(dot)
        for dot in temp:
            x, y = dot
            dots.remove(dot)
            dots.add((x, 2*instruction.value - y))
    elif instruction.direction == 'x':
        for dot in dots:
            if dot[0] > instruction.value:
                temp.add(dot)
        for dot in temp:
            x, y = dot
            dots.remove(dot)
            dots.add((2*instruction.value - x, y))

    # pprint(dots)
    return len(dots)

def part_b():
    dots, instructions = parse(input_file)
    # pprint(dots)
    for instruction in instructions:
        temp = set()
        if instruction.direction == 'y':
            for dot in dots:
                if dot[1] > instruction.value:
                    temp.add(dot)
            for dot in temp:
                x, y = dot
                dots.remove(dot)
                dots.add((x, 2*instruction.value - y))
        elif instruction.direction == 'x':
            for dot in dots:
                if dot[0] > instruction.value:
                    temp.add(dot)
            for dot in temp:
                x, y = dot
                dots.remove(dot)
                dots.add((2*instruction.value - x, y))

    pprint(dots)

if __name__ == '__main__':
    print(part_a())
    part_b()