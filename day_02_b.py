input_file = "inputs/day_2.input"


forward_map = {
    'forward': 1,
    'down': 0,
    'up': 0,
}

aim_map = {
    'forward': 0,
    'down': 1,
    'up': -1,
}

def resolve_position(commands):
    pos = [0, 0, 0]
    for command in commands:
        dir, scale_str = command.split(' ')
        scale = int(scale_str)
        pos[0] = pos[0] + scale * forward_map[dir]
        pos[1] = pos[1] + scale * pos[2] * forward_map[dir]
        pos[2] = pos[2] + scale * aim_map[dir]
    return pos

if __name__ == "__main__":
    with open(input_file, 'r') as fp:
        data = fp.read().strip()
    final_pos = resolve_position(data.split('\n'))
    print(final_pos[0] * final_pos[1])
