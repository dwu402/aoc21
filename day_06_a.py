input_file = 'inputs/day_6.input'

def next_day(state):
    new_dict = {v: 0 for v in range(9)}
    for k,v in state.items():
        if k == 0:
            new_dict[6] += v
            new_dict[8] += v
        else:
            new_dict[k-1] += v
    return new_dict

def read(fn):
    with open(fn, 'r') as fp:
        data = fp.read().strip().split(',')
    return [int(x) for x in data]

def build_state_dict(state):
    s_dict = {v: 0 for v in range(9)}
    for s in state:
        s_dict[s] += 1
    return s_dict

def total_fish(d):
    return sum(d.values())

if __name__ == '__main__':
    n = 80
    state = read(input_file)
    state_dict = build_state_dict(state)

    for i in range(n):
        state_dict = next_day(state_dict)
        # print(i+1, ':', state_dict)

    print(total_fish(state_dict))