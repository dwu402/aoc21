input_file = 'inputs/day_4.input'

def read(filename):
    with open(filename, 'r') as fp:
        data = fp.read().strip()

        lines = data.split('\n')

    return lines

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def parse(lines):

    draws_line = lines[0]

    draws = [int(x) for x in draws_line.strip().split(',')]

    boards = [parse_board(board[1:]) for board in chunks(lines[1:], 6)]

    return draws, boards


def parse_board(board):
    return [[int(x[:2]) for x in chunks(line, 3)] for line in board]


def rotate_board(board):
    return [list(b) for b in zip(*board)]

def play_bingo(draws, boards):
    boards_T = [rotate_board(board) for board in boards]

    for draw in draws:
        one_round(draw, boards, boards_T)
        board_idx = check_bingo(boards, boards_T)
        if board_idx is not None:
            return score(boards[board_idx], draw)

def remove_from_list_of_lists(lol, num):
    for l in lol:
        try:
            l.remove(num)
        except ValueError:
            pass

def one_round(draw, boards, boards_T):
    for board in boards:
        remove_from_list_of_lists(board, draw)
    for board in boards_T:
        remove_from_list_of_lists(board, draw)

def check_bingo(*blists):
    for blist in blists:
        for j, board in enumerate(blist):
            for row in board:
                if len(row) == 0:
                    return j
    return None

def score(board, num):
    val = 0
    for row in board:
        for v in row:
            val += v
    return val * num

if __name__ == "__main__":
    lines = read(input_file)

    draws, boards = parse(lines)

    print(play_bingo(draws, boards))