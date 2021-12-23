import functools
from collections import deque
from sortedcontainers import SortedKeyList

# input_file = 'test.input'
input_file = 'inputs/day_23.input'

def parse(datafile=input_file):
    with open(datafile, 'r') as fp:
        data = fp.read().strip().split('\n')

    return list(zip(*[x[3:10:2] for x in data[2:4]]))

# room -> loc -> hall
dist_rh_base = [
    [3, 2, 2, 4, 6, 8, 9],
    [5, 4, 2, 2, 4, 6, 7],
    [7, 6, 4, 2, 2, 4, 5],
    [9, 8, 6, 4, 2, 2, 3],
]

dist_rh = [[[x+loc for x in rm] for loc in range(4)] for rm in dist_rh_base]

# hall -> room -> loc
dist_hr = [[[dist_rh[room][loc][hall] for loc in range(4)] for room in range(4)] for hall in range(7)]

dist_rr_base = [
    [0, 4, 6, 8],
    [4, 0, 4, 6],
    [6, 4, 0, 4],
    [8, 6, 4, 0]
]

dist_rr = [[[[x+loc+oloc for oloc in range(4)] for x in r0] for loc in range(4)] for r0 in dist_rr_base]

hall_left = [
    [1, 0],
    [2, 1, 0],
    [3, 2, 1, 0],
    [4, 3, 2, 1, 0],
]

hall_right = [
    [2, 3, 4, 5, 6],
    [3, 4, 5, 6],
    [4, 5, 6],
    [5, 6],
]

belongs = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
}

cost_factor = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

def conform_config(config):
    """ Convert data from input to state """
    return (None, None, None, None, None, None, None), tuple(config)

def make_state(halls, rooms, mover, from_room=None, from_hall=None, to_room=None, to_hall=None, from_room_loc=None, to_room_loc=None):
    """ Constructs a new state given transition information """
    new_halls = list(halls)
    new_rooms = list(list(x) for x in rooms)

    if from_room is not None: new_rooms[from_room][from_room_loc] = None
    if from_hall is not None: new_halls[from_hall] = None
    if to_room is not None: new_rooms[to_room][to_room_loc] = mover
    if to_hall is not None: new_halls[to_hall] = mover

    return tuple(new_halls), tuple(tuple(x) for x in new_rooms)

def finished(state):
    """ Determines if a state is finished """
    halls, rooms = state
    if any(halls):
        return False
    for s, r in zip('ABCD', rooms):
        if any(x != s for x in r):
            return False

    return True

room_index = {
    0: 1.5,
    1: 2.5,
    2: 3.5,
    3: 4.5,
}
def is_legal(halls, hall, room):
    """ Determines if a hall -> room or room -> hall move is legal """
    ridx = room_index[room]
    if hall < ridx: # moving to right
        return all(x is None for x in halls[hall+1:int(ridx+1)])
    else:
        return all(x is None for x in halls[int(ridx+1):hall])

def is_rr_legal(halls, room1, room2):
    """ Determines if a room -> room move is legal (via halls) """
    ridx1, ridx2 = sorted([room_index[room1], room_index[room2]])
    return all(x is None for x in halls[int(ridx1+1):int(ridx2+1)])

def available(room, species):
    """ Returns the index of the deepest empty space in a partially solved room """
    i = len(room)
    for r in reversed(room):
        i -= 1
        if r is None:
            return i
        if r != species:
            return -1
    return -1

def top(room):
    """ Returns the topmost non-empty value in a room """
    for i, r in enumerate(room):
        if r is not None:
            return i
    return -1

def auto_moves(state):
    """ Returns a move that is automatically optimal (puts a value in the correct room) """
    halls, rooms = state
    # iterate hall species in cost order
    for species in 'DCBA':
        ri = belongs[species]
        sroom = rooms[belongs[species]]
        # find if target room is empty
        loc = available(sroom, species)
        if loc < 0:
            continue
        for i, s in enumerate(halls):
            # if we can move the thing in the hall to the room
            if s == species and is_legal(halls, i, ri):
                return (make_state(halls, rooms, species, from_hall=i, to_room=ri, to_room_loc=loc), dist_hr[i][ri][loc] * cost_factor[species])
    for ri, room in enumerate(rooms):
        # if room is solved, do nothing
        if all((s is None) or (belongs[s] == ri) for s in room):
            continue
        for i, s in enumerate(room):
            if s is not None:
                targ_room = belongs[s]
                # check if it can move to target room
                loc = available(rooms[targ_room], s)
                if loc >= 0 and is_rr_legal(halls, ri, targ_room):
                    return (make_state(halls, rooms, s, from_room=ri, to_room=targ_room, from_room_loc=i, to_room_loc=loc), dist_rr[ri][i][targ_room][loc] * cost_factor[s])
                break

def backup_moves(state):
    """ Generator of all room -> hall moves that are legal """
    halls, rooms = state
    for i, room in enumerate(rooms):
        # if room contains all members or empty cells
        if all(x is None or belongs[x] == i for x in room):
            continue
        # else has someone to move
        tidx = top(room)
        topper = room[tidx]
        for hdir in [hall_left, hall_right]:
            for hi in hdir[i]:
                if halls[hi] is None:
                    yield make_state(halls, rooms, topper, from_room=i, to_hall=hi, from_room_loc=tidx), dist_rh[i][tidx][hi] * cost_factor[topper]
                else:
                    break

class DictWatch(dict):
    def __init__(self, *args, **kwargs):
        self._hits = 0
        self.update(*args, **kwargs)

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        self._hits += 1
        return val

    @property
    def hits(self):
        return self._hits

    def recount(self):
        self._hits = 0

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)
        
    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

DP = DictWatch()
PATH = {}
def cost_of_this(state):
    """ Recursively computes cost of getting a state to finished """
    if finished(state):
        return 0
    if state in DP:
        return DP[state]
    amv = auto_moves(state)
    if amv:
        z = amv[1] + cost_of_this(amv[0])
        DP[state] = z
        PATH[state] = amv
        return z
    zs = {s: (c, cost_of_this(s)) for s, c in backup_moves(state)}
    kek, z, kekc = None, float('Inf'), 0
    for ns, (c, cc) in zs.items():
        zn = c + cc
        if zn < z:
            kek = ns
            z = zn
            kekc = c
    PATH[state] = kek, kekc
    DP[state] = z
    return z

def part_a():
    config = parse()
    IC = conform_config(config)

    cost = cost_of_this(IC)
    nd = IC
    print(IC)
    while nd in PATH:
        nd, c = PATH[nd]
        print(nd, c)

    print('----  ', DP.hits, '  ----')
    DP.recount()

    return cost

def conform_deep_config(config):
    halls, rooms = conform_config(config)
    extra = [('D', 'D'), ('C', 'B'), ('B', 'A'), ('A', 'C')]
    return halls, tuple((r0, *x, r1) for (r0, r1), x in zip(rooms, extra))

def part_b():
    config = parse()
    IC = conform_deep_config(config)

    cost = cost_of_this(IC)
    nd = IC
    print(IC)
    while nd in PATH:
        nd, c = PATH[nd]
        print(nd, c)


    print('----  ', DP.hits, '  ----')
    DP.recount()

    return cost

if __name__ == "__main__":
    print(part_a())
    print(part_b())