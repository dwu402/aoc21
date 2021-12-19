from collections import Counter, defaultdict

# input_file = 'test.input'
input_file = 'inputs/day_14.input'

def parse_a():
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    chain = data[0]
    rules = dict()
    for rule in data[2:]:
        a, b = rule.split(' -> ')
        c = a[0] + b
        rules[a] = c


    return chain, rules

def part_a():
    chain, rules = parse_a()
    # print(rules)

    Niters = 10
    for _ in range(Niters):
        new_chain = ''.join(rules.get(x+y, x) for x, y in zip(chain[:-1], chain[1:])) + chain[-1]
        # print(len(new_chain))
        chain = new_chain

    c = Counter(chain).most_common()
    # print(c[0], c[-1])
    return c[0][1] - c[-1][1]


def parse_b():
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    chain = data[0]
    pairs = defaultdict(int)
    for x, y in zip(chain[:-1], chain[1:]):
        pairs[x+y] += 1
    final = chain[-1]

    rules = dict()
    for rule in data[2:]:
        a, b = rule.split(' -> ')
        c1 = a[0] + b
        c2 = b + a[1]
        rules[a] = (c1, c2)

    return pairs, final, rules

def part_b():
    pairs, final, rules = parse_b()

    print(pairs)
    Niters = 40
    for _ in range(Niters):
        update = defaultdict(int)
        for k, v in pairs.items():
            pairs[k] -= v
            for x in rules.get(k, [k]):
                update[x] += v
        for k, v in update.items():
            pairs[k] += v

    counts = Counter(final)
    for pair, value in pairs.items():
        counts[pair[0]] += value
    mc = counts.most_common()
    return mc[0][1] - mc[-1][1]

if __name__ == "__main__":
    # print(part_a())
    print(part_b())