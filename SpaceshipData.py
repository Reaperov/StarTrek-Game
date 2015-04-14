import pygame
import random
from spaceship import Spaceship
from baddie import Baddie
from stardestroyer import Destroyer
spaceship = Spaceship
gameover = False

class SpaceshipData:

    def __init__(self,width,height,frame_rate):
        self.font = pygame.font.SysFont("Times New Roman",36)
        self.font2 = pygame.font.SysFont("Courier New",20)
        self.frame_rate = frame_rate
        self.text_color = (255,0,0)
        self.width  = width
        self.height = height
        self.upper_limit = self.width/3
        self.spaceship_width = 20
        self.spaceship_height = 10
        self.spaceship = Spaceship(self.spaceship_width,self.spaceship_height,0,(self.height / 2) - 10, (255,255,255))
        self.spaceship_speed = 5
        self.bullets = []
        self.bullet_width = 2
        self.bullet_height = 80
        self.bullet_color = (255,50,50)
        self.destroyer = []
        self.destroyer_width = 200
        self.destroyer_height = 200
        self.destroyer_color = (255,0,0)
        self.baddies = []
        self.baddie_width = 20
        self.baddie_height = 20
        self.baddie_color = (255,0,0)
        self.score = 0
        self.life = 5
        return


    def evolve(self, keys, newkeys, buttons, newbuttons, mouse_position):
        if pygame.K_LEFT in keys:
            self.spaceship.moveLeft(self.spaceship_speed)
        if pygame.K_RIGHT in keys:
            self.spaceship.moveRight(self.spaceship_speed,self.upper_limit)
        if pygame.K_UP in keys:
            self.spaceship.moveUp(self.spaceship_speed)
        if pygame.K_DOWN in keys:
            self.spaceship.moveDown(self.spaceship_speed,self.height)

        if pygame.K_SPACE in newkeys:
            self.bullets.append(self.spaceship.fire(self.bullet_width,self.bullet_height,self.bullet_color))

        if random.randint(1, self.frame_rate/2) == 1:
            self.addBaddie()

        for bullet in self.bullets:
            bullet.moveBullet()
            bullet.checkBackWall(self.width)
                
        for baddie in self.baddies:
            baddie.tick(0,0,self.height)

        for bullet in self.bullets:
            if not bullet.alive:
                continue
            for baddie in self.baddies:
                if not baddie.alive:
                    continue
                x,y,w,h = baddie.getDimensions()
                bullet.checkHitBaddie(x,y,w,h)
                if bullet.getHit():
                    bullet.setAlive(False)
                    bullet.hit = False
                    baddie.life -= 1
                if baddie.life <= 0:
                    hitsound = pygame.mixer.Sound("EX-PHS-7.wav")
                    hitsound.play()
                    self.score += 1
                    baddie.setAlive(False)

        for baddie in self.baddies:
            if not baddie.alive:
                   continue
            x,y,w,h = baddie.getDimensions()
            self.spaceship.checkHitBaddie(x,y,w,h)
            if self.spaceship.getHit():
                self.spaceship.setAlive(False)
                baddie.setAlive(False)
                self.spaceship.hit = False
                self.life -= 1
                if self.life <= 0:
                    pygame.quit()
                    exit()


        live_bullets = []
        live_baddies = []
        for bullet in self.bullets:
            if bullet.alive:
                live_bullets.append(bullet)
        for baddie in self.baddies:
            if baddie.alive:
                live_baddies.append(baddie)
      
        self.bullets = live_bullets
        self.baddies = live_baddies
            
        return


    def addDestroyer(self):
        x_point = 300
        new_destroyer = Destroyer(self.destroyer_width, self.destroyer_height, x_point, 0, self.destroyer_color)
        self.destroyer.append(new_destroyer)
        print ("Destroyer")
        return

    def addBaddie(self):
        x_point = 300 + random.randint(-250, 250)
        new_baddie = Baddie(self.baddie_width, self.baddie_height, x_point, 0, self.baddie_color)
        self.baddies.append(new_baddie)
        print ("TIE")  
        return



    def draw(self,surface):
        rect = pygame.Rect(0,0,self.width,self.height)
        surface.fill((0,0,0),rect )
        self.spaceship.draw(surface)
        for bullet in self.bullets:
            bullet.draw(surface)
        for baddie in self.baddies:
            baddie.draw(surface)
        self.drawTextLeft(surface, str(self.score), (0, 255, 0), 50, 50, self.font)
        self.drawTextRight(surface, str(self.life), (0, 255, 0), 500, 50, self.font)
        return     
    
    def drawTextLeft(self, surface, text, color, x, y,font):
        textobj = font.render(text, False, color)
        textrect = textobj.get_rect()
        textrect.bottomleft = (x, y)
        surface.blit(textobj, textrect)
        return

    def drawTextRight(self, surface, text, color, x, y,font):
        textobj = font.render(text, False, color)
        textrect = textobj.get_rect()
        textrect.bottomright = (x, y)
        surface.blit(textobj, textrect)
        return
