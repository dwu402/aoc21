from itertools import product
from functools import lru_cache
from collections import Counter

# input_file = 'test.input'
input_file = 'inputs/day_21.input'

def parse():
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    p_1 = int(data[0][-2:])
    p_2 = int(data[1][-2:])

    return p_1, p_2

def deterministic_die():
    i = 1
    while True:
        yield i, i+1, i+2
        i += 3

def part_a():
    p_1, p_2 = parse()
    # print(p_1, p_2)
    s_1, s_2 = 0, 0
    winner = 0
    rolls = iter(deterministic_die())
    n = 0
    while True:
        p_1 = (p_1 + sum(next(rolls)) - 1) % 10 + 1
        s_1 += p_1
        n += 3
        if s_1 >= 1000:
            winner = 1
            break
        # print(p_1, s_1)
        p_2 = (p_2 + sum(next(rolls)) - 1) % 10 + 1
        s_2 += p_2
        n += 3
        if s_2 >= 1000:
            winner = 2
            break
        # print(p_1, s_1)
    print(n, s_1, s_2)
    return ((2 - winner) * s_2 + (winner - 1) * s_1) * n

@lru_cache(None)
def rollz(n):
    """ Returns an iterable of (r, n) 
    where r is the sum of rolls, 
    and n is the number of times that happens
    """
    rs = product(range(1, n+1), repeat=3)
    return Counter(map(sum, rs)).items()

@lru_cache(None)
def play(p1, p2, s1=0, s2=0):
    # s2 is the last player that rolled, check if they won
    if s2 >= 21:
        return 0, 1
    w1, w2 = 0, 0
    # iterate over all combinations of quantum rolls
    for roll, n in rollz(3):
        # use of or to go 0 -> 10
        p = (p1 + roll) % 10 or 10
        # next player
        v2, v1 = play(p2, p, s2, s1+p)
        # add wins
        w1, w2 = w1 + v1*n, w2 + v2*n
    # return wins
    return w1, w2

def part_b():
    p = parse()
    w = play(*p)
    return w

if __name__ == "__main__":
    print(part_a())
    print(part_b())