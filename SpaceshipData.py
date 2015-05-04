import pygame
import random
from spaceship import Spaceship
from baddie import Baddie
from stardestroyer import Destroyer
from powerup import Powerup
spaceship = Spaceship
gameover = False
adddestroyer = True
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
        self.powerups = []
        self.powerup_width = 20
        self.powerup_height = 20
        self.powerup_color = (50,255,50)
        self.destroyers = []
        self.destroyer_width = 200
        self.destroyer_height = 200
        self.destroyer_color = (255,0,0)
        self.baddies = []
        self.baddie_width = 20
        self.baddie_height = 20
        self.baddie_color = (255,0,0)
        self.score = 0
        self.baddie_kills = 0
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

        if self.baddie_kills == 10:
            print("your mom", len(self.powerups))
            self.addPowerup()
            print("again your mom", len(self.powerups))
            self.baddie_kills == 0

        if self.score == 50:
            adddestroyer = True
            if adddestroyer == True:
                self.addDestroyer()
                adddestroyer = False



        for bullet in self.bullets:
            bullet.moveBullet()
            bullet.checkBackWall(self.width)
                
        for baddie in self.baddies:
            baddie.tick(0,0,self.height)

        for powerup in self.powerups:
            powerup.tick(0,0,self.height)

        for destroyer in self.destroyers:
            destroyer.tick(0,0,self.height)

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
                    self.baddie_kills += 1
                    print self.baddie_kills
                    baddie.setAlive(False)
            for destroyer in self.destroyers:
                if not destroyer.alive:
                    continue
                x,y,w,h = destroyer.getDimensions()
                bullet.checkHitDestroyer(x,y,w,h)
                if bullet.getHit():
                    bullet.setAlive(False)
                    bullet.hit = False
                    destroyer.life -= 1
                if destroyer.life <= 0:
                    hitsound = pygame.mixer.Sound("EX-PHS-7.wav")
                    hitsound.play()
                    self.score += 40
                    destroyer.setAlive(False)
            for powerup in self.powerups:
                if not powerup.alive:
                    continue
                x,y,w,h = powerup.getDimensions()
                bullet.checkHitDestroyer(x,y,w,h)
                if bullet.getHit():
                    bullet.setAlive(False)
                    bullet.hit = False
                    powerup.life -= 1
                if powerup.life <= 0:
                    hitsound = pygame.mixer.Sound("EX-PHS-7.wav")
                    hitsound.play()
                    self.score += 0
                    powerup.setAlive(False)


        for destroyer in self.destroyers:
            if not destroyer.alive:
                   continue
            x,y,w,h = destroyer.getDimensions()
            self.spaceship.checkHitDestroyer(x,y,w,h)
            if self.spaceship.getHit():
                self.spaceship.setAlive(False)
                destroyer.life -= 10
                self.spaceship.hit = False
                self.life -= 1
                if self.life <= 0:
                    pygame.quit()
                    exit()

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

        for powerup in self.powerups:
            if not powerup.alive:
                   continue
            x,y,w,h = powerup.getDimensions()
            self.spaceship.checkHitPowerup(x,y,w,h)
            if self.spaceship.getHit():
                self.spaceship.setAlive(False)
                powerup.setAlive(False)
                self.spaceship.hit = False
                self.life += 5

        live_bullets = []
        live_baddies = []
        live_destroyers = []
        live_powerups = []
        for bullet in self.bullets:
            if bullet.alive:
                live_bullets.append(bullet)
        for baddie in self.baddies:
            if baddie.alive:
                live_baddies.append(baddie)
        for destroyer in self.destroyers:
            if destroyer.alive:
                live_destroyers.append(destroyer)
        for powerup in self.powerups:
            if powerup.alive:
                live_powerups.append(powerup)
      
        self.bullets = live_bullets
        self.baddies = live_baddies
        self.destroyers = live_destroyers
        self.powerups = live_powerups
            
        return


    def addDestroyer(self):
        x_point = 300
        new_destroyer = Destroyer(self.destroyer_width, self.destroyer_height, x_point, 0, self.destroyer_color)
        self.destroyers.append(new_destroyer)
        #print ("Destroyer")
        return

    def addBaddie(self):
        x_point = 300 + random.randint(-250, 250)
        new_baddie = Baddie(self.baddie_width, self.baddie_height, x_point, 0, self.baddie_color)
        self.baddies.append(new_baddie)
        #print ("TIE")  
        return

    def addPowerup(self):
        x_point = 300 + random.randint(-250, 250)
        new_powerup = Powerup(self.powerup_width, self.powerup_height, x_point, 0, self.powerup_color)
        self.powerups.append(new_powerup)
        print ("upgrade")  
        return

    def draw(self,surface):
        rect = pygame.Rect(0,0,self.width,self.height)
        surface.fill((0,0,0),rect )
        self.spaceship.draw(surface)
        for bullet in self.bullets:
            bullet.draw(surface)
        for baddie in self.baddies:
            baddie.draw(surface)
        for destroyer in self.destroyers:
            destroyer.draw(surface)
        for powerup in self.powerups:
            print("this is your mom")
            powerup.draw(surface)
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
