from .values.dimens import *
from .values.colors import CHESS_WHITE, AlertDialogBG, AlertDialogFG
from .values.assets import gameFont


class AlertDialog:
    def __init__(self, win, alertText, title='Chess', positiveBtn=None, negativeBtn=None):
        self.win = win
        self.alertText = alertText
        self.title = title
        self.pBtn = positiveBtn
        self.nBtn = negativeBtn
        self.pBtnRect = None
        self.nBtnRect = None

    def show(self):
        pygame.draw.rect(self.win, AlertDialogBG, ((AlertDialogStartX, AlertDialogStartY),
                                                   (AlertDialogLenX, AlertDialogLenY)),
                         border_radius=DialogTitleHeight // 2)
        pygame.draw.rect(self.win, AlertDialogFG,
                         ((DialogInX, DialogInY), (DialogInLenX, DialogInLenY)),
                         border_bottom_left_radius=DialogTitleHeight // 2,
                         border_bottom_right_radius=DialogTitleHeight // 2)

        self.drawText(self.title, 50, AlertDialogStartX + AlertDialogLenX // 2, AlertDialogStartY +
                      (dialogPad + DialogTitleHeight) // 2, CHESS_WHITE, font=gameFont, centre='XY')

        if '*' not in self.alertText:
            self.drawText(self.alertText, 40, DialogInX + DialogInLenX // 2, DialogInY + SquareDimen,
                          CHESS_WHITE, centre=True)
        else:
            texts = self.alertText.split('*')
            length = SquareDimen // (len(texts) + (len(texts) % 2))
            for txt in texts:
                self.drawText(txt, 30, DialogInX + DialogInLenX // 2, DialogInY + length, CHESS_WHITE, centre=True)
                length += SquareDimen // 2

        btnX = DialogInX + int(0.125 * DialogInLenX)
        btnLenY = int(DialogInLenY * 0.2)
        btnY = DialogInY + int(0.7 * DialogInLenY)
        if self.nBtn:
            btnLenX = min(int(1.5 * SquareDimen), max(SquareDimen, 30 * (len(self.nBtn) + 2)))
            self.nBtnRect = pygame.draw.rect(self.win, CHESS_WHITE, ((btnX, btnY), (btnLenX, btnLenY)),
                                             border_radius=15)
            self.drawText(self.nBtn[0], 20, btnX + btnLenX // 2, btnY + btnLenY // 2, (0, 0, 0), centre=True)
        if self.pBtn:
            btnLenX = min(int(1.5 * SquareDimen), max(SquareDimen, 30 * (len(self.pBtn) + 2)))
            self.pBtnRect = pygame.draw.rect(self.win, CHESS_WHITE, ((btnX + DialogInLenX // 2, btnY),
                                                                     (btnLenX, btnLenY)), border_radius=15)
            self.drawText(self.pBtn[0], 20, btnX + DialogInLenX // 2 + btnLenX // 2, btnY + btnLenY // 2, (0, 0, 0),
                          centre=True)
        pygame.display.update()

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
