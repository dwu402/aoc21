from numpy import product

input_file = 'inputs/day_9.input'
# input_file = 'test.input'

def parse(input_file):
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')
    
    NX = len(data)
    NY = len(data[0])
    H = [[int(x) for x in d] for d in data]
    return NX, NY, H

def get_lows(NX, NY, H):
    lows = []
    for i, ROW in enumerate(H):
        for j, x in enumerate(ROW):
            if i != 0 and H[i-1][j] <= x:
                continue
            if i != (NX - 1) and H[i+1][j] <= x:
                continue
            if j != 0 and H[i][j-1] <= x:
                continue
            if j != (NY - 1) and H[i][j+1] <= x:
                continue
            lows.append((i,j,x))
    return lows

def part_a():
    NX, NY, H = parse(input_file)
    lows = get_lows(NX, NY, H)
    risk = sum((1+x[2]) for x in lows)
    print(risk)

def explore(i, j, x, NX, NY, H):
    cands = [(i, j, x)]
    basin = set()
    while len(cands) > 0:
        ii, jj, xx = cands.pop()
        # stop at 9s
        if xx == 9:
            continue
        # add to basin
        basin.add((ii, jj, xx))
        # check edges
        if ii != 0 and H[ii-1][jj] > xx:
            cands.append((ii-1, jj, H[ii-1][jj]))
        if ii != (NX - 1) and H[ii+1][jj] > xx:
            cands.append((ii+1, jj, H[ii+1][jj]))
        if jj != 0 and H[ii][jj-1] > xx:
            cands.append((ii, jj-1, H[ii][jj-1]))
        if jj != (NY - 1) and H[ii][jj+1] > xx:
            cands.append((ii, jj+1, H[ii][jj+1]))

    return len(basin)

def part_b():
    NX, NY, H = parse(input_file)
    lows = get_lows(NX, NY, H)

    basins = []
    for low in lows:
        size = explore(*low, NX, NY, H)
        basins.append(size)

    return product(sorted(basins)[-3:])

if __name__ == "__main__":
    print(part_b())