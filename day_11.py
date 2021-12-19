from itertools import product
from collections import deque
# input_file = 'test.input'
input_file = 'inputs/day_11.input'

def parse(input_file):
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')
    L = [[int(x) for x in r] for r in data]

    return L

def neighbours(x, NX, NY):
    i,j = x
    dirs = product([-1, 0, 1], [-1, 0, 1])
    neighbours = []
    for d in dirs:
        ii = i + d[0]
        jj = j + d[1]
        if ii == i and jj == j:
            continue
        if ii < 0 or ii >= NX:
            continue
        if jj < 0 or  jj >= NY: 
            continue
        neighbours.append((ii, jj))

    return neighbours

def sexyprint(L):
    for ln in L:
        print(*ln, sep='')

def part_a():
    L = parse(input_file)

    NX = len(L)
    NY = len(L[0])

    N = 100

    nf = 0
    for n in range(N):
        flashers = set()
        for i in range(NX):
            for j in range(NY):
                L[i][j] = L[i][j] + 1
        searchlist = deque(product(range(NX), range(NY)))
        while len(searchlist) > 0:
            i, j = searchlist.pop()
            if L[i][j] > 9 and (i,j) not in flashers:
                flashers.add((i,j))
                ngs = neighbours((i,j), NX, NY)
                for ni, nj in ngs:
                    L[ni][nj] = L[ni][nj] + 1
                searchlist.extend(ngs)
        nf += len(flashers)
        # print(nf)
        for fi, fj in flashers:
            L[fi][fj] = 0
        # sexyprint(L)
    return nf

def part_b():
    L = parse(input_file)

    NX = len(L)
    NY = len(L[0])

    N = 0
    while True:
        flashers = set()
        for i in range(NX):
            for j in range(NY):
                L[i][j] = L[i][j] + 1
        searchlist = deque(product(range(NX), range(NY)))
        while len(searchlist) > 0:
            i, j = searchlist.pop()
            if L[i][j] > 9 and (i,j) not in flashers:
                flashers.add((i,j))
                ngs = neighbours((i,j), NX, NY)
                for ni, nj in ngs:
                    L[ni][nj] = L[ni][nj] + 1
                searchlist.extend(ngs)
        N += 1
        if len(flashers) == NX*NY:
            return N
        for fi, fj in flashers:
            L[fi][fj] = 0

if __name__ == "__main__":
    print(part_a())
    print(part_b())