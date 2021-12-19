from itertools import permutations
from collections import Counter, defaultdict

input_file = "inputs/day_8.input"

ALL = 'ABCDEFG'

segment_count_map = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8]
}

excludes = {
    0: 'D',
    1: 'ABDEG',
    2: 'BF',
    3: 'BE',
    4: 'AEG',
    5: 'CE',
    6: 'C',
    7: 'BDEG',
    8: '',
    9: 'E',
}

def invert_str(allstr, part):
    cpy = str(allstr)
    for p in part:
        cpy = cpy.replace(p, '')
    return cpy

seg_map = {invert_str(ALL, v): k for k,v in excludes.items()}

def parse(input_file):
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    inputs_raw, outputs_raw = zip(*(x.split('|') for x in data))

    inputs = list(x.strip().split() for x in inputs_raw)
    outputs = list(x.strip().split() for x in outputs_raw)

    return inputs, outputs
    
def part_a():
    inputs, outputs = parse(input_file)

    accum_1478 = 0
    for output in outputs:
        for val in output:
            if len(segment_count_map[len(val)]) == 1:
                accum_1478 += 1
    print(accum_1478)

def remove_excludes(possible, xput):
    for val in xput:
        possible_values = segment_count_map[len(val)]
        if len(possible_values) == 1:
            for ex in excludes[possible_values[0]]:
                for letter in val:
                    possible[ex] = possible[ex].replace(letter, '')

def elim(possible, keys):
    for k, v in possible.items():
        if k not in keys:
            for e in possible[keys[0]]:
                possible[k] = v.replace(e, '')

def normalise(string):
    return ''.join(sorted(string.upper()))

def add_map(basemap, xputs):
    for xput in xputs:
        updv = segment_count_map[len(xput)]
        for u in updv:
            basemap[u].add(normalise(xput))

def strdiff(a, b):
    if len(b) > len(a):
        a, b = b, a
    
    for i in b:
        a = a.replace(i, '')

    return a

def strcommon(*args):
    ss = map(set, args)

    s0 = set(ALL)
    for s in ss:
        s0 = s0.intersection(s)

    return normalise(''.join(s0))

def part_b():
    inputs, outputs = parse(input_file)

    oval = 0
    for iput, oput in zip(inputs, outputs):
        nmap = defaultdict(set)
        add_map(nmap, iput)
        add_map(nmap, oput)

        for k,v in nmap.items():
            if len(v) == 1:
                nmap[k] = v.pop()

        smap = {'A': strdiff(nmap[7], nmap[1])}

        ADG = strcommon(*nmap[3])

        nmap[3] = normalise(nmap[1] + ADG)

        nmap[2].remove(nmap[3])
        nmap[5].remove(nmap[3])

        smap['G'] = strdiff(nmap[3], normalise(smap['A'] + nmap[4]))
        smap['D'] = strdiff(strdiff(ADG, smap['A']), smap['G'])

        nmap[0] = {len(strdiff(i, ADG)):i for i in nmap[0]}[4]
        nmap[6].remove(nmap[0])
        nmap[9].remove(nmap[0])

        nmap[5] = strcommon(*nmap[6])
        nmap[2].remove(nmap[5])
        nmap[2] = nmap[2].pop()

        nmap[9] = [k for k in nmap[9] if strcommon(nmap[3], k) == nmap[3]][0]
        nmap[6].remove(nmap[9])
        nmap[6] = nmap[6].pop()

        rmap = {v:k for k,v in nmap.items()}

        ovals = [rmap[normalise(o)] for o in oput]

        oval += sum(10**i * x for i,x in enumerate(reversed(ovals)))

    return oval
444444


if __name__ == '__main__':
    # part_a()
    print(part_b())
    pass 