import numpy as np
from itertools import product
from collections import deque
from sortedcontainers import SortedSet

# input_file = 'test.input'
input_file = 'inputs/day_22.input'

onehot = {
    'on': 1,
    'off': 0,
}
def parse(ipfl=input_file):
    with open(ipfl, 'r') as fp:
        data = fp.read().strip().split('\n')

    commands = []
    for ln in data:
        action, region = ln.split(' ')
        xs, ys, zs = map(lambda s: s[2:], region.split(','))
        x0, x1 = map(int, xs.split('..'))
        y0, y1 = map(int, ys.split('..'))
        z0, z1 = map(int, zs.split('..'))
        commands.append((onehot[action], x0, x1, y0, y1, z0, z1))

    return commands

def part_a():
    A = np.zeros((101, 101, 101), dtype=int)
    def coord(x, y, z):
        return x+50, y+50, z+50

    commands = parse()
    for command in commands:
        ac, x0, x1, y0, y1, z0, z1 = command
        A[x0+50:x1+51, y0+50:y1+51, z0+50:z1+51] = ac
        # print(np.sum(A))

    return np.sum(A)

class Box():

    def __init__(self, on, *loc):
        self.value = on
        self.x0, self.y0, self.z0 = loc[::2]
        self.x1, self.y1, self.z1 = loc[1::2]

    def __repr__(self):
        return f'Box({self.value}, {self.x0}, {self.x1}, {self.y0}, {self.y1}, {self.z0}, {self.z1})'

    @property
    def volume(self):
        return (self.x1 - self.x0 + 1) * (self.y1 - self.y0 + 1) * (self.z1 - self.z0 + 1) * self.value

    def intersects(self, other):
        mx0 = max(self.x0, other.x0)
        mx1 = min(self.x1, other.x1)

        my0 = max(self.y0, other.y0)
        my1 = min(self.y1, other.y1)

        mz0 = max(self.z0, other.z0)
        mz1 = min(self.z1, other.z1)

        if mx0 <= mx1 and my0 <= my1 and mz0 <= mz1:
            intersection_value = -self.value
            intersection_box = Box(intersection_value, mx0, mx1, my0, my1, mz0, mz1)
            return intersection_box

def total_volume(boxes):
    return sum((x.volume for x in boxes))

def resolve(commands):
    boxes = []
    for command in commands:
        new_box = Box(*command)
        ibxs = []
        for box in boxes:
            ibox = box.intersects(new_box)
            if ibox is not None:
                ibxs.append(ibox)
        boxes.extend(ibxs)
        if command[0] == 1:
            boxes.append(new_box)

        # print(total_volume(boxes))

    return boxes

def part_b():
    commands = parse()
    boxes = resolve(commands)
    return total_volume(boxes)

if __name__ == "__main__":
    # import time
    # tic = time.perf_counter()
    # print(part_a())
    # toc = time.perf_counter()
    # print('----')
    # print(toc-tic)
    # print('----')
    print(part_b())
    # print('----')
    # print(time.perf_counter() - toc)