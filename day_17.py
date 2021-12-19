import re
from numpy import isfinite

# input_file = 'test.input'
input_file = 'inputs/day_17.input'

target_re = re.compile(r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)')

def parse():
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')[0]

    x0, x1, y0, y1 = (int(z) for z in target_re.match(data).groups())

    return x0, x1, y0, y1

def a_step(x, y, u, v):
    sign_u = -1 if u < 0 else (1 if u > 0 else 0)
    return x+u, y+v, u - sign_u, v-1

def a_sim(u0, v0, x0, x1, y0, y1, verbose=False):
    x, y = 0, 0
    u, v = u0, v0
    if verbose:
        print(x, y, u, v)
    max_y = 0
    while y > min(y0, y1):
        x, y, u, v = a_step(x, y, u, v)
        if verbose:
            print(x, y, u, v)
        if max_y < y:
            max_y = y
        if (x0 <= x <= x1) and (y0 <= y <= y1):
            return max_y
    return -float('Inf')

def part_a():
    x0, x1, y0, y1 = parse()

    u0s = [20, 21]
    # it looks like the y landing area is around -(v0 + 1)
    print(a_sim(20, 88, x0, x1, y0, y1))


def part_b():
    x0, x1, y0, y1 = parse()

    recs = set()
    ZZZ = 100
    for u0 in range(0, min(x0, x1)):
        for v0 in range(max(y0, y1), ZZZ):
            highest = a_sim(u0, v0, x0, x1, y0, y1)
            if isfinite(a_sim(u0, v0, x0, x1, y0, y1)):
                recs.add((u0, v0))
    # print(recs)
    for u0 in range(x0, x1+1):
        for v0 in range(y0, y1+1):
            recs.add((u0, v0))
    from matplotlib import pyplot as plt

    plt.plot(*zip(*recs), 'o')
    plt.show()
    return len(recs)

if __name__ == "__main__":
    print(part_a())
    print(part_b())