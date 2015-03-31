import pygame
from bullet import Bullet

pygame.mixer.init()

class Spaceship():

    def __init__(self,width,height,x,y,color):
        self.image = pygame.image.load("X-Wing.png") 
        self.width  = 26
        self.height = 50
        self.x      = x
        self.y      = y
        self.color  = color
        self.alive  = True
        self.hit    = False
        return

    def checkHitBaddie(self,x,y,w,h):
        if self.hitRectangle(x, y, w, h):
            self.setAlive(False)
            self.hit = True
        if self.hit == True:
            hitsound = pygame.mixer.Sound("R2HIT.wav")
            hitsound.play()

    def setAlive(self,alive):
        self.alive = alive
        return
    
    def hitRectangle(self, x, y, w, h):
        if( ((self.x + self.width) >= x) and
            (self.x <= x + w) ):
            if( ((self.y + self.height) >= y) and
                (self.y <= y + h)) :
                return True
        return False

    def getHit(self):
        return self.hit


    def moveLeft(self, dx):
        self.x -= dx
        # check the wall
        if self.x < 0:
            self.x = 0
        return

    def moveRight(self, dx, upper_limit):
        self.x += dx
        return

    def moveUp(self, dy):
        self.y -= dy
        # check the wall
        if self.y < 0:
            self.y = 0
        return

    def moveDown(self, dy, board_height):
        self.y += dy
        # check the wall
        if self.y > board_height - self.height:
            self.y = board_height - self.height
        return

    def fire(self,width,height,color):
        firesound = pygame.mixer.Sound("REB-LS-2.wav")
        firesound.play()
        return Bullet(width,height,(self.x + self.width + 33) , self.y - 30, color)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        #rect = pygame.Rect( self.x, self.y, self.width, self.height )
        #pygame.draw.rect(surface, self.color, rect)
        return
        
