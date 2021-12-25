def parse(ifn):
    with open(ifn, 'r') as fp:
        data = fp.read().strip().split('\n')

    return [[i for i in x] for x in data], len(data), len(data[0])

unlock = {
    '.': '.',
    'v': 'v',
    '>': '>',
    'E': '>',
    'S': 'v',
    'Z': '.'
}

def nextstate(state, m, n):
    moves = 0
    for ridx in range(m):
        # EAST
        for j in range(n):
            jnext = (j+1)%n
            if state[ridx][j] == '>' and state[ridx][jnext] == '.':
                # moves.append([(row, j), (row, jnext)])
                state[ridx][jnext] = 'E'
                state[ridx][j] = 'Z'
                moves += 1
    for i, row in enumerate(state):
        for j, val in enumerate(row):
            state[i][j] = unlock[val]
    for ridx in range(m):
        # SOUTH
        rprev = (ridx-1)%m
        for i, (z, q) in enumerate(zip(state[rprev], state[ridx])):
            if z == 'v' and q == '.':
                state[rprev][i] = 'Z'
                state[ridx][i] = 'S'
                moves += 1
    for i, row in enumerate(state):
        for j, val in enumerate(row):
            state[i][j] = unlock[val]
    return moves

def pprint(A):
    for row in A:
        print(''.join(row))

def part_a():
    A, *sz = parse('inputs/day_25.input')
    moves = -1
    i = 0
    while moves != 0:
        moves = nextstate(A, *sz)
        i += 1
        # if i % 5 == 0 or i < 5:
        #     print(f'step {i}')
        #     pprint(A)
    return i

if __name__ == "__main__":
    print(part_a())