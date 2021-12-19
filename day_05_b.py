input_file = 'inputs/day_5.input'
# input_file = 'test.input'
MAX_NUM = 999

def toxy(spec):
    return [int(i) for a in spec.strip().split('->') for i in a.strip().split(',')]

def is_horizontal(ax, ay, bx, by):
    return ay == by

def is_vertical(ax, ay, bx, by):
    return ax == bx

def diag(ax, ay, bx, by):
    dx = (bx - ax)
    dy = (by - ay)
    return dx, dy

def is_diagonal(ax, ay, bx, by):
    dx, dy = diag(ax, ay, bx, by)
    return abs(dx) == abs(dy)


def draw_picture(specs):
    picture =  [[0 for _ in range(MAX_NUM+1)] for _ in range(MAX_NUM+1)]
    coords = [toxy(spec) for spec in specs]
    for line in coords:
        # print(line, end='')
        if is_horizontal(*line):
            # print('h')
            if line[0] < line[2]:
                start, end = line[0], line[2] + 1
            else:
                start, end = line[2], line[0] + 1
            for x in range(start, end):
                picture[line[1]][x] += 1
        elif is_vertical(*line):
            # print('v')
            if line[1] < line[3]:
                start, end = line[1], line[3] + 1
            else:
                start, end = line[3], line[1] + 1
            for y in range(start, end):
                picture[y][line[0]] += 1
        elif is_diagonal(*line):
            # print('d')
            dx, dy = diag(*line)
            dxi = (1 if  dx > 0 else -1)
            dyi = (1 if dy > 0 else -1)
            for i in range(abs(dx)+1):
                picture[line[1] + i*dyi][line[0] + i*dxi] += 1
        else:
            # print('x')
            pass
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