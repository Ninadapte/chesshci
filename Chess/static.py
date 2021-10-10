from Game.values.dimens import coordinates, letters

def get_board_co_ord(row, col):
    return str(coordinates[col + 1]) + str(row + 1)

def get_row_col(move):
    return int(move[1]) - 1, letters[move[0]] - 1

def is_valid_rc(row=0, col=0):
    if 0 <= row <= 7 and 0 <= col <= 7:
        return True
    return False
