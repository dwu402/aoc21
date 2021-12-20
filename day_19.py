import numpy as np
from itertools import permutations, product, combinations
from collections import defaultdict, Counter
import networkx as nx

# input_file = 'test.input'
input_file = 'inputs/day_19.input'

def parse():
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    scanners = {}
    n = -99
    for ln in data:
        if ln.startswith('---'):
            n = int(ln[12:-4])
            scanners[n] = []
        elif len(ln) == 0:
            continue
        else:
            scanners[n].append(np.array([int(x) for x in ln.split(',')]))

    for s, v in scanners.items():
        scanners[s] = np.vstack(v)

    return scanners

def distance(b1, b2):
    # use the signature idea from u/jmpmpp
    return tuple(sorted(np.abs(b1 - b2)))

def construct_distance_map(scanners):
    """
    Outputs:
    {
        DISTANCE: {
            SCANNER_NUMBER: PAIR OF BEACONS
        }
    }
    """
    dmap = defaultdict(dict)

    for n,v in scanners.items():
        for ((i, bi), (j, bj)) in permutations(enumerate(v), 2):
            dmap[distance(bi, bj)][n] = tuple(sorted([i, j]))

    return dmap

def restrict_dmap(dmap, r1, r2):
    """
    Outputs:
    {
        DISTANCE: {
            SCANNER_NUMBER: PAIR OF BEACONS
        }
    }

    but only if SCANNER_NUMBER is R1 or R2
    """
    return {d: {n: vi for n, vi in v.items() if n in (r1, r2)} for d,v in dmap.items()}

def extract_common(dmap, r1, r2):
    """
    Outputs:
    {
        DISTANCE: {
            SCANNER_NUMBER: PAIR OF BEACONS
        }
    }

    if there is more than1 SCANNER_NUMBER for that distance, where SCANNER_NUMBER is restricted to R1 or R2
    """
    return {d: v for d,v in restrict_dmap(dmap, r1, r2).items() if len(v) > 1}

def map_common(dmap, r1, r2):
    """
    Outputs:
    [
        (BEACON_R1, BEACON_R2)
    ]
    in all combos that had commons (should only be one per)
    """
    commons = extract_common(dmap, r1, r2)
    cc = Counter([(ki, vi) for v in commons.values() for ki, vi in product(*v.values())])
    return [k for k,v in cc.items() if v > 1]

def get_pairwise_mappings(scanners):
    dmap = construct_distance_map(scanners)

    N = len(scanners)

    return {(i,j): map_common(dmap, i, j) for i,j in combinations(range(N), 2)}

zeros = [0,0,0]

def all_of_it():
    X = scanners = parse()
    pairwise_mappings = get_pairwise_mappings(scanners)
    # Compute Rotation and Translation (U) matrices between mappable scanners
    R = dict()
    U = dict()
    for (ki, kj), mps in pairwise_mappings.items():
        if len(mps) < 12:
            continue
        else:
            A, b = [], []
            for i, j in mps:
                xmotif = X[ki][i][0], X[ki][i][1], X[ki][i][2]
                row_slice = np.array([
                    [*xmotif, *zeros, *zeros, 1,0,0],
                    [*zeros, *xmotif, *zeros, 0,1,0],
                    [*zeros, *zeros, *xmotif, 0,0,1] 
                ])
                b_slice = np.array(X[kj][j]).reshape((3, 1))
                A.append(row_slice)
                b.append(b_slice)
            A = np.vstack(A)
            b = np.vstack(b)
            RU, *_ = np.linalg.lstsq(A, b, rcond=12)
            Ri = RU[:9].reshape((3, 3))
            Ui = RU[9:].reshape((3, 1))
            R[ki, kj] = Ri
            U[ki, kj] = Ui

    dep_G = nx.DiGraph()
    for (ki, kj) in R.keys():
        dep_G.add_edge(ki, kj, R=R[ki, kj], U=U[ki, kj], type=1) # forward: kj = R @ ki + U
        dep_G.add_edge(kj, ki, R=R[ki, kj].T, U=-U[ki, kj], type=-1) # backward: ki = R^T @ (kj - U)

    common_scanner = 0
    beacon_list = set()
    locs = dict()
    for s, coords in scanners.items():
        path = nx.shortest_path(dep_G, source=s, target=common_scanner)
        z = np.array([0,0,0]).reshape((3, 1)).astype(float)
        for p0, p1 in zip(path[:-1], path[1:]):
            if dep_G[p0][p1]['type'] == 1:
                coords = (dep_G[p0][p1]['R'] @ coords.T + dep_G[p0][p1]['U']).T
                z = dep_G[p0][p1]['R'] @ z + dep_G[p0][p1]['U']
            elif dep_G[p0][p1]['type'] == -1:
                coords = (dep_G[p0][p1]['R'] @ (coords.T + dep_G[p0][p1]['U'])).T
                z = dep_G[p0][p1]['R'] @ (z + dep_G[p0][p1]['U'])

        locs[s] = z
        beacon_list.update(map(tuple, np.round(coords).astype(int).tolist()))

    print(len(beacon_list))

    mhds = {(i,j): np.sum(np.abs(locs[i] - locs[j])) for i,j in combinations(range(len(scanners)), 2)}

    print(np.round(max(mhds.values())))

if __name__ == "__main__":
    all_of_it()