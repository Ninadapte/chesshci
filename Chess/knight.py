from Chess.static import get_board_co_ord, is_valid_rc
from Game.values.colors import CHESS_WHITE

class Knight:
    Points = 3

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        if self.color == CHESS_WHITE:
            self.role = 'N'
        else:
            self.role = 'n'

    def get_valid_moves(self, board):
        pieces = board.pieces
        validMoves = []
        allMoves = []
        mv = 'N_' + get_board_co_ord(self.row, self.col) + '_'

        r, c = self.row, self.col
        for row, col in [(r+2, c+1), (r+1, c+2), (r-2, c+1), (r-1, c+2), (r+2, c-1), (r+1, c-2), (r-2, c-1),
                         (r-1, c-2)]:
            if is_valid_rc(row, col):
                if pieces[row][col] == '.':
                    allMoves.append(mv + get_board_co_ord(row, col))
                elif pieces[row][col].color != self.color:
                    allMoves.append(mv + get_board_co_ord(row, col) + 'x' + pieces[row][col].role.upper())

        # Validation
        for mv in allMoves:
            board.move(mv, debug=True)
            board.change_turn()
            if not board.is_check():
                validMoves.append(mv)
            board.change_turn()
            board.move_back(debug=True)
        return validMoves
