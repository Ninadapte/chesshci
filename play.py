import os
import sys
import threading
import Chess
from Game import UI
from Game.values.dimens import *
from Game.values.assets import brdFileName
import cv2
import numpy as np
import Game.HandTrackingModule as htm
import time
import autopy
from win32api import GetSystemMetrics
import pickle

FPS = 60

pygame.display.set_caption("Wizard's chess")

class settings_Selector:

    # options is list of options
    def __init__(self, screen, title_pos, options_center, next_btn_pos, selector_title, options):
        self.options = options
        self.i = 0  # option no. zero is selected by default
        self.n = len(options)
        self.font = pygame.font.Font("resources/Product Sans Regular.ttf", 30)
        self.screen = screen
        self.options_pos = options_center
        self.option_selected = options[0]
        self.left_pressed = False
        self.right_pressed = False
        self.selector_title = selector_title
        self.next_btn_pos = next_btn_pos
        self.title_pos = title_pos
        self.text_surf = self.font.render(self.selector_title, True, (70, 70, 70))
        self.prev_img = pygame.image.load("images/left-arrow.png")
        self.next_img = pygame.image.load("images/right-arrow.png")
        self.prev_img = pygame.transform.scale(self.prev_img, (30, 30))
        self.next_img = pygame.transform.scale(self.next_img, (30, 30))
        self.title_width = self.text_surf.get_rect().width
        self.prev_rect = self.prev_img.get_rect(
            center=(self.title_pos[0], self.title_pos[1] + 60))
        self.next_rect = self.next_img.get_rect(center=(self.title_pos[0] + 150, self.title_pos[1] + 60))
        # selector title

        # self.text_rect = self.text_surf.get_rect(center=center)

    def draw(self):
        a = self.screen.blit(self.text_surf, (self.title_pos[0], self.title_pos[1]))
        self.screen.blit(self.prev_img, self.prev_rect)
        option = self.font.render(self.options[self.i], True, (70, 70, 70))
        # self.screen.blit(option, option.get_rect(center=(970, 325)))
        # self.screen.blit(option, option.get_rect(center=(self.options_pos[0], self.options_pos[1])))
        self.screen.blit(option, option.get_rect(center=(self.title_pos[0] + 75, self.title_pos[1] + 60)))
        self.screen.blit(self.next_img, self.next_rect)
        # pygame.display.update()
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.prev_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.left_pressed = True
            else:
                if self.left_pressed:
                    self.i = (self.i - 1) % (len(self.options))
                    self.option_selected = self.options[self.i]
                    self.left_pressed = False
                    UI.theme_selected = self.option_selected
        if self.next_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.right_pressed = True
            else:
                if self.right_pressed:
                    self.i = (self.i + 1) % (len(self.options))
                    self.option_selected = self.options[self.i]
                    self.right_pressed = False
                    UI.theme_selected = self.option_selected
class DialogueBox:
    def __init__(self, screen, pos, dimensions, color, color_title, title, dia_type, volume):
        self.screen = screen
        self.pos = pos
        self.dim = dimensions
        self.color = color
        self.color_title = color_title
        self.close_img = pygame.image.load("images/a.png")
        self.close_img_rect = self.close_img.get_rect(center=(self.pos[0] + self.dim[0] + 15, self.pos[1] + 55))
        self.close_img = pygame.transform.scale(self.close_img, (40, 40))
        self.title = title
        self.font = pygame.font.Font(UI.product_sans_path, 25)
        self.text_surf = self.font.render(self.title, True, (253, 246, 227))
        self.text_rect = self.text_surf.get_rect(center=(self.pos[0] + 190, self.pos[1] + 20))
        self.dia_type = dia_type
        self.mute_img = pygame.image.load("images/mute.png")
        self.mute_img = pygame.transform.scale(self.mute_img, (50, 50))
        self.mute_img_rect = self.mute_img.get_rect(center=(self.pos[0] + self.dim[0] + -200, self.pos[1] + 140))
        self.mute_pressed = False

        self.volume_down_img = pygame.image.load("images/volume-down.png")
        self.volume_down_img = pygame.transform.scale(self.volume_down_img, (50, 50))
        self.volume_down_img_rect = self.volume_down_img.get_rect(
            center=(self.pos[0] + self.dim[0] - 130, self.pos[1] + 80))
        self.down_pressed = False

        self.volume_up_img = pygame.image.load("images/volume-up.png")
        self.volume_up_img = pygame.transform.scale(self.volume_up_img, (50, 50))
        self.volume_up_img_rect = self.volume_up_img.get_rect(center=(self.pos[0] + 130, self.pos[1] + 80))
        self.up_pressed = False
        self.volume = volume

        self.theme_selector = settings_Selector(self.screen, (self.pos[0] + self.dim[0] + -275, self.pos[1] + 180),
                                                (860, 500), (420, 500), "--Themes--",
                                                ['Classic', 'Blue', 'Red '])

    def rects(self):
        pygame.draw.rect(self.screen, self.color, (self.pos[0], self.pos[1], self.dim[0], self.dim[1] - 145),
                         border_top_left_radius=5, border_top_right_radius=5,
                         border_bottom_left_radius=5, border_bottom_right_radius=5)

        pygame.draw.rect(self.screen, (253, 246, 227),
                         (self.pos[0] + 10, self.pos[1] + 45, self.dim[0] - 20, self.dim[1] - 200),
                         border_top_left_radius=5, border_top_right_radius=5,
                         border_bottom_left_radius=5, border_bottom_right_radius=5)

    def draw(self):
        if UI.settings_clicked:
            self.rects()
            self.screen.blit(self.text_surf, self.text_rect)
            self.screen.blit(self.close_img, self.close_img_rect)
            self.screen.blit(self.volume_up_img, self.volume_up_img_rect)
            volume_txt = self.font.render(str(UI.volume), True, (70, 70, 70))
            self.screen.blit(volume_txt, volume_txt.get_rect(center=(self.pos[0] + 195, self.pos[1] + 80)))
            self.screen.blit(self.volume_down_img, self.volume_down_img_rect)
            self.screen.blit(self.mute_img, self.mute_img_rect)
            self.theme_selector.draw()

        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.close_img_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                time.sleep(0.3)
                if self.dia_type == 'settings':
                    UI.settings_clicked = False
                    UI.first  = True

                    
        if self.volume_up_img_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.up_pressed = True
            else:
                if self.up_pressed:
                    if UI.volume < 100:
                        UI.volume += 1
                    self.up_pressed = False
        if self.volume_down_img_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.down_pressed = True
            else:
                if self.down_pressed:
                    if UI.volume > 0:
                        UI.volume -= 1
                    self.down_pressed = False
        if self.mute_img_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.mute_pressed = True
            else:
                if self.mute_pressed:
                    UI.volume = 0
                    self.mute_pressed = False
class Play:
    def __init__(self):
        self.chessBoard = None
        self.displayUI = None
        self.handgesT = None
        self.win = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        
    def hander(self):
        
      
            
            #print("Width =", GetSystemMetrics(0))
            #print("Height =", GetSystemMetrics(1))
            w = 640
            h = 480
            
            ######################
            wCam, hCam = w,h
            frameR = 100  # Frame Reduction
            smoothening = 7

            ######################
            pTime = 0
            plocX, plocY = 0, 0  # previous location
            clocX, clocY = 0, 0  # current location

            cap = cv2.VideoCapture(0)
            cap.set(3, wCam)
            cap.set(4, hCam)

            detector = htm.handDetector(maxHands=1)
            wScr, hScr = autopy.screen.size()
            
           
            while UI.handgesture:
                # 1. Find hand Landmarks
                success, img = cap.read()
                img = detector.findHands(img)
                lmList, bbox = detector.findPosition(img)
                
                # 2. Get the tip of the index and middle fingers
                if len(lmList)!=0:
                    x1, y1 = lmList[8][1:]
                    x2, y2 = lmList[12][1:]
                    # 3. Which fingers are up
                    fingers = detector.fingersUp()
                    # print(fingers)
                    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                                  (255, 0, 255), 2)
                    # 4. Only Index Finger : Moving Mode
                    if fingers[1] == 1 and fingers[2] == 0:

                        # 5. Convert Coordinates
                        x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
                    # print(x1, y1, x2, y2)

                        y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))


                        # 6. Smoothen Values
                        clocX = plocX + (x3 - plocX)/smoothening
                        clocY = plocY + (y3 - plocY)/smoothening
                        # 7. Move Mouse
                        autopy.mouse.move(wScr-clocX, clocY)
                        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                        plocX, plocY = clocX, clocY
                    # 8. Both Index and middle fingers are up : Clicking Mode
                    if fingers[1] == 1 and fingers[2] == 1:
                        # 9. Find distance between fingers
                        length, img, lineInfo = detector.findDistance(8, 12, img)
                        # 10. Click mouse if distance short
                        if length < 40:
                            cv2.circle(img, (lineInfo[4],lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                            autopy.mouse.click()



                # 11. Frame Rate
                cTime = time.time()
                fps = 1/(cTime - pTime)
                pTime = cTime
                #cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                #            (255, 0, 0), 3)
                # 12. Frame Rate
                cv2.imshow("Image", img)
                cv2.waitKey(1)
   

    def start(self  , first_name , second_name,game_type, theme , volume , continue_last_game):
        clock = pygame.time.Clock()
        self.continue_last_game = continue_last_game
        self.game_type = game_type
        self.assignChessBoard()
        self.settings_obj = DialogueBox(self.win, (0, HEIGHT-300), (400, 500), (70, 70, 70), (70, 70, 70), "Settings",
                                   dia_type='settings', volume=UI.volume)
        self.displayUI = UI(self.win, self.chessBoard , p1Name = first_name , p2Name = second_name)
        self.displayUI.listview.setOnItemSelected(self.OnItemClick)
        self.displayUI.drawDisplay()
        
        while self.displayUI.running:
            clock.tick(FPS)
            if (UI.handgesture == True):
                if self.handgesT is None:
                    #x = threading.Thread(target=thread_function, args=(1,))
                    self.handgesT = threading.Thread(target = self.hander )
                    self.handgesT.start()

            

            for event in pygame.event.get():
                self.displayUI.listview.eventHandler(event)

                if event.type == pygame.QUIT:
                    self.displayUI.running = False


                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.displayUI.dialog:
                        self.displayUI.dialogClick(pos)
                    else:
                        if pos[0] < TitleLenX:
                            self.displayUI.menuClick(pos)
                        else:
                            self.displayUI.click(pos)

            if UI.settings_clicked == True:
                self.settings_obj.draw()
                pygame.display.update()
            elif UI.first == True:
                UI.first = False
                self.displayUI.updateBoard()
                
                

        self.displayUI.quit()

    def assignChessBoard(self):
        if os.path.exists(brdFileName) and self.continue_last_game:
            with open(brdFileName, "rb") as savedBrd:
                self.chessBoard = pickle.load(savedBrd)
        else:
            self.chessBoard = Chess.chessBoard(Board_type = self.game_type)

    # noinspection PyUnusedLocal
    def OnItemClick(self, x, y, W, Ih, pos):
        if W / 6 < x < W / 6 + 70:
            pos = 2 * pos
            length = len(self.chessBoard.moveList)
            for hold in range(pos, length - 1):
                self.chessBoard.move_back()
            self.displayUI.updateBoard()

        elif W / 2 < x < W / 2 + 70:
            pos = 2 * pos + 1
            length = len(self.chessBoard.moveList)
            for hold in range(pos, length - 1):
                self.chessBoard.move_back()
            self.displayUI.updateBoard()


if __name__ == "__main__":
    playGame = Play()
    playGame.start()
