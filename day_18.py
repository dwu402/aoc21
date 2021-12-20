
# yanked from https://github.com/Gravitar64/Advent-of-Code-2021/blob/main/Tag_18.py
from itertools import permutations

# input_file = 'test.input'
input_file = 'inputs/day_18.input'

def parse():
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    return data

def make_line(d):
    line = []
    depth = 0
    for c in d:
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
        elif c.isdigit():
            line.append([int(c), depth])
    return line

def explode(x):
    for i, ((n1, d1), (n2, d2)) in enumerate(zip(x[:-1], x[1:])):
        # if not deep or not a 'pair' with next
        if d1 < 5 or d1 != d2:
            continue
        # is deep, is pair, is not first / has left neighbour
        if i > 0:
            x[i-1][0] += n1
        # is deep, is pair, next is not last/has right neighbour
        if i+1 < len(x) - 1:
            x[i+2][0] += n2
        # changed, and updated list (replace x[i] and x[i+1] with a 0)
        return True, x[:i] + [[0, d1-1]] + x[i+2:]
    return False, x

def split(x):
    for i, (n, d) in enumerate(x):
        if n < 10:
            continue
        return True, x[:i] + [[n//2, d+1], [(n+1)//2, d+1]] + x[i+1:]
    return False, x

def add(a, b):
    x = [[n, d+1] for n, d in a + b]
    while True:
        changed, x = explode(x)
        if changed:
            continue
        changed, x = split(x)
        if not changed:
            break
    return x

def magnitude(x):
    while len(x) > 1:
        for i, ((n1, d1), (n2, d2)) in enumerate(zip(x[:-1], x[1:])):
            if d1 != d2:
                continue # not a pair
            mag = n1 * 3 + n2 * 2
            x = x[:i] + [[mag, d1-1]] + x[i+2:]
            break

    return x[0][0]

def part_a():
    data = parse()
    lines = [make_line(d) for d in data]
    x = lines[0]
    for l in lines[1:]:
        x = add(x, l)
    return magnitude(x)

def part_b():
    data = parse()
    lines = [make_line(d) for d in data]
    return max(magnitude(add(li, lj)) for li, lj in permutations(lines, 2))


if __name__ == '__main__':
    print(part_a())