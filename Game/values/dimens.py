import pygame

# Window size of user
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = int(info.current_w), int(info.current_h * 0.92)

btnPadding = 15
padding = 15
dialogPad = padding//2

coordinates = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
letters = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

# Dimensions of square
SquareDimen = (HEIGHT - 2 * padding) // 8
# Dimensions of pieces
PieceDimen = int(SquareDimen * 0.95)

# Title
TitleStartX = 0
TitleStartY = 0
TitleLenX = int(WIDTH * 0.25)
TitleLenY = int(HEIGHT * 0.15)

# Menu tab
MenuStartX = TitleStartX
MenuStartY = TitleStartY + TitleLenY
MenuLenX = TitleLenX
MenuLenY = HEIGHT - TitleLenY - int(HEIGHT * 0.3)

# Menu Buttons

MenuBtnLeftPad = 50
MenuBtnFntSize = 25
MenuBtnHeight = 32
MenuBtnWidth = TitleLenX - 2 * MenuBtnLeftPad
ArrowBtnLenX = SquareDimen//2
ArrowBtnLenY = SquareDimen//2

# Board
BoardStartX = TitleStartX + TitleLenX
BoardStartY = 0
BoardLenX = 2*padding + 8*SquareDimen
BoardLenY = HEIGHT

# Player 1
P1StartX = 0
P1StartY = int(HEIGHT * 0.7)
P1LenX = TitleLenX
P1LenY = int(HEIGHT * 0.15)

# Player 2
P2StartX = 0
P2StartY = int(HEIGHT * 0.85)
P2LenX = TitleLenX
P2LenY = int(HEIGHT * 0.16)

# Evaluation Bar (Only visible during analysis.)
EvalBarStartX = BoardStartX + BoardLenX - padding
EvalBarStartY = 0
EvalBarWidth = 25
EvalBarLenX = padding + EvalBarWidth + padding
EvalBarLenY = HEIGHT

# Displays user's move and best move
InfoStartX = EvalBarStartX + EvalBarLenX
InfoStartY = 0
InfoLenX = WIDTH - EvalBarStartX - EvalBarLenX
InfoLenY = padding + 2*SquareDimen

# Previous moves tab
FENStartX = EvalBarStartX + EvalBarLenX
FENStartY = InfoStartY + InfoLenY
FENLenX = WIDTH - FENStartX
FENLenY = HEIGHT

# Alert Dialog (Outer box)
AlertDialogStartX = int(BoardStartX+padding+1.5*SquareDimen)
AlertDialogStartY = int(BoardStartY+padding+2.5*SquareDimen)
AlertDialogLenX = int(5*SquareDimen)
AlertDialogLenY = int(3*SquareDimen)
DialogTitleHeight = SquareDimen//2

# Alert Dialog (Inner Box)
DialogInX = AlertDialogStartX+dialogPad
DialogInY = AlertDialogStartY+dialogPad+DialogTitleHeight
DialogInLenX = AlertDialogLenX - 2 * dialogPad
DialogInLenY = AlertDialogLenY - 2 * dialogPad - DialogTitleHeight
