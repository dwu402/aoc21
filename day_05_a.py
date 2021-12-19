input_file = 'inputs/day_5.input'
MAX_NUM = 999

def toxy(spec):
    return [int(i) for a in spec.strip().split('->') for i in a.strip().split(',')]

def is_horizontal(ax, ay, bx, by):
    return ay == by

def is_vertical(ax, ay, bx, by):
    return ax == bx

def draw_picture(specs):
    picture =  [[0 for _ in range(MAX_NUM+1)] for _ in range(MAX_NUM+1)]
    coords = [toxy(spec) for spec in specs]
    for line in coords:
        if is_horizontal(*line):
            if line[0] < line[2]:
                start, end = line[0], line[2] + 1
            else:
                start, end = line[2], line[0] + 1
            for x in range(start, end):
                picture[line[1]][x] += 1
        elif is_vertical(*line):
            if line[1] < line[3]:
                start, end = line[1], line[3] + 1
            else:
                start, end = line[3], line[1] + 1
            for y in range(start, end):
                picture[y][line[0]] += 1
    # print_pic(picture)
    return picture

def print_pic(pic):
    for line in pic:
        for x in line:
            if x > 0:
                print(x, end='')
            else:
                print('.', end='')
        print('')

def count(pic):
    v = 0
    for row in pic:
        for pixel in row:
            if pixel > 1:
                v += 1
    return v

if __name__ == "__main__":
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    pic = draw_picture(data)
    print(count(pic))