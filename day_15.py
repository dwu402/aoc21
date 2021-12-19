from itertools import product
from collections import defaultdict

import networkx as nx

# input_file = 'test.input'
input_file = 'inputs/day_15.input'

def parse(input_file):
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    nx = len(data)
    ny = len(data[0])
    R = [[int(x) for x in row.strip()] for row in data]

    return R, nx, ny

def part_a():
    R, NX, NY = parse(input_file)

    G = nx.DiGraph()
    for x in range(NX-1):
        for y in range(NY):
            G.add_edge((x,y), (x+1,y), weight=(R[x+1][y]))
            G.add_edge((x+1,y), (x,y), weight=(R[x][y]))
    for y in range(NY-1):
        for x in range(NX):
            G.add_edge((x,y), (x,y+1), weight=(R[x][y+1]))
            G.add_edge((x,y+1), (x,y), weight=(R[x][y]))

    return nx.single_source_dijkstra(G, source=(0,0), target=(NX-1,NY-1), weight='weight')

def cap(k, base=9):
    return base - ((base - k) % base)

def part_b():
    R, NX, NY = parse(input_file)

    K = 5

    G = nx.DiGraph()
    for x in range(K*NX-1):
        for y in range(K*NY):
            G.add_edge((x,y), (x+1,y), weight=cap(R[(x+1)%NX][y%NY] + ((x+1)//NX + y//NY)))
            G.add_edge((x+1,y), (x,y), weight=cap(R[x%NX][y%NY] + (x//NX + y//NY)))
    for y in range(K*NY-1):
        for x in range(K*NX):
            G.add_edge((x,y), (x,y+1), weight=cap(R[x%NX][(y+1)%NY] + (x//NX + (y+1)//NY)))
            G.add_edge((x,y+1), (x,y), weight=cap(R[x%NX][y%NY] + (x//NX + y//NY)))

    return nx.single_source_dijkstra(G, source=(0,0), target=(5*NX-1,5*NY-1), weight='weight')
    # return nx.single_source_dijkstra(G, source=(0,0), target=(0,NY), weight='weight')

def pprint(dist, path):
    nx = path[-1][0] + 1
    ny = path[-1][1] + 1
    A = [['.' for _ in range(ny)] for _ in range(nx)]
    for x,y in path:
        A[x][y] = 'O'
    for row in A:
        print(''.join(row))
    print('')
    print(dist)
    print('')

def dprint(dist, path):
    print(dist)

if __name__ == "__main__":
    pprint(*part_a())
    # dprint(*part_b())