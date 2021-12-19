input_file = "inputs/day_2.input"

def add_pos(pos, scale, diff):
    new_pos = []
    for p, d in zip(pos, diff):
        new_pos.append(p + scale * d)
    return new_pos

command_map = {
    'forward': (1, 0),
    'down': (0, 1),
    'up': (0, -1),
}

def resolve_position(commands):
    pos = [0, 0]
    for command in commands:
        dir, scale_str = command.split(' ')
        scale = int(scale_str)
        pos = add_pos(pos, scale, command_map[dir])
    return pos

if __name__ == "__main__":
    with open(input_file, 'r') as fp:
        data = fp.read().strip()
    final_pos = resolve_position(data.split('\n'))
    print(final_pos[0] * final_pos[1])
