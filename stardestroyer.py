class Destroyer():

    def __init__(self,width,height,x,y,color):
        self.image = pygame.image.load("star_destroyer.png")
        self.width  = 200
        self.height = 200
        self.x      = x
        self.y      = y
        self.new_x  = x
        self.new_y  = y
        self.speed  = 3
        self.color  = color
        self.alive  = True
        self.life = 50
        return

    def tick(self,back_wall,upper_wall,lower_wall):
        self.new_y = self.y + self.speed
        self.new_x = self.x - random.randint(-1, 1)
        if self.new_y >= lower_wall:
            self.setAlive(False)
        else:
            self.y = self.new_y
        self.y = self.new_y
        self.x = self.new_x
        return self.alive

    def getAlive(self):
        return self.alive

    def getDimensions(self):
        return self.x,self.y,self.width,self.height

    def setAlive(self,alive):
        self.alive = alive

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        #rect = pygame.Rect( self.x, self.y, self.width, self.height )
        #pygame.draw.rect(surface, self.color, rect)
        return