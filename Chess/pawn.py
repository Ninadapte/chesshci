from Game.values.colors import CHESS_WHITE
from .static import get_board_co_ord, is_valid_rc


class Pawn:
    Points = 1

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        if self.color == CHESS_WHITE:
            self.role = 'P'
        else:
            self.role = 'p'

    def get_valid_moves(self, board, en_passant_col=-1):
        pieces = board.pieces
        validMoves = []
        allMoves = []
        direction = -1
        mv = 'P_' + get_board_co_ord(self.row, self.col) + '_'
        if self.color == CHESS_WHITE:
            direction = 1

        # If pawn is not moved, play 2 moves if possible
        if direction == 1 and self.row == 1 and pieces[self.row + 1][self.col] == '.' and \
                pieces[self.row + 2][self.col] == '.':
            allMoves.append(mv + get_board_co_ord(self.row + 2, self.col))
        elif direction == -1 and self.row == 6 and pieces[self.row - 1][self.col] == '.' and \
                pieces[self.row - 2][self.col] == '.':
            allMoves.append(mv + get_board_co_ord(self.row - 2, self.col))

        # En-passants
        if en_passant_col != -1:
            if direction == 1 and self.row == 4 and abs(en_passant_col - self.col) == 1:
                allMoves.append(mv + get_board_co_ord(self.row + 1, en_passant_col) + 'xP')
            elif direction == -1 and self.row == 3 and abs(en_passant_col - self.col) == 1:
                allMoves.append(mv + get_board_co_ord(self.row - 1, en_passant_col) + 'xP')

        # Promotions
        if (direction == 1 and self.row == 6) or (direction == -1 and self.row == 1):
            if pieces[self.row + direction][self.col] == '.':
                nxtPlace = get_board_co_ord(self.row + direction, self.col)
                allMoves.append(mv + nxtPlace + '=Q')
                allMoves.append(mv + nxtPlace + '=R')
                allMoves.append(mv + nxtPlace + '=N')
                allMoves.append(mv + nxtPlace + '=B')
            if is_valid_rc(0, self.col-1) and pieces[self.row + direction][self.col-1] != '.'\
                    and pieces[self.row+direction][self.col-1].color != self.color:
                nxtPlace = get_board_co_ord(self.row + direction, self.col-1)
                takenPieceRole = pieces[self.row + direction][self.col-1].role.upper()
                allMoves.append(mv + nxtPlace + 'x' + takenPieceRole + '=Q')
                allMoves.append(mv + nxtPlace + 'x' + takenPieceRole + '=R')
                allMoves.append(mv + nxtPlace + 'x' + takenPieceRole + '=N')
                allMoves.append(mv + nxtPlace + 'x' + takenPieceRole + '=B')
            if is_valid_rc(0, self.col+1) and pieces[self.row + direction][self.col+1] != '.'\
                    and pieces[self.row+direction][self.col+1].color != self.color:
                nxtPlace = get_board_co_ord(self.row + direction, self.col+1)
                takenPieceRole = pieces[self.row + direction][self.col+1].role.upper()
                allMoves.append(mv + nxtPlace + 'x' + takenPieceRole + '=Q')
                allMoves.append(mv + nxtPlace + 'x' + takenPieceRole + '=R')
                allMoves.append(mv + nxtPlace + 'x' + takenPieceRole + '=N')
                allMoves.append(mv + nxtPlace + 'x' + takenPieceRole + '=B')

        # Pawn 1 move and takes.
        if (direction == 1 and self.row != 6) or (direction == -1 and self.row != 1):
            if pieces[self.row + direction][self.col] == '.':
                allMoves.append(mv + get_board_co_ord(self.row + direction, self.col))

            if is_valid_rc(0, self.col-1):
                pieceTk = pieces[self.row + direction][self.col - 1]
                if pieceTk != '.' and pieceTk.color != self.color:
                    nxtPlace = get_board_co_ord(self.row + direction, self.col-1)
                    takenPieceRole = pieceTk.role.upper()
                    allMoves.append(mv + nxtPlace + 'x' + takenPieceRole)

            if is_valid_rc(0, self.col+1):
                pieceTk = pieces[self.row + direction][self.col+1]
                if pieceTk != '.' and pieceTk.color != self.color:
                    nxtPlace = get_board_co_ord(self.row + direction, self.col+1)
                    takenPieceRole = pieceTk.role.upper()
                    allMoves.append(mv + nxtPlace + 'x' + takenPieceRole)

        # Validation
        for mv in allMoves:
            board.move(mv, debug=True)
            board.change_turn()
            if not board.is_check():
                validMoves.append(mv)
            board.change_turn()
            board.move_back(debug=True)
        return validMoves
