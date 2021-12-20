class Value():
    def __init__(self, val):
        self.value = val

input_file = 'test.input'

def parse():

    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    return [translate(d) for d in data]

def translate(raw_str):
    l = []
    for s in raw_str:
        if s in '[,]':
            l.append(s)
        else:
            l.append(int(s))
    return l

def pprint(lang):
    print(''.join(map(str, lang)))

def scan(slist):
    changed = False
    counter = 0
    i = 0
    side = 'l'
    storage = []
    while i < len(slist):
        if changed:
            break
        symbol = slist[i]
        if symbol == '[':
            side = 'l'
            counter += 1
        elif symbol == ']':
            counter -= 1
        elif symbol == ',':
            side = 'r'
        else:
            if counter > 4:
                # need to explode
                if side == 'l':
                    storage.append({'l': symbol})
                if side == 'r':
                    storage[-1]['r'] = symbol
                    # explode left
                    j = i-4
                    while j > 0:
                        j -= 1
                        if isinstance(slist[j], int):
                            slist[j] += storage[-1]['l']
                            break
                    j = i+2
                    while j < (len(slist) - 1):
                        j += 1
                        if isinstance(slist[j], int):
                            slist[j] += storage[-1]['r']
                            break
                    i = i-3
                    slist[i] = 0
                    del slist[i+1:i+5]
                    counter -= 1
                    del storage[-1]
                    changed = True
            if symbol > 9:
                replacement = ['[', symbol//2, ',', (symbol+1)//2, ']']
                # need to split
                del slist[i]
                for r in reversed(replacement):
                    slist.insert(i, r)
                changed = True
        i += 1
    return changed

def add(str1, str2):
    return ['[', *str1, ',', *str2, ']']

def part_a():
    snails = parse()
    e = snails[0]
    for s in snails[1:]:
        e = add(e, s)
        changed = True
        while changed:
            changed = scan(e)
    
    pprint(e)

if __name__ == "__main__":
    part_a()