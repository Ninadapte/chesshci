# This is an implementation of a listView using the pygame library
# 11:38
import pygame
from pygame.locals import *
from Game.values.dimens import *


class ListView:
    def __init__(self, x, y, width, height, fruits, backgroundColor=(255, 255, 255), ItemBackGround=(255, 255, 255),
                 ItemBorderRadius=0, ItemBorderColor=(0, 0, 0), itemborderThickness=1, win=None):

        self.x = x  # x cordinate of the top left the the container
        self.y = y  # y cordinate of the top left of the container
        self.W = width  # width of the container
        self.H = height  # height of the container
        self.cotainerRadius = 30  # initial container radius (implementation of the corner radius in padding has not been done)
        self.fruits = fruits
        self.Ih = fruits.Ih  # initially list item height is 100
        self.P = self.Ih  # initial padding
        self.rightP = 5
        self.N = 0  # number of items initially   {{ modify later }}
        self.itemTopmargin = fruits.itemTopmargin  # top margin for all the items
        self.containerColor = (0, 0, 0)  # outline color of the container Black by default
        self.scrollbarColor = (0, 0, 0)
        self.window = win  # windown on which to draw
        self.background = backgroundColor  # background color of the container
        self.scrollbarw = 10  # width of the scrollbar
        self.scrollbary = self.y + self.P
        self.itemborderColor = self.fruits.ItemBorderColor

        self.itemRadius = self.fruits.itemRadius
        self.listItemY = [
            self.y + self.P + self.itemTopmargin]  # this holds all the top y coordinate of all the list items {{ modify later }}
        self.containerFill = 4  # fill value of the outline color of the container
        # initialize the fruits variable
        self.itemBorderThickness = itemborderThickness
        self.scrollbarh = self.H - 2 * self.P
        self.topItem = 0  # This is the top item
        self.bottomItem = 0  # This is the bottom item
        self.onItemSelected = None
        self.scrollBarRadius = 5
        self.itembackground = ItemBackGround
        # call all the initializer functions
        self.initializeListOutline()
        self.createOutline()

        self.draw()

    # Get the scrollbar height updated
    def getscrollbarh(self):
        alpha = 20
        if self.fruits.length() * (self.Ih + self.itemTopmargin) > self.H - 2 * self.P:
            self.scrollbarh = min((self.H - 2 * self.P) * 5 / (self.N + 1) + alpha, self.H - 2 * self.P)
        # self.scrollbarh = 200
        # self.scrollbarh = 30

    def setOnItemSelected(self, func):
        # onItemSelected(pos , x , y)
        self.onItemSelected = func

    # initialize all the display parameters of the list including the scrollbar parameters
    def initializeListOutline(self):
        self.listx = self.x + self.rightP
        self.listy = self.y + self.P
        self.listh = self.H - 2 * self.P  # initial height of the scroll bar   {{ modify later }}
        self.listw = self.W - 2 * self.rightP  # initialize the list width
        self.fruits.attachCallback(self.callback)  # initialize the fruit variable
        self.getscrollbarh()
        self.scrollbarx = self.x + self.W - self.rightP - self.scrollbarw

    def drawListArea(self):
        pygame.draw.rect(self.window, self.itembackground,
                         (self.x + self.rightP, self.y + self.P, self.W - 2 * self.rightP, self.H - 2 * self.P))

    # Used to draw the border of the item
    def drawItemBorder(self, x, y):
        pygame.draw.rect(self.window, self.itemborderColor, (x, y, self.W - 2 * self.rightP, self.Ih),
                         self.itemBorderThickness, self.itemRadius)

    def drawScrollbar(self):
        pygame.draw.rect(self.window, self.scrollbarColor,
                         (self.scrollbarx, self.scrollbary, self.scrollbarw, self.scrollbarh))

    # draw the container
    def drawContainer(self):
        pygame.draw.rect(self.window, self.background, self.containerRect, self.containerFill, self.cotainerRadius)

    # create a frame for the container and the list
    def createOutline(self):
        self.containerRect = pygame.Rect(self.x, self.y, self.W, self.H)
        self.listRect = pygame.Rect(self.listx, self.listy, self.listw, self.listh)
        self.drawContainer()
        self.drawScrollbar()
        # pygame.display.flip()

    def drawMarginalRecs(self):
        pygame.draw.rect(self.window, self.itembackground,
                         (self.x + self.rightP, self.y, self.W - 2 * self.rightP, self.P),
                         border_top_left_radius=self.cotainerRadius, border_top_right_radius=self.cotainerRadius)
        pygame.draw.rect(self.window, self.itembackground,
                         (self.x + self.rightP, self.y + self.H - self.P, self.W - 2 * self.rightP, self.P),
                         border_bottom_left_radius=self.cotainerRadius, border_bottom_right_radius=self.cotainerRadius)

    # updates and draws the whole of list
    def draw(self):

        self.drawListArea()
        self.getscrollbarh()
        BoxEndY = self.y + self.P + self.H
        BoxStartY = self.y + self.P
        bar_height = self.scrollbarh

        scroll_height = self.H - 2 * self.P - self.scrollbarh
        height_of_item = (self.Ih + self.itemTopmargin)
        if (self.fruits.length() * height_of_item < self.H - 2 * self.P) and self.scrollbary > self.y + self.P:
            self.scrollbary = self.y + self.P

        scroll_rel = (self.scrollbary - BoxStartY) / (scroll_height + 0.000001)

        box_height = self.H - 2 * self.P

        list_height = self.fruits.length() * height_of_item
        offset = (list_height - box_height) * scroll_rel
        initial_start_pos_list = self.y + self.P

        self.listItemY = []
        for x in range(self.fruits.length()):
            self.listItemY.append((x * height_of_item) + initial_start_pos_list - offset)

        isbottomSelected = False

        for item in range(self.fruits.length()):
            if self.listItemY[item] >= self.y + 0.5 * self.P and self.listItemY[
                item] + self.Ih + self.itemTopmargin <= self.y + self.H - 0.5 * self.P:
                # self.drawItemBorder(self.x+self.rightP,self.listItemY[item])
                # self.drawItemContents(self.x+self.rightP+30,self.listItemY[item]+30,item)
                self.fruits.draw(self.x + self.rightP, self.listItemY[item], item, self.rightP, self.window)

            if self.listItemY[item] <= self.y + self.P:
                self.topItem = item

            if self.listItemY[item] + self.Ih >= self.y + self.H - self.P and not isbottomSelected:
                self.bottomItem = item

                isbottomSelected = True

        self.drawScrollbar()
        self.scrollbarColor = (0, 0, 0)
        self.drawMarginalRecs()
        pygame.display.flip()

    def setItemMargin(self, margin):
        self.itemTopmargin = margin

    # callback for items of list
    def callback(self):
        self.N = self.fruits.length()
        self.getscrollbarh()
        self.draw()  # rel for addition of items is always positive

    def ItemclickHandler(self, x, y):

        self.bottomItem = self.fruits.length() - 1
        if self.fruits.length() == 0:
            return
        if x > self.x + self.rightP and x < self.x + self.W - self.rightP - self.scrollbarw:
            if y > self.y + self.P and y < self.y + self.H - self.P:

                firItemtop = max(self.y + self.P, self.listItemY[self.topItem])
                botItemBot = min(self.y + self.H - self.P,
                                 self.listItemY[self.bottomItem] + self.Ih + self.itemTopmargin)

                # check for first item click
                if y > firItemtop and y < self.listItemY[self.topItem] + self.Ih:
                    self.onItemSelected(x - FENStartX, y - FENStartY, self.W, self.Ih, self.topItem)


                # check for last item click
                elif y > self.listItemY[self.bottomItem] and y < botItemBot:
                    self.onItemSelected(x - FENStartX, y - FENStartY, self.W, self.Ih, self.bottomItem)



                else:
                    for w in range(self.topItem + 1, self.bottomItem):
                        top = self.listItemY[w]
                        bottom = self.listItemY[w] + self.Ih
                        if y > top and y < bottom:
                            self.onItemSelected(x - FENStartX, y - FENStartY, self.W, self.Ih, w)

                            break

    def eventHandler(self, event):
        # print(event)
        if event.type == pygame.MOUSEMOTION and event.buttons == (1, 0, 0) and (
                event.pos[0] > self.scrollbarx and event.pos[0] < self.scrollbarx + self.scrollbarw):
            if event.rel[1] > 0:
                # print("You're moving the mouse to the down")

                if self.scrollbary + self.scrollbarh < self.y + self.H - self.P:
                    self.scrollbary = max(self.y + self.P,
                                          min(self.y + self.H - self.P - self.scrollbarh, event.pos[1]))
                    self.scrollbarColor = (255, 0, 0)
                    self.draw()

            else:
                # print("You are moving the mouse to the top")

                if self.scrollbary > self.y + self.P:
                    self.scrollbary = max(self.y + self.P,
                                          min(self.y + self.H - self.P - self.scrollbarh, event.pos[1]))
                    self.scrollbarColor = (255, 0, 0)
                    self.draw()




        elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1):

            self.ItemclickHandler(event.pos[0], event.pos[1])

        elif event.type == MOUSEWHEEL and pygame.mouse.get_pressed()[0] != 1 and (
                pygame.mouse.get_pos()[0] > self.x + self.rightP and pygame.mouse.get_pos()[
            0] < self.x + self.W - self.rightP):

            speed = self.Ih / 2
            if event.y == 1:
                self.scrollbary = max(self.y + self.P,
                                      min(self.y + self.H - self.P - self.scrollbarh, self.scrollbary - speed))
                self.draw()

            elif event.y == -1:
                self.scrollbary = max(self.y + self.P,
                                      min(self.y + self.H - self.P - self.scrollbarh, self.scrollbary + speed))
                self.draw()


