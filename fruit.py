import pygame


class Fruit:
    def __init__(self, ls, itemborderColor, Ih, W, itemTopmargin, itemBorderThickness, itemRadius):
        self.whiteList = ls
        self.ItemBorderColor = itemborderColor
        self.Ih = Ih
        self.W = W
        self.blacklist = []
        self.itemTopmargin = itemTopmargin
        self.itemBorderThickness = itemBorderThickness
        self.itemRadius = itemRadius
        self.PieceDimen = int(self.Ih / 2)
        self.WHITE_PAWN = pygame.transform.scale(pygame.image.load('assets/wpawn.png'),
                                                 (self.PieceDimen, self.PieceDimen))
        self.WHITE_KING = pygame.transform.scale(pygame.image.load('assets/wking.png'),
                                                 (self.PieceDimen, self.PieceDimen))
        self.WHITE_QUEEN = pygame.transform.scale(pygame.image.load('assets/wqueen.png'),
                                                  (self.PieceDimen, self.PieceDimen))
        self.WHITE_BISHOP = pygame.transform.scale(pygame.image.load('assets/wbishop.png'),
                                                   (self.PieceDimen, self.PieceDimen))
        self.WHITE_KNIGHT = pygame.transform.scale(pygame.image.load('assets/wknight.png'),
                                                   (self.PieceDimen, self.PieceDimen))
        self.WHITE_ROOK = pygame.transform.scale(pygame.image.load('assets/wrook.png'),
                                                 (self.PieceDimen, self.PieceDimen))

        self.BLACK_PAWN = pygame.transform.scale(pygame.image.load('assets/bpawn.png'),
                                                 (self.PieceDimen, self.PieceDimen))
        self.BLACK_KING = pygame.transform.scale(pygame.image.load('assets/bking.png'),
                                                 (self.PieceDimen, self.PieceDimen))
        self.BLACK_QUEEN = pygame.transform.scale(pygame.image.load('assets/bqueen.png'),
                                                  (self.PieceDimen, self.PieceDimen))
        self.BLACK_BISHOP = pygame.transform.scale(pygame.image.load('assets/bbishop.png'),
                                                   (self.PieceDimen, self.PieceDimen))
        self.BLACK_KNIGHT = pygame.transform.scale(pygame.image.load('assets/bknight.png'),
                                                   (self.PieceDimen, self.PieceDimen))
        self.BLACK_ROOK = pygame.transform.scale(pygame.image.load('assets/brook.png'),
                                                 (self.PieceDimen, self.PieceDimen))

    def attachCallback(self, callback):
        self.callback = callback

    def append(self, item):
        self.whiteList.append(item)

        self.callback()

    def pop(self, pos):
        pop = self.whiteList.pop(pos)

        self.callback()
        return pop

    def length(self):
        return len(self.whiteList)

    def drawContent(self, x, y, pos, window):

        # for white
        try:
            move = str(self.whiteList[pos])
            hold = move
            move = move.split("_")

            # Handle for promotion

            if '=' not in hold:
                if move[0] == 'R':
                    window.blit(self.WHITE_ROOK, (x + self.W / 6, y + self.Ih / 4))
                elif move[0] == 'N':
                    window.blit(self.WHITE_KNIGHT, (x + self.W / 6, y + self.Ih / 4))
                elif move[0] == 'Q':
                    window.blit(self.WHITE_QUEEN, (x + self.W / 6, y + self.Ih / 4))
                elif move[0] == 'K':
                    window.blit(self.WHITE_KING, (x + self.W / 6, y + self.Ih / 4))
                elif move[0] == 'P':
                    window.blit(self.WHITE_PAWN, (x + self.W / 6, y + self.Ih / 4))
                elif move[0] == 'B':
                    window.blit(self.WHITE_BISHOP, (x + self.W / 6, y + self.Ih / 4))
            else:
                if 'R' == hold[len(hold) - 1]:

                    window.blit(self.WHITE_ROOK, (x + self.W / 6 + 50, y + self.Ih / 4))
                    window.blit(self.WHITE_PAWN, (x + 25, y + self.Ih / 4))
                elif 'N' == hold[len(hold) - 1]:
                    window.blit(self.WHITE_KNIGHT, (x + self.W / 6 + 50, y + self.Ih / 4))
                    window.blit(self.WHITE_PAWN, (x + 25, y + self.Ih / 4))
                elif 'Q' == hold[len(hold) - 1]:
                    window.blit(self.WHITE_QUEEN, (x + self.W / 6 + 50, y + self.Ih / 4))
                    window.blit(self.WHITE_PAWN, (x + 25, y + self.Ih / 4))
                elif 'K' == hold[len(hold) - 1]:
                    window.blit(self.WHITE_KING, (x + self.W / 6 + 50, y + self.Ih / 4))
                    window.blit(self.WHITE_PAWN, (x + 25, y + self.Ih / 4))

                elif 'B' == hold[len(hold) - 1]:
                    window.blit(self.WHITE_BISHOP, (x + self.W / 6 + 50, y + self.Ih / 4))
                    window.blit(self.WHITE_PAWN, (x + 25, y + self.Ih / 4))

            if move[0] == 'O-O':
                font = pygame.font.Font('freesansbold.ttf', 20)
                text = font.render(move[0], True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (x + self.W / 6 + 30, y + self.Ih / 2)
                window.blit(text, textRect)
            elif move[0] == 'O-O-O':
                font = pygame.font.Font('freesansbold.ttf', 20)
                text = font.render(move[0], True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (x + self.W / 6 + 30, y + self.Ih / 2)
                window.blit(text, textRect)
            elif 'x' in hold:
                font = pygame.font.Font('freesansbold.ttf', 20)
                toPrint = 'x' + move[2][0] + move[2][1]

                if '=' in hold:
                    toPrint = toPrint + '='
                    text = font.render(toPrint, True, (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (x + self.W / 6 + 30, y + self.Ih / 2)
                    window.blit(text, textRect)
                else:

                    text = font.render(toPrint, True, (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (x + self.W / 6 + 50, y + self.Ih / 2)
                    window.blit(text, textRect)
            elif '=' in hold:
                font = pygame.font.Font('freesansbold.ttf', 20)
                toPrint = move[2][0] + move[2][1]
                toPrint = toPrint + '='
                text = font.render(toPrint, True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (x + self.W / 6 + 30, y + self.Ih / 2)
                window.blit(text, textRect)
            else:

                font = pygame.font.Font('freesansbold.ttf', 20)
                text = font.render(move[2], True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (x + self.W / 6 + 50, y + self.Ih / 2)
                window.blit(text, textRect)
        except:
            pass
        # for black
        try:
            move = str(self.blacklist[pos])
            hold = move
            move = move.split("_")

            if '=' not in hold:
                if move[0] == 'R':
                    window.blit(self.BLACK_ROOK, (x + self.W / 2, y + self.Ih / 4))
                elif move[0] == 'N':
                    window.blit(self.BLACK_KNIGHT, (x + self.W / 2, y + self.Ih / 4))
                elif move[0] == 'Q':
                    window.blit(self.BLACK_QUEEN, (x + self.W / 2, y + self.Ih / 4))
                elif move[0] == 'K':
                    window.blit(self.BLACK_KING, (x + self.W / 2, y + self.Ih / 4))
                elif move[0] == 'P':
                    window.blit(self.BLACK_PAWN, (x + self.W / 2, y + self.Ih / 4))
                elif move[0] == 'B':
                    window.blit(self.BLACK_BISHOP, (x + self.W / 2, y + self.Ih / 4))
            else:
                if 'R' == hold[len(hold) - 1]:
                    window.blit(self.BLACK_ROOK, (x + self.W / 2 + 75, y + self.Ih / 4))
                    window.blit(self.BLACK_PAWN, (x + self.W / 2, y + self.Ih / 4))
                elif 'N' == hold[len(hold) - 1]:
                    window.blit(self.BLACK_KNIGHT, (x + self.W / 2 + 75, y + self.Ih / 4))
                    window.blit(self.BLACK_PAWN, (x + self.W / 2, y + self.Ih / 4))
                elif 'Q' == hold[len(hold) - 1]:
                    window.blit(self.BLACK_QUEEN, (x + self.W / 2 + 75, y + self.Ih / 4))
                    window.blit(self.BLACK_PAWN, (x + self.W / 2, y + self.Ih / 4))
                elif 'K' == hold[len(hold) - 1]:
                    window.blit(self.BLACK_KING, (x + self.W / 2 + 75, y + self.Ih / 4))
                    window.blit(self.BLACK_PAWN, (x + self.W / 2, y + self.Ih / 4))

                elif 'B' == hold[len(hold) - 1]:
                    window.blit(self.BLACK_BISHOP, (x + self.W / 2 + 75, y + self.Ih / 4))
                    window.blit(self.BLACK_PAWN, (x + self.W / 2, y + self.Ih / 4))

            if move[0] == 'O-O':
                font = pygame.font.Font('freesansbold.ttf', 20)
                text = font.render(move[0], True, (255, 0, 0))
                textRect = text.get_rect()
                textRect.center = (x + self.W / 2 + 30, y + self.Ih / 2)
                window.blit(text, textRect)
            elif move[0] == 'O-O-O':
                font = pygame.font.Font('freesansbold.ttf', 20)
                text = font.render(move[0], True, (255, 0, 0))
                textRect = text.get_rect()
                textRect.center = (x + self.W / 2 + 30, y + self.Ih / 2)
                window.blit(text, textRect)
            elif 'x' in hold:
                font = pygame.font.Font('freesansbold.ttf', 20)
                toPrint = 'x' + move[2][0] + move[2][1]
                if '=' in hold:
                    toPrint = toPrint + '='
                    text = font.render(toPrint, True, (255, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (x + self.W / 2 + 55, y + self.Ih / 2)
                    window.blit(text, textRect)
                else:
                    text = font.render(toPrint, True, (255, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (x + self.W / 2 + 50, y + self.Ih / 2)
                    window.blit(text, textRect)
            elif '=' in hold:
                font = pygame.font.Font('freesansbold.ttf', 20)
                toPrint = move[2][0] + move[2][1]
                toPrint = toPrint + '='
                text = font.render(toPrint, True, (255, 0, 0))
                textRect = text.get_rect()
                textRect.center = (x + self.W / 2 + 55, y + self.Ih / 2)
                window.blit(text, textRect)
            else:

                font = pygame.font.Font('freesansbold.ttf', 20)
                text = font.render(move[2], True, (255, 0, 0))
                textRect = text.get_rect()
                textRect.center = (x + self.W / 2 + 50, y + self.Ih / 2)
                window.blit(text, textRect)
        except:
            pass

    def drawBorder(self, x, y, rightP, window):
        pygame.draw.rect(window, self.ItemBorderColor, (x, y, self.W - 2 * rightP, self.Ih), self.itemBorderThickness,
                         self.itemRadius)

    def draw(self, x, y, pos, rightP, window):

        self.drawBorder(x, y, rightP, window)
        self.drawContent(x, y, pos, window)

    def UpdateData(self, ls):
        self.whiteList = ls
        self.callback()

    def updatemainList(self, ls):
        self.blacklist = ls
