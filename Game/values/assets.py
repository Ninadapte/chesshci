import pygame

from Game.values.dimens import PieceDimen, TitleLenX, TitleLenY, HEIGHT, WIDTH, ArrowBtnLenX, ArrowBtnLenY

# Fonts
gameFont = "Assets/product_sans_regular.ttf"
gameFontBold = "Assets/product_sans_bold.ttf"

brdFileName = 'saved_chess_board.pickle'

MODE_VOICE = 1
MODE_GESTURES = 0

# Pieces
# 345, 148
w = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

BackArrow = pygame.transform.scale(pygame.image.load('assets/back.png'), (ArrowBtnLenX, ArrowBtnLenY))
ForwardArrow = pygame.transform.scale(pygame.image.load('assets/forward.png'), (ArrowBtnLenX, ArrowBtnLenY))

title = pygame.transform.scale(pygame.image.load('assets/title.png'), (TitleLenX, TitleLenY))
WHITE_PAWN = pygame.transform.scale(pygame.image.load('assets/wpawn.png'), (PieceDimen, PieceDimen))
WHITE_KING = pygame.transform.scale(pygame.image.load('assets/wking.png'), (PieceDimen, PieceDimen))
WHITE_QUEEN = pygame.transform.scale(pygame.image.load('assets/wqueen.png'), (PieceDimen, PieceDimen))
WHITE_BISHOP = pygame.transform.scale(pygame.image.load('assets/wbishop.png'), (PieceDimen, PieceDimen))
WHITE_KNIGHT = pygame.transform.scale(pygame.image.load('assets/wknight.png'), (PieceDimen, PieceDimen))
WHITE_ROOK = pygame.transform.scale(pygame.image.load('assets/wrook.png'), (PieceDimen, PieceDimen))

BLACK_PAWN = pygame.transform.scale(pygame.image.load('assets/bpawn.png'), (PieceDimen, PieceDimen))
BLACK_KING = pygame.transform.scale(pygame.image.load('assets/bking.png'), (PieceDimen, PieceDimen))
BLACK_QUEEN = pygame.transform.scale(pygame.image.load('assets/bqueen.png'), (PieceDimen, PieceDimen))
BLACK_BISHOP = pygame.transform.scale(pygame.image.load('assets/bbishop.png'), (PieceDimen, PieceDimen))
BLACK_KNIGHT = pygame.transform.scale(pygame.image.load('assets/bknight.png'), (PieceDimen, PieceDimen))
BLACK_ROOK = pygame.transform.scale(pygame.image.load('assets/brook.png'), (PieceDimen, PieceDimen))
