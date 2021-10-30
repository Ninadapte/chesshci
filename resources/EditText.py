import pygame

             #(x,y)               #W
##              --------------------------------------
##             |                                      |
##             |     Text Comes Here                  |
##             |                                      |     #H
##             |                                      |
##              --------------------------------------


class Edittext:
    def __init__(self , window,x,y,H=50,W=50,margin_left=0,margin_right=0 , margin_top=0,margin_bottom=0,text_size=30,text_color=(0,0,0),padding=10,topLeftradius = 10,bottomLeftradius = 10 ,topRightradius=10,bottomRightradius =10 ,borderColor = (0,0,0) , borderFill = 1,font = 'freesansbold.ttf',focusColor=(0,0,255),background_color = (255,255,255)):
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
        self.text_size = text_size
        self.text_color = text_color
        self.P = padding
        self.borderColor = borderColor
        self.bgcolor = background_color
        self.borderfill = borderFill
        self.text = ""
        self.window = window
        self.font = font
        self.font = pygame.font.Font(self.font, self.text_size)
        self.focusedColor = focusColor
        text = self.font.render("H", True, self.text_color)
        self.letterSize = text.get_rect().width
        self.left = 0
        
        self.isGreater = False
        self.focus = False
    def draw(self):
        
        bCol= None
        if not self.focus:
             bCol = self.borderColor
        else:
            bCol = self.focusedColor


        ###Draw the outer rect here
        pygame.draw.rect(self.window ,bCol,(self.x,self.y,self.W,self.H),self.borderfill,border_top_left_radius = self.TLR,border_top_right_radius = self.TRR,
                             border_bottom_left_radius = self.BLR,border_bottom_right_radius = self.BRR)


        ###Draw the inner background 
        pygame.draw.rect(self.window ,self.bgcolor,(self.x+self.borderfill,self.y+self.borderfill,self.W-2*self.borderfill,self.H-2*self.borderfill),0,border_top_left_radius = self.TLR,border_top_right_radius = self.TRR,
                             border_bottom_left_radius = self.BLR,border_bottom_right_radius = self.BRR)




        ###format the contents here
        

        if (len(self.text))*self.letterSize > self.W and not self.isGreater:
           
            self.left +=1
            self.isGreater = True
        
        if len(self.text)*self.letterSize < self.W:
            self.left = 0
            self.isGreater = False


        ###Draw the contents here
        text = self.font.render(self.text[self.left:self.left + self.W//self.letterSize], True, self.text_color)
        textRect = text.get_rect()
        textRect.center = (self.x + self.W/2 , self.y + self.H/2 )
        self.window.blit(text, textRect)

        pygame.display.flip()

    def eventHandler(self,event):

        if event.type == pygame.MOUSEBUTTONDOWN and (event.button==1):
            
            if event.pos[0]>self.x and event.pos[0]<self.x+self.W:
                if event.pos[1]>self.y and event.pos[1]<self.y+self.H:
                    self.focus = True
                else:
                    self.focus = False
            else:
                self.focus = False
        
        if event.type ==  pygame.KEYDOWN:
            #print(event.key)
            if event.key>= 97 and event.key<=122 and self.focus:
                self.text+= chr(event.key)
                
                self.left+=1

            #Handle backspace here
            elif event.key == 8:
                #self.text = self.text[:-1]
                self.text = self.text[:-1]
                if self.left!=0:
                    self.left-=1
                

            #handle the enter event
            elif event.key == 13:
                pass


            #handle the left key event
            elif event.key == 1073741904:

                
                    if self.left!=0:
                        self.left-=1



            #handle the right key event
            elif event.key == 1073741903:
                
                if self.left + self.W//self.letterSize != len(self.text):
                    self.left+=1
            #handle the space event here
            elif event.key == 32:
                self.text+=" "
            
        self.draw()
    
    def setText(self,text):
        self.text=  text

    def getText(self):

        
        return self.text