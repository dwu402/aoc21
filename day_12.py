import networkx as nx
from collections import deque
import string

# input_file = 'test3.input'
input_file = 'inputs/day_12.input'

def parse(input_file):
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    G = nx.Graph()
    for ln in data:
        x, y = ln.split('-')
        G.add_edge(x, y)

    return G

class Path():
    def __init__(self):
        self._path = ['start']
        self.rep = None

    def copy(self):
        p = Path()
        p._path = list(self._path)
        p.rep = self.rep
        return p

    def add(self, nd, copy=False):
        targ = self
        if copy:
            targ = self.copy()
        targ._path.append(nd)

        return targ

    def __getitem__(self, i):
        return self._path[i]

    def __str__(self):
        return ','.join(self._path)

    def __lt__(self, other):
        return self._path < other._path

def part_a():
    G = parse(input_file)

    srch = deque([Path()])
    paths = []
    while len(srch) > 0:
        cand = srch.pop()
        nbs = G[cand[-1]]
        for nb in nbs:
            if nb == 'end':
                path = cand.add('end', copy=True)
                paths.append(path)
            elif nb[0] in string.ascii_uppercase:
                also = cand.add(nb, copy=True)
                srch.append(also)
            elif nb not in cand:
                also = cand.add(nb, copy=True)
                srch.append(also)
    return len(paths)

def part_b():
    G = parse(input_file)

    srch = deque([Path()])
    paths = []
    while len(srch) > 0:
        cand = srch.pop()
        nbs = G[cand[-1]]
        for nb in nbs:
            if nb == 'end':
                path = cand.add('end', copy=True)
                paths.append(path)
            elif nb[0] in string.ascii_uppercase:
                also = cand.add(nb, copy=True)
                srch.append(also)
            elif nb not in cand:
                also = cand.add(nb, copy=True)
                srch.append(also)
            elif cand.rep is None and nb != 'start':
                also = cand.add(nb, copy=True)
                also.rep = nb
                srch.append(also)
    # for p in sorted(paths):
    #     print(str(p))
    return len(paths)

if __name__ == '__main__':
    print(part_a())
    print(part_b())