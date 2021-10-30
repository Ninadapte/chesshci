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

BackArrow = pygame.transform.scale(pygame.image.load('Assets/back.png'), (ArrowBtnLenX, ArrowBtnLenY))
ForwardArrow = pygame.transform.scale(pygame.image.load('Assets/forward.png'), (ArrowBtnLenX, ArrowBtnLenY))

title = pygame.transform.scale(pygame.image.load('Assets/title.png'), (TitleLenX, TitleLenY))
WHITE_PAWN = pygame.transform.scale(pygame.image.load('Assets/wpawn.png'), (PieceDimen, PieceDimen))
WHITE_KING = pygame.transform.scale(pygame.image.load('Assets/wking.png'), (PieceDimen, PieceDimen))
WHITE_QUEEN = pygame.transform.scale(pygame.image.load('Assets/wqueen.png'), (PieceDimen, PieceDimen))
WHITE_BISHOP = pygame.transform.scale(pygame.image.load('Assets/wbishop.png'), (PieceDimen, PieceDimen))
WHITE_KNIGHT = pygame.transform.scale(pygame.image.load('Assets/wknight.png'), (PieceDimen, PieceDimen))
WHITE_ROOK = pygame.transform.scale(pygame.image.load('Assets/wrook.png'), (PieceDimen, PieceDimen))

BLACK_PAWN = pygame.transform.scale(pygame.image.load('Assets/bpawn.png'), (PieceDimen, PieceDimen))
BLACK_KING = pygame.transform.scale(pygame.image.load('Assets/bking.png'), (PieceDimen, PieceDimen))
BLACK_QUEEN = pygame.transform.scale(pygame.image.load('Assets/bqueen.png'), (PieceDimen, PieceDimen))
BLACK_BISHOP = pygame.transform.scale(pygame.image.load('Assets/bbishop.png'), (PieceDimen, PieceDimen))
BLACK_KNIGHT = pygame.transform.scale(pygame.image.load('Assets/bknight.png'), (PieceDimen, PieceDimen))
BLACK_ROOK = pygame.transform.scale(pygame.image.load('Assets/brook.png'), (PieceDimen, PieceDimen))
