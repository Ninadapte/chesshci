import pygame
import os
import time
from resources import strings
from play import Play

class info_dialogue:
    def __init__(self, screen, pos, dimensions, color, color_title, title, dia_type):
        self.screen = screen
        self.pos = pos
        self.dim = dimensions
        self.color = color
        self.color_title = color_title
        self.close_img = pygame.image.load("images/a.png")
        self.close_img_rect = self.close_img.get_rect(center=(self.pos[0] + self.dim[0] + 15, self.pos[1] + 55))
        self.close_img = pygame.transform.scale(self.close_img, (40, 40))
        self.title = title
        self.font = pygame.font.Font(Menu.product_sans_path, 25)
        self.text_surf = self.font.render(self.title, True, (253, 246, 227))
        self.text_rect = self.text_surf.get_rect(center=(self.pos[0] + 750, self.pos[1] + 20))
        self.dia_type = dia_type
        self.mute_img = pygame.image.load("images/mute.png")
        self.mute_img = pygame.transform.scale(self.mute_img, (50, 50))
        self.mute_img_rect = self.mute_img.get_rect(center=(self.pos[0] + self.dim[0] + -130, self.pos[1] + 140))

        self.volume_down_img = pygame.image.load("images/volume-down.png")
        self.volume_down_img = pygame.transform.scale(self.volume_down_img, (50, 50))
        self.volume_down_img_rect = self.volume_down_img.get_rect(
            center=(self.pos[0] + self.dim[0] - 130, self.pos[1] + 80))

        self.volume_up_img = pygame.image.load("images/volume-up.png")
        self.volume_up_img = pygame.transform.scale(self.volume_up_img, (50, 50))
        self.volume_up_img_rect = self.volume_up_img.get_rect(center=(self.pos[0] + 130, self.pos[1] + 80))

    def rects(self):
        pygame.draw.rect(self.screen, self.color, (self.pos[0], self.pos[1], self.dim[0], self.dim[1] - 25),
                         border_top_left_radius=5, border_top_right_radius=5,
                         border_bottom_left_radius=5, border_bottom_right_radius=5)

        pygame.draw.rect(self.screen, '#B3E5FC',
                         (self.pos[0] + 10, self.pos[1] + 45, self.dim[0] - 20, self.dim[1] - 80),
                         border_top_left_radius=5, border_top_right_radius=5,
                         border_bottom_left_radius=5, border_bottom_right_radius=5)
        # (253, 246, 227)

    def draw(self):
        if Menu.info_clicked:
            self.rects()
            self.screen.blit(self.text_surf, self.text_rect)
            self.screen.blit(self.close_img, self.close_img_rect)
            self.display_info()
        self.check_click()

    def display_info(self):
        string = '''                Chess is a board game played between two players that simulates a war between two kingdoms. Chess is a turn-based strategy game with no hidden information.There are six types of chess pieces. They are the pawn, the knight, the bishop,the rook, the queen, and the king. Each of those pieces moves differently and has a distinct value.Pawns move up the board one square unless it's the first time they're moving when they may move two squares. Note that they cannot move backward.The pawn captures pieces one square diagonally and is the only chess piece that captures differently than the way it moves. It is also the only piece that can capture using the special en passant rule.The knight moves two squares horizontally and one vertically, or two squares vertically and one horizontally. The way the knight moves resembles the upper-case "L." The bishop can move any number of squares diagonally.The rook can move any number of squares vertically or horizontally.The queen is the most powerful piece on the board.It can move diagonally, horizontally, or vertically as many squares as it wants (unless another piece blocks it).The king can move one square in every direction.Also, the king can make use of the special castling rule together with a rook.
                
                You can enter name of both the players and choose which chess(standard, chess 960, no casle) you want to play in the main menu. You can start to play new game or continue your previous game and these options are also provided in main menu. Theme selection and sound settings are provided in settings menu. There are three ways in which you can play the game.
                1. By using mouse
                2. By using hand gestures
                3. By using voice commands, and you can always switch between these options which will be provided in the game window.
                
'''
        x, y = self.pos[0] + 15, self.pos[1] + 50
        words = [word.split(' ') for word in string.splitlines()]
        space = self.font.size(' ')[0]  # width of space
        max_width, max_height = self.dim
        for line in words:
            for word in line:
                word_surface = self.font.render(word, True, (70, 70, 70))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = self.pos[0] + 15  # reset x
                    y += word_height  # start on new row.
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = self.pos[0] + 15  # reset x
            y += word_height  # start on new row.

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.close_img_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                time.sleep(0.3)
                if self.dia_type == 'info':
                    Menu.info_clicked = False


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
        self.font = pygame.font.Font(Menu.product_sans_path, 25)
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
        if Menu.settings_clicked:
            self.rects()
            self.screen.blit(self.text_surf, self.text_rect)
            self.screen.blit(self.close_img, self.close_img_rect)
            self.screen.blit(self.volume_up_img, self.volume_up_img_rect)
            volume_txt = self.font.render(str(Menu.volume), True, (70, 70, 70))
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
                    Menu.settings_clicked = False
        if self.volume_up_img_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.up_pressed = True
            else:
                if self.up_pressed:
                    if Menu.volume < 100:
                        Menu.volume += 1
                    self.up_pressed = False
        if self.volume_down_img_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.down_pressed = True
            else:
                if self.down_pressed:
                    if Menu.volume > 0:
                        Menu.volume -= 1
                    self.down_pressed = False
        if self.mute_img_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.mute_pressed = True
            else:
                if self.mute_pressed:
                    Menu.volume = 0
                    self.mute_pressed = False


class Edittext:
    def __init__(self, window, x, y, default, H=50, W=50, margin_left=0, margin_right=0, margin_top=0, margin_bottom=0,
                 text_size=38, text_color=(70, 70, 70), padding=10, topLeftradius=5, bottomLeftradius=5,
                 topRightradius=5, bottomRightradius=5, borderColor=(70, 70, 70), borderFill=1,
                 font="resources/Product Sans Regular.ttf",
                 focusColor=(150, 200, 100), background_color=(253, 246, 227), title="DUMMY", title_pos=(500, 500)):
        self.x = x
        self.y = y
        self.H = H
        self.W = W
        self.ML = margin_left
        self.MR = margin_right
        self.MT = margin_top
        self.MB = margin_bottom
        self.TLR = topLeftradius
        self.TRR = topRightradius
        self.BLR = bottomLeftradius
        self.BRR = bottomRightradius
        self.title = title
        self.title_pos = title_pos
        self.text_size = text_size
        self.text_color = text_color
        self.P = padding
        self.borderColor = borderColor
        self.bgcolor = background_color
        self.borderfill = borderFill
        self.text = default
        self.default = default
        self.window = window
        self.font = font
        self.font = pygame.font.Font(self.font, self.text_size)
        self.focusedColor = focusColor
        self.text_box = self.font.render("H", True, self.text_color)
        self.letterSize = self.text_box.get_rect().width
        self.left = 0

        self.isGreater = False
        self.focus = False

    def draw(self):
        bCol = None
        if not self.focus:
            bCol = self.borderColor
        else:
            bCol = self.focusedColor

        text_surf = self.font.render(self.title, True, (253, 246, 227))
        self.window.blit(text_surf, (self.title_pos[0], self.title_pos[1]))
        ### Draw the outer rect here
        pygame.draw.rect(self.window, bCol, (self.x, self.y, self.W, self.H), self.borderfill,
                         border_top_left_radius=self.TLR, border_top_right_radius=self.TRR,
                         border_bottom_left_radius=self.BLR, border_bottom_right_radius=self.BRR)

        ###Draw the inner background
        pygame.draw.rect(self.window, self.bgcolor, (
            self.x + self.borderfill, self.y + self.borderfill, self.W - 2 * self.borderfill,
            self.H - 2 * self.borderfill),
                         0, border_top_left_radius=self.TLR - 3, border_top_right_radius=self.TRR - 3,
                         border_bottom_left_radius=self.BLR - 3, border_bottom_right_radius=self.BRR - 3)

        ###format the contents here

        if (len(self.text)) * self.letterSize > self.W and not self.isGreater:
            self.left += 1
            self.isGreater = True

        if len(self.text) * self.letterSize < self.W:
            self.left = 0
            self.isGreater = False

        ###Draw the contents here
        text = self.font.render(self.text[self.left:self.left + self.W // self.letterSize], True, self.text_color)
        textRect = text.get_rect()
        textRect.center = (self.x + self.W / 2, self.y + self.H / 2)
        self.window.blit(text, textRect)

        # pygame.display.update()

    def eventHandler(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1):
            if event.pos[0] > self.x and event.pos[0] < self.x + self.W:
                if event.pos[1] > self.y and event.pos[1] < self.y + self.H:
                    self.focus = True
                else:
                    self.focus = False
            else:
                self.focus = False

        if event.type == pygame.KEYDOWN:
            # print(event.key)
            if event.key >= 97 and event.key <= 122 and self.focus:
                self.text += chr(event.key)

                self.left += 1

            # Handle backspace here
            elif event.key == 8 and self.focus:
                # self.text = self.text[:-1]
                if len(self.text) != 0:
                    self.text = self.text[:-1]
                if self.left != 0:
                    self.left -= 1


            # handle the enter event
            elif event.key == 13 and self.focus:
                pass


            # handle the left key event
            elif event.key == 1073741904 and self.focus:

                if self.left != 0:
                    self.left -= 1



            # handle the right key event
            elif event.key == 1073741903 and self.focus:

                if self.left + self.W // self.letterSize != len(self.text):
                    self.left += 1
            # handle the space event here
            elif event.key == 32 and self.focus:
                self.text += " "

        # self.draw()

    def setText(self, text):
        self.text = text

    def getText(self):
        return self.text

class Menu:
    path = 'D://Python-Projects//pygame_menus//'
    product_sans_path = "resources/Product Sans Regular.ttf"
    continue_last_game = False
    settings_clicked = False
    info_clicked = False
    volume = 50
    theme_selected = 'Classic'

    # Variables to be called by main game window------------------------------------------------------------------------
    var_chess_type = "Standard Chess"  # possible options - "Standard Chess", "Chess 960", "No Castle"
    var_first_players_name = "Ronald"
    var_second_players_name = "Harry"
    var_theme_selected = theme_selected  # possible options - "Classic", "Blue", "Red"
    var_volume = volume
    var_is_continue_last_game = continue_last_game

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):

        pygame.init()
        info = pygame.display.Info()
        # open up a window
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # resolution of the screen
        self.res = self.screen.get_size()

        # white color
        self.color = (255, 255, 255)

        # light shade of the button
        self.color_light = (170, 170, 170)

        # dark shade of the button
        self.color_dark = (100, 100, 100)

        # stores the width of the
        # screen into a variable
        self.width = self.screen.get_width()

        # stores the height of the
        # screen into a variable
        self.height = self.screen.get_height()

        # project folder path
        self.path = "D://Python-Projects//pygame_menus//"
        # product-sans font path
        self.product_sans_path = "resources\Product Sans Regular.ttf"

        # defining a font
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        
        self.font = pygame.font.Font("resources/Product Sans Regular.ttf", 40)
        self.caption_font = pygame.font.Font("resources/Product Sans Regular.ttf", 30)

        # rendering a text written in
        # this font
        self.text = self.smallfont.render('Quit', True, self.color)
        self.title_bar_name = self.font.render("Main Menu", True, self.color)

        # quit image
        self.quit_image = pygame.image.load("images/a.png")
        self.quit_image = pygame.transform.scale(self.quit_image, (40, 40))

        # minimize image
        self.min_image = pygame.image.load("images/b.png")
        self.min_image = pygame.transform.scale(self.min_image, (32, 32))

        # title image
        self.title = pygame.image.load("images/bi2.png")
        self.title = pygame.transform.scale(self.title, (500, 175))

        # chess type images
        self.std_chess_img = pygame.image.load("images/standard_chess.png")
        self.std_chess_img = pygame.transform.scale(self.std_chess_img, (80, 70))
        self.chess_960_img = pygame.image.load("images/chess_960.jpg")
        self.chess_960_img = pygame.transform.scale(self.chess_960_img, (80, 70))

        self.play_against = "computer"
        self.event = None

        # play against images
        self.play_against_human_img = pygame.image.load("images/human.png")
        self.play_against_human_img = pygame.transform.scale(self.play_against_human_img, (75, 75))
        self.play_against_computer_img = pygame.image.load("images/ai.png")
        self.play_against_computer_img = pygame.transform.scale(self.play_against_computer_img, (75, 75))

        self.clock = pygame.time.Clock()
        self.fps = 60

    def get_mouse_pos(self):
        mouse = pygame.mouse.get_pos()
        return mouse

    # to quit menu screen
    def quit_menu(self):
        mouse = self.get_mouse_pos()
        if self.width - 40 <= mouse[0] <= self.width and -5 <= mouse[1] <= 40:
            self.screen.blit(self.quit_image, (self.width - 39, -3))
            self.title_bar_btn_animation()
            pygame.quit()

    # to minimize menu screen
    def min_menu(self):
        mouse = self.get_mouse_pos()
        if self.width - 65 <= mouse[0] <= self.width - 39 and 0 <= mouse[1] <= 32:
            self.screen.blit(self.min_image, (self.width - 64, 2))
            self.title_bar_btn_animation()
            pygame.display.iconify()

    def load_background(self):
        image = pygame.image.load("images/image.png")
        image = pygame.transform.scale(image, self.res)
        return image

    def draw_title_bar(self):
        pygame.draw.rect(self.screen, (70, 70, 70), (0, 0, self.width, 30))
        pygame.draw.rect(self.screen, (70, 70, 70), (0, 0, 200, 55))
        pygame.draw.polygon(surface=self.screen, color=(70, 70, 70), points=[(200, 0), (200, 54), (250, 0)])
        self.screen.blit(self.title_bar_name, (10, 2))
        self.screen.blit(self.quit_image, (self.width - 40, -5))
        self.screen.blit(self.min_image, (self.width - 65, 0))

    def draw_bg(self):
        image = self.load_background()
        self.screen.blit(image, (0, 0))
        self.draw_title_bar()
        # self.screen.blit(self.title, (self.width / 2 - 225, 20))
        img_rect = self.title.get_rect(center=(self.width / 2, 100))
        self.screen.blit(self.title, img_rect)

    def title_bar_btn_animation(self):
        pygame.display.update()
        time.sleep(0.2)
        self.draw_title_bar()
        pygame.display.update()
        time.sleep(0.3)

    def main(self):
        # player1_name = Input(self.screen, self.width*4/10 - self.width*1/150, self.width*2.7/20)
        # player2_name = Input(self.screen, 600, 225)
        button1 = Button(self.screen, 'Play the game', 220, 60, (self.width / 2 - 95, self.height - 150), 4,
                         "play-new-game")
        button2 = Button(self.screen, 'Continue last game', 220, 60, (self.width / 2 + 200, self.height - 150), 4,
                         'continue-last-game')
        button3 = Button(self.screen, 'Settings', 220, 60, (self.width / 2 - 397, self.height - 150), 4, 'settings')
        chess_type_selector = Selector(self.screen, (550, 300), (970, 325), (600, 328), "Chess Type",
                                       ['Standard Chess', 'Chess 960', 'No '
                                                                       'Castle'])
        difficulty_selector = Selector(self.screen, (550, 475), (860, 500), (420, 500), "Difficulty",
                                       ['Easy', 'Medium', 'Hard '])

        first_player_name = Edittext(self.screen, 900, 389, 'Ronald', 50, 250, borderFill=3,
                                     title="First Player's Name",
                                     title_pos=(550, 390))
        second_player_name = Edittext(self.screen, 950, 475, 'Harry', 50, 250, borderFill=3,
                                      title="Second Player's Name",
                                      title_pos=(550, 475))

        settings_win = DialogueBox(self.screen, (28, 200), (400, 500), (70, 70, 70), (70, 70, 70), "Settings",
                                   dia_type='settings', volume=Menu.volume)
        btn_info = Button(self.screen, 'info', 110, 50, (self.width - 150, 75), 4,
                          'info')
        # info_win = info_dialogue(self.screen, (self.width-330, 150), (320, 650), (70, 70, 70), (70, 70, 70), "Information", dia_type='info')
        info_win = info_dialogue(self.screen, (self.width - 1510, 190), (1475, 680), (70, 70, 70), (70, 70, 70),
                                 "Information", dia_type='info')
        ai_color_selector = Selector(self.screen, (550, 565), (830, 592), (390, 593), "AI color",
                                     ['White', 'Black'])
        while True:
            for ev in pygame.event.get():
                self.event = ev
                if ev.type == pygame.QUIT:
                    pygame.quit()

                # checks if a mouse is clicked
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    # if the mouse is clicked on the quit button the game is terminated
                    self.quit_menu()
                    self.min_menu()
                    x, y = self.get_mouse_pos()


                first_player_name.eventHandler(ev)

                second_player_name.eventHandler(ev)

            # ui language ----------------------------------------------------------------------------------------------
            self.draw_bg()
            first_player_name.draw()
            second_player_name.draw()
            if Menu.settings_clicked:
                settings_win.draw()
            # if Menu.info_clicked:
            #     info_win.draw()

            # ----------------------------------------------------------------------------------------------------------

            button1.draw()
            button2.draw()
            btn_info.draw()
            # print(button2.isContinue)
            button3.draw()
            chess_type_selector.draw()



            if Menu.info_clicked:
                info_win.draw()
            Menu.var_chess_type = chess_type_selector.option_selected
            Menu.var_ai_color = ai_color_selector.option_selected
            Menu.var_ai_difficulty = difficulty_selector.option_selected
            if first_player_name.getText() == " ":
                Menu.var_first_players_name = "Ronald"
            else:
                Menu.var_first_players_name = first_player_name.getText()

            if second_player_name.getText() == " ":
                Menu.var_second_players_name = "Harry"
            else:
                Menu.var_second_players_name = second_player_name.getText()

            # updates the frames of the game
            pygame.display.update()

class Button:
    def __init__(self, screen, text, width, height, pos, elevation, type):
        self.gui_font = pygame.font.Font(None, 30)
        self.screen = screen
        self.type = type
        self.isContinue = False
        # core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]
        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#01579B'  # '#475f77'

        # botton rectangle
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = '#BFC0C2'  # '#354B5E'

        # text
        self.text_surf = self.gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        self.screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#36AF57'  # '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True

            else:
                if self.pressed:
                    if self.type == "play-new-game" and not Menu.info_clicked:
                        player = Play()
                         
    
     
                        player.start(Menu.var_first_players_name , Menu.var_second_players_name  ,Menu.var_chess_type,Menu.var_theme_selected,Menu.var_volume,Menu.var_is_continue_last_game)
                        

                    if self.type == "continue-last-game" and not Menu.info_clicked:
                        self.isContinue = True
                        player = Play()
                        player.start(Menu.var_first_players_name , Menu.var_second_players_name  ,Menu.var_chess_type,Menu.var_theme_selected,Menu.var_volume,True)
                    self.dynamic_elevation = self.elevation
                    self.pressed = False
                    if self.type == "settings" and not Menu.info_clicked:
                        if Menu.settings_clicked:
                            Menu.settings_clicked = False
                        else:
                            Menu.settings_clicked = True
                    if self.type == "info":
                        if Menu.info_clicked:
                            Menu.info_clicked = False
                        else:
                            Menu.info_clicked = True
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#D74B4B'  # '#36AF57'


class ImageOption:
    # cc is caption
    def __init__(self, screen, img1, img2, x, y, length, width, cc1, cc2, decision_title, text_rect, image_rect1,
                 image_rect2):
        self.img1 = img1
        self.img2 = img2
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.cc1 = cc1
        self.cc2 = cc2
        self.decision_title = decision_title
        self.screen = screen
        self.text_rect = text_rect
        self.image_rect1 = image_rect1
        self.image_rect2 = image_rect2

    def draw(self):
        self.screen.blit(self.img1, self.image_rect1)
        self.screen.blit(self.decision_title, self.text_rect)
        self.screen.blit(self.img2, self.image_rect2)


class settings_Selector:

    # options is list of options
    def __init__(self, screen, title_pos, options_center, next_btn_pos, selector_title, options):
        self.options = options
        self.i = 0  # option no. zero is selected by default
        self.n = len(options)
        self.path = Menu().path
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
                    Menu.theme_selected = self.option_selected
        if self.next_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.right_pressed = True
            else:
                if self.right_pressed:
                    self.i = (self.i + 1) % (len(self.options))
                    self.option_selected = self.options[self.i]
                    self.right_pressed = False
                    Menu.theme_selected = self.option_selected


class Selector:

    # options is list of options
    def __init__(self, screen, title_pos, options_center, next_btn_pos, selector_title, options):
        self.options = options
        self.i = 0  # option no. zero is selected by default
        self.n = len(options)
        self.path = Menu().path
        self.font = pygame.font.Font("resources/Product Sans Regular.ttf", 40)
        self.screen = screen
        self.options_pos = options_center
        self.option_selected = options[0]
        self.left_pressed = False
        self.right_pressed = False
        self.selector_title = selector_title
        self.next_btn_pos = next_btn_pos
        self.title_pos = title_pos
        self.text_surf = self.font.render(self.selector_title, True, (253, 246, 227))
        self.prev_img = pygame.image.load("images/left-arrow.png")
        self.next_img = pygame.image.load("images/right-arrow.png")
        self.prev_img = pygame.transform.scale(self.prev_img, (50, 50))
        self.next_img = pygame.transform.scale(self.next_img, (50, 50))
        self.title_width = self.text_surf.get_rect().width
        self.prev_rect = self.prev_img.get_rect(
            center=(self.title_pos[0] + self.title_width + 40, self.title_pos[1] + 27))
        self.next_rect = self.next_img.get_rect(center=(self.title_pos[0] + next_btn_pos[0], next_btn_pos[1]))
        # selector title

        # self.text_rect = self.text_surf.get_rect(center=center)

    def draw(self):
        a = self.screen.blit(self.text_surf, (self.title_pos[0], self.title_pos[1]))
        self.screen.blit(self.prev_img, self.prev_rect)
        option = self.font.render(self.options[self.i], True, (253, 246, 227))
        # self.screen.blit(option, option.get_rect(center=(970, 325)))
        self.screen.blit(option, option.get_rect(center=(self.options_pos[0], self.options_pos[1])))
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
        if self.next_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.right_pressed = True
            else:
                if self.right_pressed:
                    self.i = (self.i + 1) % (len(self.options))
                    self.option_selected = self.options[self.i]
                    self.right_pressed = False




if __name__ == "__main__":
    menu = Menu()
    menu.main()
