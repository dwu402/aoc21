from collections import deque

def parse(filename='test.input'):
    with open(filename, 'r') as fp:
        data = fp.read().strip().split('\n')
    
    return data

def explode(num):
    return map(int, str(num))

def build_alu(data):
    as_ = [int(x[6:]) for x in data[4::18]]
    bs_ = [int(x[6:]) for x in data[5::18]]
    cs_ = [int(x[6:]) for x in data[15::18]]

    stack = deque()
    pairs = []
    for i, (a, b, c) in enumerate(zip(as_, bs_, cs_)):
        if a == 1:
            stack.append((i, c))
        else:
            z = stack.pop()
            pairs.append([z, (i, b)])
    return pairs

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def solve(pairs, order=max):
    ns = [0] * 14
    for (i, a), (j, b) in pairs:
        c = a+b
        assert i < j
        m = order([n for n in nums if (n+c > 0) and (n+c < 10)])
        ns[i] = m
        ns[j] = m+c
    return ''.join(map(str, ns))

def part_a():
    data = parse('inputs/day_24.input')
    pairs = build_alu(data)
    return solve(pairs, max)

def part_b():
    data = parse('inputs/day_24.input')
    pairs = build_alu(data)
    return solve(pairs, min)

if __name__ == '__main__':
    print(part_a())
    print(part_b())