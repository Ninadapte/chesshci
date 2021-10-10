import os
import pickle
import time

import pygame.display

from Chess.static import get_row_col
from ListView import ListView
from fruit import Fruit
from .values.colors import *
from .values.dimens import *
from .values.assets import *
from .alertDialog import AlertDialog
from .values.assets import brdFileName


def getBoardRowColFromPos(pos):
    row, col = pos
    if BoardStartX + padding < row < BoardStartX + padding + 8 * SquareDimen:
        if padding < col < HEIGHT - padding - 1:
            return min((row - BoardStartX - padding) // SquareDimen, 7), min((col - padding) // SquareDimen, 7)
    return -1, -1


class UI:
    # MODE_VOICE = 1
    # MODE_GESTURES = 0
    def __init__(self, win, chessBoard, gameMode=MODE_VOICE, p1Name="Player 1", p2Name="Player 2"):

        self.running = True

        self.win = win
        self.chessBoard = chessBoard
        self.selectedPiece = None
        self.moveLoc = {}
        self.takesLoc = {}
        self.castleLoc = {}
        self.promotionMove = None
        self.dialog = False

        self.gameMode = gameMode

        self.p1Name = p1Name
        self.p2Name = p2Name

        self.fruit = Fruit(self.chessBoard.moveList, BorderColor, 60, FENLenX - 40, 2, 2, 5)
        self.listview = ListView(FENStartX + 20, FENStartY + 50, FENLenX - 40, HEIGHT - FENStartY - 100,
                                 self.fruit, CHESS_BLACK, CHESS_WHITE, 5, CHESS_BLACK, 3, win)

    def drawDisplay(self):
        # self.win.fill(MenuColor)
        self.updateBoard()
        pygame.display.update()

    def updateBoard(self):
        self.drawTitle()
        self.drawMenu()
        pygame.draw.rect(self.win, BorderColor, (BoardStartX, BoardStartY, BoardLenX, BoardLenY))
        for i in range(8):
            for j in range(8):
                x = BoardStartX + padding + j * SquareDimen
                y = BoardStartY + padding + i * SquareDimen
                if (i + j) % 2:
                    pygame.draw.rect(self.win, CHESS_BLACK, ((x, y), (SquareDimen, SquareDimen)))
                else:
                    pygame.draw.rect(self.win, CHESS_WHITE, ((x, y), (SquareDimen, SquareDimen)))

        self.drawUIMoves()
        self.drawPieces()
        self.drawCoordinates()
        self.drawPromotion()
        self.drawPlayers()
        self.drawEvalBar()
        self.drawInformation()
        self.drawFEN()
        self.isGameEnd()
        pygame.display.update()

    def drawTitle(self):
        pygame.draw.rect(self.win, CHESS_WHITE, ((TitleStartX, TitleStartY), (TitleLenX, TitleLenY)))
        self.win.blit(title, (TitleStartX, TitleStartY))

    def drawMenu(self):
        pygame.draw.rect(self.win, MenuColor, ((MenuStartX, MenuStartY), (MenuLenX, MenuLenY)))

        txtX = (TitleStartX + TitleLenX) // 2
        txtY = MenuStartY + btnPadding * 3 + MenuBtnHeight

        if self.chessBoard.moveList:
            pygame.draw.rect(self.win, CHESS_WHITE, (((txtX - btnPadding - ArrowBtnLenX, MenuStartY + btnPadding),
                                                      (ArrowBtnLenX, ArrowBtnLenY))), 0, 8)
            self.win.blit(BackArrow, (txtX - btnPadding - ArrowBtnLenX, MenuStartY + btnPadding))

        if self.chessBoard.poppedMoveList:
            pygame.draw.rect(self.win, CHESS_WHITE, ((txtX + btnPadding, MenuStartY + btnPadding),
                                                     (ArrowBtnLenX, ArrowBtnLenY)), 0, 8)

            self.win.blit(ForwardArrow, (txtX + btnPadding, MenuStartY + btnPadding))

        # Buttons
        buttonList = ['New Game', 'Save Game', 'Settings']
        if self.gameMode:
            buttonList += ['Use Hand Gestures']
        else:
            buttonList += ['Use Voice Commands']
        buttonList += ['Request Draw', 'Resign']

        for buttonTxt in buttonList:
            pygame.draw.rect(self.win, MenuBtnColor, ((MenuStartX + MenuBtnLeftPad, txtY), (MenuBtnWidth, MenuBtnHeight)
                                                      ), 0, 8)
            self.drawText(buttonTxt, MenuBtnFntSize, txtX, txtY, MenuBtnTextColor, centre='X')
            txtY += MenuBtnHeight + btnPadding

        # Placing Quit button at end.
        txtY = MenuStartY + MenuLenY - btnPadding - MenuBtnHeight
        pygame.draw.rect(self.win, MenuBtnColor, ((MenuBtnLeftPad, txtY), (MenuBtnWidth, MenuBtnHeight)), 0, 8)
        self.drawText('Quit', MenuBtnFntSize, txtX, txtY, MenuBtnTextColor, centre='X')
        txtY += MenuBtnHeight + btnPadding

    def drawCoordinates(self):
        font = pygame.font.Font(gameFontBold, 20)
        for number in coordinates.keys():
            if number % 2:
                clr = CHESS_WHITE
            else:
                clr = CHESS_BLACK

            text = font.render(str(coordinates[number]), True, clr)
            textRect = text.get_rect()
            X = BoardStartX + padding + number * SquareDimen - textRect.center[0] - 3
            Y = 8 * SquareDimen + padding - textRect.center[1]
            textRect.center = (X, Y)
            self.win.blit(text, textRect)

            text = font.render(str(number), True, clr)
            textRect = text.get_rect()
            X = BoardStartX + padding + textRect.center[0] + 3
            Y = padding + (8 - number) * SquareDimen + textRect.center[1]
            textRect.center = (X, Y)
            self.win.blit(text, textRect)

    def drawPieces(self):
        FEN = self.chessBoard.pieces
        for row in FEN:
            for piece in row:
                if piece != '.':
                    self.showPiece(piece.role, piece.row, piece.col)
        return

    def showPiece(self, piece, row, col):
        checkX = BoardStartX + padding + col * SquareDimen
        checkY = BoardStartY + padding + abs(7 - row) * SquareDimen
        X = checkX + (SquareDimen - PieceDimen) // 2
        Y = checkY + (SquareDimen - PieceDimen) // 2

        if piece == 'TAKE':
            pygame.draw.circle(self.win, TakeColor, (checkX + SquareDimen // 2, checkY + SquareDimen // 2),
                               SquareDimen // 2, 7)
        elif piece == 'MOVE':
            pygame.draw.circle(self.win, MoveColor, (checkX + SquareDimen // 2, checkY + SquareDimen // 2),
                               SquareDimen // 9)
        elif piece == 'CASTLE':
            pygame.draw.circle(self.win, CastleColor, (checkX + SquareDimen // 2, checkY + SquareDimen // 2),
                               SquareDimen // 9)
        elif piece == 'SELECT':
            pygame.draw.rect(self.win, SelectColor, ((checkX, checkY), (SquareDimen, SquareDimen)))

        elif piece == 'P':
            self.win.blit(WHITE_PAWN, (X, Y))
        elif piece == 'p':
            self.win.blit(BLACK_PAWN, (X, Y))

        elif piece == 'K':
            if self.chessBoard.is_check() and self.chessBoard.turn:
                pygame.draw.rect(self.win, CheckColor, ((checkX, checkY), (SquareDimen, SquareDimen)))
            self.win.blit(WHITE_KING, (X, Y))
        elif piece == 'k':
            if self.chessBoard.is_check() and not self.chessBoard.turn:
                pygame.draw.rect(self.win, CheckColor, ((checkX, checkY), (SquareDimen, SquareDimen)))
            self.win.blit(BLACK_KING, (X, Y))

        elif piece == 'Q':
            self.win.blit(WHITE_QUEEN, (X, Y))
        elif piece == 'q':
            self.win.blit(BLACK_QUEEN, (X, Y))

        elif piece == 'B':
            self.win.blit(WHITE_BISHOP, (X, Y))
        elif piece == 'b':
            self.win.blit(BLACK_BISHOP, (X, Y))

        elif piece == 'R':
            self.win.blit(WHITE_ROOK, (X, Y))
        elif piece == 'r':
            self.win.blit(BLACK_ROOK, (X, Y))

        elif piece == 'N':
            self.win.blit(WHITE_KNIGHT, (X, Y))
        elif piece == 'n':
            self.win.blit(BLACK_KNIGHT, (X, Y))

    def drawPlayer1(self, turn=False):
        pygame.draw.rect(self.win, CHESS_WHITE, (P1StartX, P1StartY, P1LenX, P1LenY))
        pad = int(P1LenY * 0.1)
        if turn:
            pygame.draw.rect(self.win, turnColor, (P1StartX, P1StartY, P1LenY, P1LenY))
        pygame.draw.rect(self.win, CHESS_BLACK, (P1StartX + pad, P1StartY + pad, SquareDimen, SquareDimen))
        self.win.blit(WHITE_KING, (P1StartX + pad, P1StartY + pad))

        self.drawText(self.p1Name, 36, P1StartX + 3 * pad + SquareDimen, P1StartY + (padding + SquareDimen) // 2,
                      CHESS_BLACK, centre='Y', font=gameFontBold)
        # self.drawText(self.p1Rating, 22, P1StartX + 3 * pad + SquareDimen, P1StartY + 4 * pad,
        # RatingFC, RatingBC, font=gameFontBold)

    def drawPlayer2(self, turn=False):
        pygame.draw.rect(self.win, CHESS_BLACK, (P2StartX, P2StartY, P2LenX, P2LenY))
        pad = int(P2LenY * 0.1)
        if turn:
            pygame.draw.rect(self.win, turnColor, (P2StartX, P2StartY, P1LenY, P1LenY))
        pygame.draw.rect(self.win, CHESS_WHITE, (P2StartX + pad, P2StartY + pad, SquareDimen, SquareDimen))
        self.win.blit(BLACK_KING, (P2StartX + pad, P2StartY + pad))

        self.drawText(self.p2Name, 36, P2StartX + 3 * pad + SquareDimen,
                      P2StartY + (padding + SquareDimen) // 2,
                      CHESS_WHITE, centre='Y', font=gameFontBold)
        # self.drawText(self.p2Rating, 22, P2StartX + 3 * pad + SquareDimen, P2StartY + 4 * pad,
        # RatingFC, RatingBC, font=gameFontBold)

    def drawPlayers(self):
        if self.chessBoard.turn:
            self.drawPlayer1(turn=True)
            self.drawPlayer2()
        else:
            self.drawPlayer1()
            self.drawPlayer2(turn=True)

    def isGameEnd(self):
        # Checkmate
        if self.chessBoard.is_checkmate():

            # Black won by checkmate.
            if self.chessBoard.turn:
                self.showDialog("Checkmate*Black Won !", pBtn=("New Game", self.newGame),
                                nBtn=("Quit", self.quit))

            # White won by checkmate.
            else:
                self.showDialog("Checkmate*White Won !", pBtn=("New Game", self.newGame),
                                nBtn=("Quit", self.quit))
            return True

        # Draw by Threefold repetition.
        elif self.chessBoard.draw_by_threefold_repetition():
            self.showDialog("Game drawn by*Threefold repetition !", pBtn=("New Game", self.newGame),
                            nBtn=("Quit", self.quit))
            return True

        # Draw by Insufficient material.
        elif self.chessBoard.draw_by_insufficient_material():
            self.showDialog("Game drawn by*Insufficient material !", pBtn=("New Game", self.newGame),
                            nBtn=("Quit", self.quit))
            return True

        # Draw by Stalemate.
        elif self.chessBoard.draw_by_stalemate():
            self.showDialog("Game drawn by*Stalemate !", pBtn=("New Game", self.newGame),
                            nBtn=("Quit", self.quit))
            return True

        # Win by resignation.
        elif self.chessBoard.win_by_resignation():
            # Black won by resignation.
            if self.chessBoard.winner == CHESS_BLACK:
                self.showDialog("Resignation*Black won !", pBtn=("New Game", self.newGame),
                                nBtn=("Quit", self.quit))

            # White won by resignation.
            else:
                self.showDialog("Resignation*White won !", pBtn=("New Game", self.newGame),
                                nBtn=("Quit", self.quit))
            return True

        # Draw accepted.
        elif self.chessBoard.draw_accepted:
            self.showDialog("Game drawn !*Draw accepted.", pBtn=("New Game", self.newGame),
                            nBtn=("Quit", self.quit))
            return True
        return False

    def drawEvalBar(self):
        pygame.draw.rect(self.win, CHESS_BLACK,
                         (EvalBarStartX + padding, EvalBarStartY, EvalBarLenX - padding, EvalBarLenY))

    def drawInformation(self):
        pygame.draw.rect(self.win, CHESS_BLACK, (InfoStartX, InfoStartY, InfoLenX, InfoLenY))

    def drawFEN(self):
        pygame.draw.rect(self.win, FENColor, (FENStartX, FENStartY, FENLenX, FENLenY))
        whiteMoveList = []
        blackMoveList = []
        for x in range(len(self.chessBoard.moveList)):
            if x % 2 == 0:
                whiteMoveList.append(self.chessBoard.moveList[x])
            else:
                blackMoveList.append(self.chessBoard.moveList[x])

        pygame.draw.rect(self.win, FENColor, (FENStartX, FENStartY, FENLenX, FENLenY))
        self.fruit.updatemainList(blackMoveList)
        self.fruit.UpdateData(whiteMoveList)

    def newGame(self):
        self.chessBoard.__init__(self.chessBoard.Board_type)
        self.__init__(self.win, self.chessBoard, self.p1Name, self.p2Name)

    def menuClick(self, pos):
        row, col = pos
        if MenuStartX < row < MenuStartX + MenuLenX and MenuStartY < col < MenuStartY + MenuLenY:
            centre = MenuStartX + MenuLenX // 2

            # Backward and forward move
            if 0 < col - MenuStartY - btnPadding < ArrowBtnLenY:
                if centre - btnPadding - ArrowBtnLenX < row < centre - btnPadding:
                    self.clearUIMoves()
                    self.chessBoard.move_back()
                    self.updateBoard()

                elif 0 < row - centre - btnPadding < ArrowBtnLenX:
                    self.clearUIMoves()
                    self.chessBoard.move()
                    self.updateBoard()
            Y = MenuStartY + btnPadding * 3 + MenuBtnHeight

            if 0 < row - MenuStartX - MenuBtnLeftPad < MenuBtnWidth:
                # Quit
                if MenuStartY + MenuLenY - btnPadding - MenuBtnHeight < col < MenuStartY + MenuLenY - btnPadding:
                    self.showDialog("Do you really want to quit?*The game will be saved.",
                                    pBtn=("Yes", self.quit), nBtn=("No", self.doNothing))

                # New Game.
                if Y < col < Y + MenuBtnHeight:
                    self.showDialog('Do you really want to*start a new game?', pBtn=('Yes', self.newGame),
                                    nBtn=('No', self.doNothing))
                Y += btnPadding + MenuBtnHeight

                # Game saved.
                if Y < col < Y + MenuBtnHeight:
                    self.saveBoard()
                    self.showDialog('Game Saved.')
                Y += btnPadding + MenuBtnHeight

                # Settings.
                if Y < col < Y + MenuBtnHeight:
                    print("Settings not implemented.")
                Y += btnPadding + MenuBtnHeight

                # Continue with friend/bot.
                if Y < col < Y + MenuBtnHeight:
                    if self.gameMode:
                        self.showDialog("Do you want to continue*playing the game with*Hand gestures?",
                                        pBtn=("Yes", self.switchGameMode), nBtn=("No", self.doNothing))
                    else:
                        self.showDialog("Do you want to continue*playing the game with*voice commands?",
                                        pBtn=("Yes", self.switchGameMode), nBtn=("No", self.doNothing))
                Y += btnPadding + MenuBtnHeight

                # Request draw.
                if Y < col < Y + MenuBtnHeight:
                    self.showDialog("Do you really want to*request a draw?",
                                    pBtn=("Yes", self.chessBoard.request_draw), nBtn=("No", self.doNothing))
                Y += btnPadding + MenuBtnHeight

                # resign.
                if Y < col < Y + MenuBtnHeight:
                    self.showDialog("Do you really want to*resign form game?", pBtn=("Yes", self.chessBoard.resign),
                                    nBtn=("No", self.doNothing))

    def switchGameMode(self):
        message = "*Switching "
        if self.gameMode:
            message += "game mode to*Hand gestures!"
        else:
            message += "game mode to*Voice commands!"
        self.gameMode = not self.gameMode

        self.showDialog(message)

    def click(self, pos):
        pos = getBoardRowColFromPos(pos)
        if pos != (-1, -1):
            col, row = pos
            row = abs(7 - row)
        else:
            self.clearUIMoves()
            return

        if self.promotionMove:
            if row == 3 and col == 3:
                self.chessBoard.move(self.promotionMove + 'B')
            if row == 3 and col == 4:
                self.chessBoard.move(self.promotionMove + 'N')
            if row == 4 and col == 3:
                self.chessBoard.move(self.promotionMove + 'Q')
            if row == 4 and col == 4:
                self.chessBoard.move(self.promotionMove + 'R')
            self.clearUIMoves()
            self.updateBoard()
            return

        clickedPiece = self.chessBoard.pieces[row][col]
        my_color = CHESS_BLACK
        if self.chessBoard.turn:
            my_color = CHESS_WHITE

        # Clicked piece is empty.
        if clickedPiece == '.':
            if self.selectedPiece:
                if (row, col) in self.moveLoc.keys():
                    if '=' in self.moveLoc[(row, col)]:
                        self.promotionMove = self.moveLoc[(row, col)][:-1]
                        self.updateBoard()
                        return
                    else:
                        self.chessBoard.move(self.moveLoc[(row, col)])
                elif (row, col) in self.takesLoc.keys():  # En-passant is take with clicked position = empty.
                    self.chessBoard.move(self.takesLoc[(row, col)])
                elif (row, col) in self.castleLoc.keys():
                    self.chessBoard.move(self.castleLoc[(row, col)])
            else:
                return

        # Clicked piece is of opponent's color.
        elif clickedPiece.color != my_color:
            if self.selectedPiece:
                if (row, col) in self.takesLoc.keys():
                    if '=' in self.takesLoc[(row, col)]:
                        self.promotionMove = self.takesLoc[(row, col)][:-1]
                        self.updateBoard()
                        return
                    else:
                        self.chessBoard.move(self.takesLoc[(row, col)])
            else:
                return

        # Clicked piece is of turn's color.
        else:
            if not self.selectedPiece:
                self.setUIMoves(clickedPiece)
            if clickedPiece != self.selectedPiece:
                self.clearUIMoves()
                self.setUIMoves(clickedPiece)
            self.updateBoard()
            return
        self.clearUIMoves()
        self.updateBoard()

    def setUIMoves(self, clickedPiece):
        self.selectedPiece = clickedPiece
        board = self.chessBoard
        if self.selectedPiece.role in ['P', 'p'] and (board.moveCount - 1) in board.en_passants.keys():
            moves = clickedPiece.get_valid_moves(board, board.en_passants[board.moveCount - 1])
        else:
            moves = clickedPiece.get_valid_moves(board)
        for mv in moves:
            if 'x' in mv:
                self.takesLoc[get_row_col(mv[5:7])] = mv
            elif '-' in mv:
                row = 7
                if board.turn:
                    row = 0
                if mv == 'O-O':
                    self.castleLoc[(row, 6)] = mv
                if mv == 'O-O-O':
                    self.castleLoc[(row, 2)] = mv
            else:
                self.moveLoc[get_row_col(mv[5:7])] = mv

    def drawUIMoves(self):
        for move in self.moveLoc.keys():
            self.showPiece('MOVE', move[0], move[1])
        for take in self.takesLoc.keys():
            self.showPiece('TAKE', take[0], take[1])
        for castle in self.castleLoc.keys():
            self.showPiece('CASTLE', castle[0], castle[1])
        if self.selectedPiece:
            self.showPiece('SELECT', self.selectedPiece.row, self.selectedPiece.col)

    def clearUIMoves(self):
        self.promotionMove = None
        self.selectedPiece = None
        self.moveLoc.clear()
        self.takesLoc.clear()
        self.castleLoc.clear()

    def drawPromotion(self):
        if self.promotionMove:
            X = BoardStartX + padding + 3 * SquareDimen
            Y = BoardStartY + padding + 3 * SquareDimen
            pygame.draw.rect(self.win, promotionColor, (X, Y, 2 * SquareDimen, 2 * SquareDimen))
            if self.chessBoard.turn:
                self.showPiece('Q', 4, 3)
                self.showPiece('R', 4, 4)
                self.showPiece('B', 3, 3)
                self.showPiece('N', 3, 4)
            else:
                self.showPiece('q', 4, 3)
                self.showPiece('r', 4, 4)
                self.showPiece('b', 3, 3)
                self.showPiece('n', 3, 4)

    def drawText(self, text, size, txtX, txtY, color, colorBg=None, font=gameFont, centre=False):
        Txt = pygame.font.Font(font, size).render(text, True, color, colorBg)
        nameRect = Txt.get_rect()
        if centre in [False, 'X', 'Y']:
            if centre == 'Y':
                txtX += nameRect.center[0]
            elif centre == 'X':
                txtY += nameRect.center[1]
            else:
                txtX += nameRect.center[0]
                txtY += nameRect.center[1]
        nameRect.center = (txtX, txtY)
        self.win.blit(Txt, nameRect)

    def quit(self):
        # noinspection PyBroadException
        try:
            if self.isGameEnd():
                self.delete_saved_board()
            else:
                self.saveBoard()
        except:
            self.delete_saved_board()
        self.running = False

    def saveBoard(self):
        with open(brdFileName, 'wb') as brdFile:
            pickle.dump(self.chessBoard, brdFile)

    def delete_saved_board(self):
        if os.path.exists(brdFileName):
            os.remove(brdFileName)
            self.chessBoard = None

    def doNothing(self):
        pass

    def showDialog(self, text, winTitle="Chess", pBtn=None, nBtn=None, sleepTime=1):
        self.dialog = AlertDialog(self.win, text, winTitle, pBtn, nBtn)
        self.dialog.show()
        if pBtn == nBtn is None:
            time.sleep(sleepTime)
            self.removeDialog()

    def dialogClick(self, pos):
        if self.dialog.pBtn and pygame.Rect.collidepoint(self.dialog.pBtnRect, pos):
            self.dialog.pBtn[1]()
        elif self.dialog.nBtn and pygame.Rect.collidepoint(self.dialog.nBtnRect, pos):
            self.dialog.nBtn[1]()
        self.removeDialog()

    def removeDialog(self):
        self.dialog = None
        # Error can occur as objects are deleted when quit() is called.
        # noinspection PyBroadException
        try:
            self.updateBoard()
        except:
            pass
