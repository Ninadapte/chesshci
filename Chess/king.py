from Chess.static import get_board_co_ord, is_valid_rc
from Game.values.colors import CHESS_WHITE

class King:
    Points = 0

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        if self.color == CHESS_WHITE:
            self.role = 'K'
        else:
            self.role = 'k'

    def get_valid_moves(self, board):
        pieces = board.pieces
        validMoves = []
        allMoves = []
        mv = 'K_' + get_board_co_ord(self.row, self.col) + '_'

        # One movers
        r, c = self.row, self.col
        for row, col in [(r + 1, c), (r + 1, c + 1), (r, c + 1), (r - 1, c + 1), (r - 1, c), (r - 1, c - 1), (r, c - 1),
                         (r + 1, c - 1)]:
            if is_valid_rc(row, col):
                if pieces[row][col] == '.':
                    allMoves.append(mv + get_board_co_ord(row, col))
                elif pieces[row][col].color != self.color:
                    allMoves.append(mv + get_board_co_ord(row, col) + 'x' + pieces[row][col].role.upper())

        # Castling moves
        if self.color == CHESS_WHITE:
            # Short Castle
            if board.piecesMoved['K'] == board.piecesMoved['RR'] == -1:
                if board.pieces[self.row][self.col + 1] == '.' and board.pieces[self.row][self.col + 2] == '.':
                    flag = True
                    for r, c in [(self.row, self.col), (self.row, self.col+1), (self.row, self.col+2)]:
                        if board.is_check(r, c):
                            flag = False
                            break
                    if flag:
                        validMoves.append('O-O')

            # Long Castle
            if board.piecesMoved['K'] == board.piecesMoved['LR'] == -1:
                if board.pieces[self.row][self.col-1] == '.' and board.pieces[self.row][self.col-2] == '.' and \
                        board.pieces[self.row][self.col-3] == '.':
                    flag = True
                    for r, c in [(self.row, self.col), (self.row, self.col-1), (self.row, self.col-2)]:
                        if board.is_check(r, c):
                            flag = False
                            break
                    if flag:
                        validMoves.append('O-O-O')
        else:
            # Short Castle
            if board.piecesMoved['k'] == board.piecesMoved['rr'] == -1:
                if board.pieces[self.row][self.col + 1] == '.' and board.pieces[self.row][self.col + 2] == '.':
                    flag = True
                    for r, c in [(self.row, self.col), (self.row, self.col + 1), (self.row, self.col + 2)]:
                        if board.is_check(r, c):
                            flag = False
                            break
                    if flag:
                        validMoves.append('O-O')

            # Long Castle
            if board.piecesMoved['k'] == board.piecesMoved['lr'] == -1:
                if board.pieces[self.row][self.col - 1] == '.' and board.pieces[self.row][self.col - 2] == '.' and \
                        board.pieces[self.row][self.col - 3] == '.':
                    flag = True
                    for r, c in [(self.row, self.col), (self.row, self.col - 1), (self.row, self.col - 2)]:
                        if board.is_check(r, c):
                            flag = False
                            break
                    if flag:
                        validMoves.append('O-O-O')

        # Validation
        for mv in allMoves:
            board.move(mv, debug=True)
            board.change_turn()
            if not board.is_check():
                validMoves.append(mv)
            board.change_turn()
            board.move_back(debug=True)
        return validMoves
