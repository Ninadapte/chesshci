from Game.values.colors import CHESS_WHITE, CHESS_BLACK
from .bishop import Bishop
from .king import King
from .knight import Knight
from .pawn import Pawn
from .queen import Queen
from .rook import Rook
from .static import get_row_col, is_valid_rc
import re


class chessBoard:
    def __init__(self, Board_type="STANDARD"):

        self.WhiteKing = None
        self.BlackKing = None

        self.pieces = []
        self.Board_type = Board_type

        self.turn = True

        # white pieces
        self.white_pawns = 8
        self.white_dark_bishops = 1
        self.white_light_bishops = 1
        self.white_knights = 2
        self.white_rooks = 2
        self.white_queens = 1
        self.white_kings = 1
        # black pieces
        self.black_pawns = 8
        self.black_dark_bishops = 1
        self.black_light_bishops = 1
        self.black_knights = 2
        self.black_rooks = 2
        self.black_queens = 1
        self.black_kings = 1

        self.en_passants = {}
        # Stores column of possible en-passant with the move associated with it.

        # Winning percentage of white
        self.win_percent = 50
        self.p1_adv = "0.00"
        self.p2_adv = "-0.00"

        self.moveList = []
        self.whiteMoveList = []
        self.poppedMoveList = []
        self.moveCount = 0
        # Stores the first move where respective piece was moved. (Also serves the purpose of castling rights.)
        self.piecesMoved = {'K': -1, 'LR': -1, 'RR': -1, 'k': -1, 'lr': -1, 'rr': -1}

        self.draw_accepted = False
        self.winner = None
        self.initialize_pieces()

    def initialize_pieces(self):
        if self.Board_type == 'No Castle':

            self.WhiteKing = King(0, 4, CHESS_WHITE)
            self.BlackKing = King(7, 4, CHESS_BLACK)

            self.pieces = [
                [Rook(0, 0, CHESS_WHITE), Knight(0, 1, CHESS_WHITE), Bishop(0, 2, CHESS_WHITE),
                 Queen(0, 3, CHESS_WHITE), self.WhiteKing, Bishop(0, 5, CHESS_WHITE), Knight(0, 6, CHESS_WHITE),
                 Rook(0, 7, CHESS_WHITE)],

                [Pawn(1, 0, CHESS_WHITE), Pawn(1, 1, CHESS_WHITE), Pawn(1, 2, CHESS_WHITE), Pawn(1, 3, CHESS_WHITE),
                 Pawn(1, 4, CHESS_WHITE), Pawn(1, 5, CHESS_WHITE), Pawn(1, 6, CHESS_WHITE), Pawn(1, 7, CHESS_WHITE)],

                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],

                [Pawn(6, 0, CHESS_BLACK), Pawn(6, 1, CHESS_BLACK), Pawn(6, 2, CHESS_BLACK), Pawn(6, 3, CHESS_BLACK),
                 Pawn(6, 4, CHESS_BLACK), Pawn(6, 5, CHESS_BLACK), Pawn(6, 6, CHESS_BLACK), Pawn(6, 7, CHESS_BLACK)],

                [Rook(7, 0, CHESS_BLACK), Knight(7, 1, CHESS_BLACK), Bishop(7, 2, CHESS_BLACK),
                 Queen(7, 3, CHESS_BLACK), self.BlackKing, Bishop(7, 5, CHESS_BLACK), Knight(7, 6, CHESS_BLACK),
                 Rook(7, 7, CHESS_BLACK)]
            ]
            self.piecesMoved = {'K': 0, 'LR': 0, 'RR': 0, 'k': 0, 'lr': 0, 'rr': 0}
        elif self.Board_type == 'Chess 960':

            self.WhiteKing = King(0, 3, CHESS_WHITE)
            self.BlackKing = King(7, 3, CHESS_BLACK)

            self.pieces = [
                [Queen(0, 0, CHESS_WHITE), Rook(0, 1, CHESS_WHITE), Knight(0, 2, CHESS_WHITE), self.WhiteKing,
                 Knight(0, 4, CHESS_WHITE), Bishop(0, 5, CHESS_WHITE), Bishop(0, 6, CHESS_WHITE),
                 Rook(0, 7, CHESS_WHITE)],

                [Pawn(1, 0, CHESS_WHITE), Pawn(1, 1, CHESS_WHITE), Pawn(1, 2, CHESS_WHITE), Pawn(1, 3, CHESS_WHITE),
                 Pawn(1, 4, CHESS_WHITE), Pawn(1, 5, CHESS_WHITE), Pawn(1, 6, CHESS_WHITE), Pawn(1, 7, CHESS_WHITE)],

                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],

                [Pawn(6, 0, CHESS_BLACK), Pawn(6, 1, CHESS_BLACK), Pawn(6, 2, CHESS_BLACK), Pawn(6, 3, CHESS_BLACK),
                 Pawn(6, 4, CHESS_BLACK), Pawn(6, 5, CHESS_BLACK), Pawn(6, 6, CHESS_BLACK), Pawn(6, 7, CHESS_BLACK)],

                [Queen(7, 0, CHESS_BLACK), Rook(7, 1, CHESS_BLACK), Knight(7, 2, CHESS_BLACK), self.BlackKing,
                 Knight(7, 4, CHESS_BLACK), Bishop(7, 5, CHESS_BLACK), Bishop(7, 6, CHESS_BLACK),
                 Rook(7, 7, CHESS_BLACK)]
            ]

            # No castling for chess_960
            self.piecesMoved = {'K': 0, 'LR': 0, 'RR': 0, 'k': 0, 'lr': 0, 'rr': 0}
        else:
            # 7     r n b q k b n r
            # 6     p p p p p p p p
            # 5     . . . . . . . .
            # 4     . . . . . . . .
            # 3     . . . . . . . .
            # 2     . . . . . . . .
            # 1     P P P P P P P P
            # 0     R N B Q K B N R
            #
            #       0 1 2 3 4 5 6 7

            self.WhiteKing = King(0, 4, CHESS_WHITE)
            self.BlackKing = King(7, 4, CHESS_BLACK)

            self.pieces = [
                [Rook(0, 0, CHESS_WHITE), Knight(0, 1, CHESS_WHITE), Bishop(0, 2, CHESS_WHITE),
                 Queen(0, 3, CHESS_WHITE), self.WhiteKing, Bishop(0, 5, CHESS_WHITE), Knight(0, 6, CHESS_WHITE),
                 Rook(0, 7, CHESS_WHITE)],

                [Pawn(1, 0, CHESS_WHITE), Pawn(1, 1, CHESS_WHITE), Pawn(1, 2, CHESS_WHITE), Pawn(1, 3, CHESS_WHITE),
                 Pawn(1, 4, CHESS_WHITE), Pawn(1, 5, CHESS_WHITE), Pawn(1, 6, CHESS_WHITE), Pawn(1, 7, CHESS_WHITE)],

                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],

                [Pawn(6, 0, CHESS_BLACK), Pawn(6, 1, CHESS_BLACK), Pawn(6, 2, CHESS_BLACK), Pawn(6, 3, CHESS_BLACK),
                 Pawn(6, 4, CHESS_BLACK), Pawn(6, 5, CHESS_BLACK), Pawn(6, 6, CHESS_BLACK), Pawn(6, 7, CHESS_BLACK)],

                [Rook(7, 0, CHESS_BLACK), Knight(7, 1, CHESS_BLACK), Bishop(7, 2, CHESS_BLACK),
                 Queen(7, 3, CHESS_BLACK), self.BlackKing, Bishop(7, 5, CHESS_BLACK), Knight(7, 6, CHESS_BLACK),
                 Rook(7, 7, CHESS_BLACK)]
            ]
    

    def move(self, move=None, debug=False):
        # 'P_e4_e5' - Pawn from e4 to e5.
        # 'P_e5_f6' - Pawn from e5 to f6 (En-Passant).
        # 'O-O' - Short castle.
        # 'O-O-O' - Long Castle.
        # 'R_a4_a8xB' - Rook from a4 to a8 takes Bishop.
        # 'P_e7_e8=Q' - Pawn form e7 to e8 promoted to Queen.
        # 'P_e7_f8xQ=N' - Pawn from e7 to f8 takes Queen promoted to Knight.

        if move is None:
            try:
                move = self.poppedMoveList.pop(-1)
            except IndexError:
                return False
        elif not debug:
            self.poppedMoveList.clear()

        if not debug:
            if self.turn:
                color = CHESS_WHITE
            else:
                color = CHESS_BLACK
            if move not in self.get_all_valid_moves(color):
                return

        if move == 'O-O':
            if self.turn:
                self.pieces[0][4], self.pieces[0][6] = self.pieces[0][6], self.pieces[0][4]
                self.pieces[0][6].col = 6
                self.pieces[0][5], self.pieces[0][7] = self.pieces[0][7], self.pieces[0][5]
                self.pieces[0][5].col = 5

                # Setting king and rook to be moved.
                self.piecesMoved['K'] = self.moveCount
                self.piecesMoved['RR'] = self.moveCount
            else:
                self.pieces[7][4], self.pieces[7][6] = self.pieces[7][6], self.pieces[7][4]
                self.pieces[7][6].col = 6
                self.pieces[7][5], self.pieces[7][7] = self.pieces[7][7], self.pieces[7][5]
                self.pieces[7][5].col = 5

                # Setting king and rook to be moved.
                self.piecesMoved['k'] = self.moveCount
                self.piecesMoved['rr'] = self.moveCount

        elif move == 'O-O-O':
            if self.turn:
                self.pieces[0][2], self.pieces[0][4] = self.pieces[0][4], self.pieces[0][2]
                self.pieces[0][2].col = 2
                self.pieces[0][0], self.pieces[0][3] = self.pieces[0][3], self.pieces[0][0]
                self.pieces[0][3].col = 3

                # Setting king and rook to be moved.
                self.piecesMoved['K'] = self.moveCount
                self.piecesMoved['LR'] = self.moveCount

            else:
                self.pieces[7][2], self.pieces[7][4] = self.pieces[7][4], self.pieces[7][2]
                self.pieces[7][2].col = 2
                self.pieces[7][0], self.pieces[7][3] = self.pieces[7][3], self.pieces[7][0]
                self.pieces[7][3].col = 3

                # Setting king and rook to be moved.
                self.piecesMoved['k'] = self.moveCount
                self.piecesMoved['lr'] = self.moveCount

        elif move[-2] == '=':
            newPos = get_row_col(move[5:7])
            oldPos = get_row_col(move[2:4])
            self.pieces[oldPos[0]][oldPos[1]] = '.'

            if self.turn:
                self.white_pawns -= 1

                if 'x' in move:
                    capturedPiece = move[1 + move.find('x')]
                    if capturedPiece == 'B':
                        if newPos[1] % 2:
                            self.black_dark_bishops -= 1
                        else:
                            self.black_light_bishops -= 1
                    elif capturedPiece == 'N':
                        self.black_knights -= 1
                    elif capturedPiece == 'Q':
                        self.black_queens -= 1
                    elif capturedPiece == 'R':
                        self.black_rooks -= 1
                    # Pawns can not reside on 8th or 1st rank.

                if move[-1] == 'B':
                    if newPos[1] % 2:
                        self.white_dark_bishops += 1
                    else:
                        self.white_light_bishops += 1
                    self.pieces[newPos[0]][newPos[1]] = Bishop(newPos[0], newPos[1], CHESS_WHITE)
                elif move[-1] == 'N':
                    self.white_knights += 1
                    self.pieces[newPos[0]][newPos[1]] = Knight(newPos[0], newPos[1], CHESS_WHITE)
                elif move[-1] == 'Q':
                    self.white_queens += 1
                    self.pieces[newPos[0]][newPos[1]] = Queen(newPos[0], newPos[1], CHESS_WHITE)
                elif move[-1] == 'R':
                    self.white_rooks += 1
                    self.pieces[newPos[0]][newPos[1]] = Rook(newPos[0], newPos[1], CHESS_WHITE)

            else:
                self.black_pawns -= 1

                if 'x' in move:
                    capturedPiece = move[1 + move.find('x')]
                    if capturedPiece == 'B':
                        if newPos[1] % 2:
                            self.white_dark_bishops -= 1
                        else:
                            self.white_light_bishops -= 1
                    elif capturedPiece == 'N':
                        self.white_knights -= 1
                    elif capturedPiece == 'Q':
                        self.white_queens -= 1
                    elif capturedPiece == 'R':
                        self.white_rooks -= 1
                    # Pawns can not reside on 8th or 1st rank.

                if move[-1] == 'B':
                    if newPos[1] % 2:
                        self.black_light_bishops += 1
                    else:
                        self.black_dark_bishops += 1
                    self.pieces[newPos[0]][newPos[1]] = Bishop(newPos[0], newPos[1], CHESS_BLACK)
                elif move[-1] == 'N':
                    self.black_knights += 1
                    self.pieces[newPos[0]][newPos[1]] = Knight(newPos[0], newPos[1], CHESS_BLACK)
                elif move[-1] == 'Q':
                    self.black_queens += 1
                    self.pieces[newPos[0]][newPos[1]] = Queen(newPos[0], newPos[1], CHESS_BLACK)
                elif move[-1] == 'R':
                    self.black_rooks += 1
                    self.pieces[newPos[0]][newPos[1]] = Rook(newPos[0], newPos[1], CHESS_BLACK)

        else:
            newPos = get_row_col(move[5:7])
            oldPos = get_row_col(move[2:4])

            self.pieces[newPos[0]][newPos[1]], self.pieces[oldPos[0]][oldPos[1]] = \
                self.pieces[oldPos[0]][oldPos[1]], '.'
            self.pieces[newPos[0]][newPos[1]].row = newPos[0]
            self.pieces[newPos[0]][newPos[1]].col = newPos[1]

            # Setting king and rooks when ever they moved first time.
            if move[0] == 'K':
                if oldPos == (0, 4) and self.piecesMoved['K'] == -1:
                    self.piecesMoved['K'] = self.moveCount
                elif oldPos == (7, 4) and self.piecesMoved['k'] == -1:
                    self.piecesMoved['k'] = self.moveCount

            elif move[0] == 'R':
                if oldPos == (0, 0) and self.piecesMoved['LR'] == -1:
                    self.piecesMoved['LR'] = self.moveCount
                elif oldPos == (0, 7) and self.piecesMoved['RR'] == -1:
                    self.piecesMoved['RR'] = self.moveCount
                if oldPos == (7, 0) and self.piecesMoved['lr'] == -1:
                    self.piecesMoved['lr'] = self.moveCount
                elif oldPos == (7, 7) and self.piecesMoved['rr'] == -1:
                    self.piecesMoved['rr'] = self.moveCount
            elif move[0] == 'P':
                # En-passant
                if abs(oldPos[0] - newPos[0]) == 2 and oldPos[1] == newPos[1]:
                    self.en_passants[self.moveCount] = oldPos[1]

            if self.turn:
                if 'x' in move:
                    capturedPiece = move[1 + move.find('x')]
                    if capturedPiece == 'B':
                        if (newPos[0] + newPos[1]) % 2:
                            self.black_light_bishops -= 1
                        else:
                            self.black_dark_bishops -= 1
                    elif capturedPiece == 'N':
                        self.black_knights -= 1
                    elif capturedPiece == 'Q':
                        self.black_queens -= 1
                    elif capturedPiece == 'R':
                        self.black_rooks -= 1
                    elif capturedPiece == 'P':
                        self.black_pawns -= 1
                        # if En-passant then remove the captured pawn.
                        if move[0] == 'P' and oldPos[0] == 4 and newPos[0] == 5 and abs(oldPos[1] - newPos[1]) == 1:
                            if self.moveCount-1 in self.en_passants.keys():
                                if self.en_passants[self.moveCount-1] == newPos[1]:
                                    self.pieces[oldPos[0]][newPos[1]] = '.'
            else:
                if 'x' in move:
                    capturedPiece = move[1 + move.find('x')]
                    if capturedPiece == 'B':
                        if (newPos[0] + newPos[1]) % 2:
                            self.white_light_bishops -= 1
                        else:
                            self.white_dark_bishops -= 1
                    elif capturedPiece == 'N':
                        self.white_knights -= 1
                    elif capturedPiece == 'Q':
                        self.white_queens -= 1
                    elif capturedPiece == 'R':
                        self.white_rooks -= 1
                    elif capturedPiece == 'P':
                        self.white_pawns -= 1
                        # if En-passant then remove the captured pawn.
                        if move[0] == 'P' and oldPos[0] == 3 and newPos[0] == 2 and abs(oldPos[1] - newPos[1]) == 1:
                            if self.moveCount - 1 in self.en_passants.keys():
                                if self.en_passants[self.moveCount - 1] == newPos[1]:
                                    self.pieces[oldPos[0]][newPos[1]] = '.'

        self.moveCount += 1
        self.change_turn()
        self.moveList.append(move)
        self.evaluate_advantage()
        return True

    def move_back(self, debug=False):
        # 'P_e4_e5' - Pawn from e4 to e5.
        # 'P_e5_f6' - Pawn from e5 to f6 (En-Passant).
        # 'O-O' - Short castle.
        # 'O-O-O' - Long Castle.
        # 'R_a4_a8xB' - Rook from a4 to a8 takes Bishop.
        # 'P_e7_e8=Q' - Pawn form e7 to e8 promoted to Queen.
        # 'P_e7_f8xQ=N' - Pawn from e7 to f8 takes Queen promoted to Knight.

        try:
            move = self.moveList.pop(-1)
        except IndexError:
            return False

        self.moveCount -= 1

        if move == 'O-O':
            if not self.turn:  # Black's turn
                self.pieces[0][4], self.pieces[0][6] = self.pieces[0][6], self.pieces[0][4]
                self.pieces[0][4].col = 4
                self.pieces[0][5], self.pieces[0][7] = self.pieces[0][7], self.pieces[0][5]
                self.pieces[0][7].col = 7

                # Setting king and rook as not moved.
                self.piecesMoved['K'] = -1
                self.piecesMoved['RR'] = -1
            else:
                self.pieces[7][4], self.pieces[7][6] = self.pieces[7][6], self.pieces[7][4]
                self.pieces[7][4].col = 4
                self.pieces[7][5], self.pieces[7][7] = self.pieces[7][7], self.pieces[7][5]
                self.pieces[7][7].col = 7

                # Setting king and rook as not moved.
                self.piecesMoved['k'] = -1
                self.piecesMoved['rr'] = -1

        elif move == 'O-O-O':
            if not self.turn:
                self.pieces[0][2], self.pieces[0][4] = self.pieces[0][4], self.pieces[0][2]
                self.pieces[0][4].col = 4
                self.pieces[0][0], self.pieces[0][3] = self.pieces[0][3], self.pieces[0][0]
                self.pieces[0][0].col = 0

                # Setting king and rook as not moved.
                self.piecesMoved['K'] = -1
                self.piecesMoved['LR'] = -1

            else:
                self.pieces[7][2], self.pieces[7][4] = self.pieces[7][4], self.pieces[7][2]
                self.pieces[7][4].col = 4
                self.pieces[7][0], self.pieces[7][3] = self.pieces[7][3], self.pieces[7][0]
                self.pieces[7][0].col = 0

                # Setting king and rook as not moved.
                self.piecesMoved['k'] = -1
                self.piecesMoved['lr'] = -1

        elif move[-2] == '=':
            newPos = get_row_col(move[5:7])
            oldPos = get_row_col(move[2:4])
            self.pieces[oldPos[0]][oldPos[1]] = '.'

            if not self.turn:  # Black's turn
                # noinspection PyTypeChecker
                self.pieces[oldPos[0]][oldPos[1]] = Pawn(oldPos[0], oldPos[1], CHESS_WHITE)
                self.white_pawns += 1

                if 'x' in move:
                    capturedPiece = move[1 + move.find('x')]
                    if capturedPiece == 'B':
                        self.pieces[newPos[0]][newPos[1]] = Bishop(newPos[0], newPos[1], CHESS_BLACK)
                        if newPos[1] % 2:
                            self.black_dark_bishops += 1
                        else:
                            self.black_light_bishops += 1
                    elif capturedPiece == 'N':
                        self.pieces[newPos[0]][newPos[1]] = Knight(newPos[0], newPos[1], CHESS_BLACK)
                        self.black_knights += 1
                    elif capturedPiece == 'Q':
                        self.pieces[newPos[0]][newPos[1]] = Queen(newPos[0], newPos[1], CHESS_BLACK)
                        self.black_queens += 1
                    elif capturedPiece == 'R':
                        self.pieces[newPos[0]][newPos[1]] = Rook(newPos[0], newPos[1], CHESS_BLACK)
                        self.black_rooks += 1
                    # Pawns can not reside on 8th or 1st rank.
                else:
                    # Promoted by straight move of pawn
                    self.pieces[newPos[0]][newPos[1]] = '.'

                if move[-1] == 'B':
                    if newPos[1] % 2:
                        self.white_dark_bishops -= 1
                    else:
                        self.white_light_bishops -= 1
                elif move[-1] == 'N':
                    self.white_knights -= 1
                elif move[-1] == 'Q':
                    self.white_queens -= 1
                elif move[-1] == 'R':
                    self.white_rooks -= 1

            else:  # White's turn
                # noinspection PyTypeChecker
                self.pieces[oldPos[0]][oldPos[1]] = Pawn(oldPos[0], oldPos[1], CHESS_BLACK)
                self.black_pawns += 1

                if 'x' in move:
                    capturedPiece = move[1 + move.find('x')]
                    if capturedPiece == 'B':
                        self.pieces[newPos[0]][newPos[1]] = Bishop(newPos[0], newPos[1], CHESS_WHITE)
                        if newPos[1] % 2:
                            self.white_dark_bishops += 1
                        else:
                            self.white_light_bishops += 1
                    elif capturedPiece == 'N':
                        self.pieces[newPos[0]][newPos[1]] = Knight(newPos[0], newPos[1], CHESS_WHITE)
                        self.white_knights += 1
                    elif capturedPiece == 'Q':
                        self.pieces[newPos[0]][newPos[1]] = Queen(newPos[0], newPos[1], CHESS_WHITE)
                        self.white_queens += 1
                    elif capturedPiece == 'R':
                        self.pieces[newPos[0]][newPos[1]] = Rook(newPos[0], newPos[1], CHESS_WHITE)
                        self.white_rooks += 1
                    # Pawns can not reside on 8th or 1st rank.
                else:
                    # Promoted by straight move of pawn
                    self.pieces[newPos[0]][newPos[1]] = '.'

                if move[-1] == 'B':
                    if newPos[1] % 2:
                        self.black_light_bishops -= 1
                    else:
                        self.black_dark_bishops -= 1
                elif move[-1] == 'N':
                    self.black_knights -= 1
                elif move[-1] == 'Q':
                    self.black_queens -= 1
                elif move[-1] == 'R':
                    self.black_rooks -= 1

        else:
            newPos = get_row_col(move[5:7])
            oldPos = get_row_col(move[2:4])

            self.pieces[oldPos[0]][oldPos[1]], self.pieces[newPos[0]][newPos[1]] = \
                self.pieces[newPos[0]][newPos[1]], '.'
            self.pieces[oldPos[0]][oldPos[1]].row = oldPos[0]
            self.pieces[oldPos[0]][oldPos[1]].col = oldPos[1]

            # Setting king and rooks when ever they moved first time.
            if move[0] == 'K':
                if oldPos == (0, 4) and self.piecesMoved['K'] == self.moveCount:
                    self.piecesMoved['K'] = -1
                elif oldPos == (7, 4) and self.piecesMoved['k'] == self.moveCount:
                    self.piecesMoved['k'] = -1

            elif move[0] == 'R':
                if oldPos == (0, 0) and self.piecesMoved['LR'] == self.moveCount:
                    self.piecesMoved['LR'] = -1
                elif oldPos == (0, 7) and self.piecesMoved['RR'] == self.moveCount:
                    self.piecesMoved['RR'] = -1
                if oldPos == (7, 0) and self.piecesMoved['lr'] == self.moveCount:
                    self.piecesMoved['lr'] = -1
                elif oldPos == (7, 7) and self.piecesMoved['rr'] == self.moveCount:
                    self.piecesMoved['rr'] = -1

            elif move[0] == 'P':
                # En-passant
                if abs(oldPos[0] - newPos[0]) == 2 and oldPos[1] == newPos[1]:
                    self.en_passants.pop(self.moveCount)

            if not self.turn:  # Black's turn
                if 'x' in move:
                    capturedPiece = move[1 + move.find('x')]
                    if capturedPiece == 'B':
                        self.pieces[newPos[0]][newPos[1]] = Bishop(newPos[0], newPos[1], CHESS_BLACK)
                        if (newPos[0] + newPos[1]) % 2:
                            self.black_light_bishops += 1
                        else:
                            self.black_dark_bishops += 1
                    elif capturedPiece == 'N':
                        self.pieces[newPos[0]][newPos[1]] = Knight(newPos[0], newPos[1], CHESS_BLACK)
                        self.black_knights += 1
                    elif capturedPiece == 'Q':
                        self.pieces[newPos[0]][newPos[1]] = Queen(newPos[0], newPos[1], CHESS_BLACK)
                        self.black_queens += 1
                    elif capturedPiece == 'R':
                        self.pieces[newPos[0]][newPos[1]] = Rook(newPos[0], newPos[1], CHESS_BLACK)
                        self.black_rooks += 1
                    elif capturedPiece == 'P':
                        # If En-Passant
                        if oldPos[0] == 4 and self.moveCount - 1 in self.en_passants.keys() and \
                                self.en_passants[self.moveCount - 1] == newPos[1]:
                            self.pieces[oldPos[0]][newPos[1]] = Pawn(oldPos[0], newPos[1], CHESS_BLACK)
                        else:
                            self.pieces[newPos[0]][newPos[1]] = Pawn(newPos[0], newPos[1], CHESS_BLACK)
                        self.black_pawns += 1

            else:  # White's move
                if 'x' in move:
                    capturedPiece = move[1 + move.find('x')]
                    if capturedPiece == 'B':
                        self.pieces[newPos[0]][newPos[1]] = Bishop(newPos[0], newPos[1], CHESS_WHITE)
                        if (newPos[0] + newPos[1]) % 2:
                            self.white_light_bishops += 1
                        else:
                            self.white_dark_bishops += 1
                    elif capturedPiece == 'N':
                        self.pieces[newPos[0]][newPos[1]] = Knight(newPos[0], newPos[1], CHESS_WHITE)
                        self.white_knights += 1
                    elif capturedPiece == 'Q':
                        self.pieces[newPos[0]][newPos[1]] = Queen(newPos[0], newPos[1], CHESS_WHITE)
                        self.white_queens += 1
                    elif capturedPiece == 'R':
                        self.pieces[newPos[0]][newPos[1]] = Rook(newPos[0], newPos[1], CHESS_WHITE)
                        self.white_rooks += 1
                    elif capturedPiece == 'P':
                        # if En-passant
                        if oldPos[0] == 3 and self.moveCount - 1 in self.en_passants.keys() and \
                                self.en_passants[self.moveCount - 1] == newPos[1]:
                            self.pieces[oldPos[0]][newPos[1]] = Pawn(oldPos[0], newPos[1], CHESS_WHITE)
                        else:
                            self.pieces[newPos[0]][newPos[1]] = Pawn(newPos[0], newPos[1], CHESS_WHITE)
                        self.white_pawns += 1

        # self.en_passants.clear()
        self.change_turn()
        if not debug:
            self.poppedMoveList.append(move)
        self.evaluate_advantage()
        return True

    def is_check(self, row=None, col=None):
        if row is None:
            if self.turn:
                row = self.WhiteKing.row
                col = self.WhiteKing.col
            else:
                row = self.BlackKing.row
                col = self.BlackKing.col

        oppColor = CHESS_WHITE
        if self.turn:
            oppColor = CHESS_BLACK

        # Pawn attacks
        if self.turn:
            for r, c in [(row + 1, col + 1), (row + 1, col - 1)]:
                if is_valid_rc(r, c):
                    piece = self.pieces[r][c]
                    if piece != '.' and piece.color == oppColor and piece.role in ['P', 'p']:
                        return True
        else:
            for r, c in [(row - 1, col + 1), (row - 1, col - 1)]:
                if is_valid_rc(r, c):
                    piece = self.pieces[r][c]
                    if piece != '.' and piece.color == oppColor and piece.role in ['P', 'p']:
                        return True

        # Rook and horizontal queen attacks
        # North
        r, c = row + 1, col
        while is_valid_rc(r, c):
            piece = self.pieces[r][c]
            if piece != '.':
                if piece.color == oppColor and piece.role in ['R', 'r', 'Q', 'q']:
                    return True
                break
            r += 1

        # East
        r, c = row, col + 1
        while is_valid_rc(r, c):
            piece = self.pieces[r][c]
            if piece != '.':
                if piece.color == oppColor and piece.role in ['R', 'r', 'Q', 'q']:
                    return True
                break
            c += 1

        # South
        r, c = row - 1, col
        while is_valid_rc(r, c):
            piece = self.pieces[r][c]
            if piece != '.':
                if piece.color == oppColor and piece.role in ['R', 'r', 'Q', 'q']:
                    return True
                break
            r -= 1

        # West
        r, c = row, col - 1
        while is_valid_rc(r, c):
            piece = self.pieces[r][c]
            if piece != '.':
                if piece.color == oppColor and piece.role in ['R', 'r', 'Q', 'q']:
                    return True
                break
            c -= 1

        # Bishop and diagonal queen attacks
        # North - East
        r, c = row + 1, col + 1
        while is_valid_rc(r, c):
            piece = self.pieces[r][c]
            if piece != '.':
                if piece.color == oppColor and piece.role in ['B', 'b', 'Q', 'q']:
                    return True
                break
            r += 1
            c += 1

        # South - East
        r, c = row - 1, col + 1
        while is_valid_rc(r, c):
            piece = self.pieces[r][c]
            if piece != '.':
                if piece.color == oppColor and piece.role in ['B', 'b', 'Q', 'q']:
                    return True
                break
            r -= 1
            c += 1

        # South - West
        r, c = row - 1, col - 1
        while is_valid_rc(r, c):
            piece = self.pieces[r][c]
            if piece != '.':
                if piece.color == oppColor and piece.role in ['B', 'b', 'Q', 'q']:
                    return True
                break
            r -= 1
            c -= 1

        # North - West
        r, c = row + 1, col - 1
        while is_valid_rc(r, c):
            piece = self.pieces[r][c]
            if piece != '.':
                if piece.color == oppColor and piece.role in ['B', 'b', 'Q', 'q']:
                    return True
                break
            r += 1
            c -= 1

        # Knight attacks
        for r, c in [(row + 2, col + 1), (row + 1, col + 2), (row - 2, col + 1), (row - 1, col + 2), (row + 2, col - 1),
                     (row + 1, col - 2),
                     (row - 2, col - 1), (row - 1, col - 2)]:
            if is_valid_rc(r, c):
                piece = self.pieces[r][c]
                if piece != '.' and piece.color == oppColor and piece.role in ['N', 'n']:
                    return True

        # King attacks
        # ( Though king cannot attack opponent's king, to remove the condition where two kings will stand side by side,
        # king's attacks are also taken into consideration.)
        r, c = row, col
        for rw, co in [(r + 1, c), (r + 1, c + 1), (r, c + 1), (r - 1, c + 1), (r - 1, c), (r - 1, c - 1), (r, c - 1),
                       (r + 1, c - 1)]:
            if is_valid_rc(rw, co):
                piece = self.pieces[rw][co]
                if piece != '.' and piece.color == oppColor and piece.role in ['K', 'k']:
                    return True

        return False

    def is_checkmate(self):
        if self.turn:
            if self.is_check(self.WhiteKing.row, self.WhiteKing.col) and not self.get_all_valid_moves():
                return True
        else:
            if self.is_check(self.BlackKing.row, self.BlackKing.col) and not self.get_all_valid_moves():
                return True
        return False

    def draw_by_insufficient_material(self):
        white_bishops = self.white_dark_bishops + self.white_light_bishops
        black_bishops = self.black_dark_bishops + self.black_light_bishops

        if self.white_queens == 0 and self.black_queens == 0 and self.white_rooks == 0 and self.black_rooks == 0 \
                and self.white_pawns == 0 and self.black_pawns == 0:
            # check for two kings
            if white_bishops == 0 and black_bishops == 0 and self.white_knights == 0 and self.black_knights == 0:
                return True
            # check for two kings and white knight
            elif white_bishops == 0 and black_bishops == 0 and self.white_knights == 1 and self.black_knights == 0:
                return True
            # check for two kings and black knight
            elif white_bishops == 0 and black_bishops == 0 and self.white_knights == 0 and self.black_knights == 1:
                return True
            # check for two kings and white bishop
            elif white_bishops == 1 and black_bishops == 0 and self.white_knights == 0 and self.black_knights == 0:
                return True
            # check for two kings and black bishop
            elif white_bishops == 0 and black_bishops == 1 and self.white_knights == 0 and self.black_knights == 0:
                return True
            # check for two kings and two bishops(same colored)
            elif self.white_dark_bishops == 1 and self.black_dark_bishops == 1 and self.white_knights == 0 \
                    and self.black_knights == 0:
                return True
            # check for two kings and two bishops(same colored)
            elif self.white_light_bishops == 1 and self.black_light_bishops == 1 and self.white_knights == 0 \
                    and self.black_knights == 0:
                return True
            else:
                return False

    def draw_by_threefold_repetition(self):
        if len(self.moveList) >= 7:
            if self.moveList[-1] == self.moveList[-5]:
                if self.moveList[-2] == self.moveList[-6]:
                    if self.moveList[-3] == self.moveList[-7]:
                        return True
        return False

    def change_turn(self):
        self.turn = not self.turn

    def get_all_valid_moves(self, color=None):
        if not color:
            if self.turn:
                color = CHESS_WHITE
            else:
                color = CHESS_BLACK

        validMoves = list()
        for row in self.pieces:
            for piece in row:
                if piece != '.' and piece.color == color:
                    if piece.role in ['P', 'p'] and (self.moveCount - 1) in self.en_passants.keys():
                        # noinspection PyArgumentList
                        validMoves.extend(piece.get_valid_moves(self, self.en_passants[self.moveCount - 1]))
                    else:
                        validMoves.extend(piece.get_valid_moves(self))
        return validMoves

    def get_all_standard_moves(self):
        moveList = self.get_all_valid_moves()
        move_dict = {}
        l1 = []
        for move in moveList:
            mv = ''
            if move in ['O-O-O', 'O-O']:
                move_dict[move] = move

            if move[0] != 'P':
                mv += move[0]

            pattern = move[:2] + '...' + move[5:]
            l1.clear()
            for i in moveList:
                l1.extend(re.findall(pattern, i))
            if len(l1) > 1:
                if l1[0][2] != l1[1][2]:
                    mv += move[2]
                else:
                    mv += move[3]

            if 'x' in move:
                if move[0] == 'P':
                    mv += move[2]
                mv += 'x'
            mv += move[5:7]

            if move[-2] == '=':
                mv += move[-2:]

            move_dict[mv] = move
        return move_dict

    # Use and Implementation remained.
    def evaluate_advantage(self):
        pass

    def get_score(self):
        whiteScore = 0
        blackScore = 0

        whiteScore += self.white_pawns * Pawn.Points
        whiteScore += self.white_dark_bishops * Bishop.Points
        whiteScore += self.white_light_bishops * Bishop.Points
        whiteScore += self.white_knights * Knight.Points
        whiteScore += self.white_rooks * Rook.Points
        whiteScore += self.white_queens * Queen.Points
        whiteScore += self.white_kings * King.Points

        blackScore += self.black_pawns * Pawn.Points
        blackScore += self.black_dark_bishops * Bishop.Points
        blackScore += self.black_light_bishops * Bishop.Points
        blackScore += self.black_knights * Knight.Points
        blackScore += self.black_rooks * Rook.Points
        blackScore += self.black_queens * Queen.Points
        blackScore += self.black_kings * King.Points

        return whiteScore, blackScore

    def draw_by_stalemate(self):
        if not self.get_all_valid_moves() and not self.is_check():
            return True
        return False

    def win_by_resignation(self):
        if self.winner is not None:
            return True
        return False

    def request_draw(self):
        self.draw_accepted = True

    def resign(self):
        if self.turn:
            self.winner = CHESS_BLACK
        else:
            self.winner = CHESS_WHITE
