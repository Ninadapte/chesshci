from Chess.static import get_board_co_ord, is_valid_rc
from Game.values.colors import CHESS_WHITE

class Bishop:
    Points = 3

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        if self.color == CHESS_WHITE:
            self.role = 'B'
        else:
            self.role = 'b'

    def get_valid_moves(self, board):
        pieces = board.pieces
        validMoves = []
        allMoves = []
        mv = 'B_' + get_board_co_ord(self.row, self.col) + '_'

        # North - East
        r, c = self.row + 1, self.col + 1
        while is_valid_rc(r, c):
            piece = pieces[r][c]
            if piece != '.':
                if piece.color != self.color:
                    allMoves.append(mv + get_board_co_ord(r, c) + 'x' + piece.role.upper())
                break
            else:
                allMoves.append(mv + get_board_co_ord(r, c))
            r += 1
            c += 1

        # South - East
        r, c = self.row - 1, self.col + 1
        while is_valid_rc(r, c):
            piece = pieces[r][c]
            if piece != '.':
                if piece.color != self.color:
                    allMoves.append(mv + get_board_co_ord(r, c) + 'x' + piece.role.upper())
                break
            else:
                allMoves.append(mv + get_board_co_ord(r, c))
            r -= 1
            c += 1

        # South - West
        r, c = self.row - 1, self.col - 1
        while is_valid_rc(r, c):
            piece = pieces[r][c]
            if piece != '.':
                if piece.color != self.color:
                    allMoves.append(mv + get_board_co_ord(r, c) + 'x' + piece.role.upper())
                break
            else:
                allMoves.append(mv + get_board_co_ord(r, c))
            r -= 1
            c -= 1

        # North - West
        r, c = self.row + 1, self.col - 1
        while is_valid_rc(r, c):
            piece = pieces[r][c]
            if piece != '.':
                if piece.color != self.color:
                    allMoves.append(mv + get_board_co_ord(r, c) + 'x' + piece.role.upper())
                break
            else:
                allMoves.append(mv + get_board_co_ord(r, c))
            r += 1
            c -= 1

        # Validation
        for mv in allMoves:
            board.move(mv, debug=True)
            board.change_turn()
            if not board.is_check():
                validMoves.append(mv)
            board.change_turn()
            board.move_back(debug=True)
        return validMoves
