from collections import deque
# input_file = 'test.input'
input_file = 'inputs/day_10.input'

def parse(input_file):
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    return data

a_points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

matches = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

def part_a():
    data = parse(input_file)

    pnts = 0
    for line in data:
        queue = deque()
        for char in line:
            if char in matches:
                queue.append(matches[char])
            elif char != queue[-1]:
                pnts += a_points[char]
                # print('Expected', queue[-1], 'got', char)
                break
            else:
                queue.pop()
    return pnts

b_points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def part_b():
    data = parse(input_file)

    pnts = []
    for line in data:
        queue = deque()
        for char in line:
            if char in matches:
                queue.append(matches[char])
            elif char != queue[-1]:
                queue.clear()
                break
            else:
                queue.pop()
        if len(queue) > 0:
            pnt = 0
            for char in reversed(queue):
                pnt *= 5
                pnt += b_points[char]
            pnts.append(pnt)
    N = len(pnts)
    return sorted(pnts)[N//2]

if __name__ == "__main__":
    print(part_a())
    print(part_b())