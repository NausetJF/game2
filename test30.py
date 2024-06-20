import gc
import random
import pygame
from pythonperlin import perlin
# import colour

pygame.init()

screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True
TILESIZE = 30

class Tile(pygame.sprite.Sprite):
    
    def __init__(self,color,size = TILESIZE,solid = True):
        super().__init__()
        self.image = pygame.Surface([size,size])
        print(color)
        self.image.fill(color=color)
        self.rect = self.image.get_rect()
        self.solid = solid
        
    def place(self,x,y):
        self.rect.centerx = TILESIZE*x
        self.rect.centery = TILESIZE*y
    
    def move(self,x,y):
        self.rect.centerx += x
        self.rect.centery += y
    
    
class BackgroundTile(Tile):
    
    def __init__(self, color, size=TILESIZE, solid=False):
        super().__init__(color, size, solid)
        
def randomcolor():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    color = (r,g,b)
    return color
    
class ProcMap():
    
    
    def __init__(self,seed = 0):
        self.tiles = pygame.sprite.Group()
        

        noise = perlin((40,40),dens=6,octaves=3)*255+255/2
        
        color1 = randomcolor()
        print(color1)
        color2 = randomcolor()
        x = 0
        y = 0
        
        for row in noise:
            x = 0
            for cell in row:
                if cell > (255/2):
                    cellheight = cell//2
                    color = color1
                    newcolor = self.addheight(cellheight, color)
                    tile = BackgroundTile(color = newcolor)
                    tile.place(x,y)    
                else:
                    cellheight = cell//2
                    color = color2
                    newcolor = self.addheight(cellheight, color)
                    tile = Tile(color = newcolor)
                    tile.place(x,y)
                self.tiles.add(tile)
                x += 1 
            y += 1
            
            
        
        pass

    def addheight(self, cellheight, color):
        newr = color[0] + cellheight % 255
        newg = color[1] + cellheight % 255
        newb = color[2] + cellheight % 255
        newr = abs(int(newr)) % 255
        newg = abs(int(newg)) % 255
        newb = abs(int(newb)) % 255
        newcolor = (newr,newg,newb)
        return newcolor

map = ProcMap()

class Position():
    
    def __init__(self,x,y):
            
        self.x = x
        self.y = y
        
        
        pass

#just controls the camera 
class Player():
    
    def __init__(self):
        self.position = Position(0,0)
        

        
        pass
        


while running: 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_r]:
        del map
        map = ProcMap()
        # TILESIZE = random.randint(2,60)
    
    screen.fill("black")
    
    
    
    
    
    map.tiles.draw(screen)
    pygame.display.flip()
    
    clock.tick(60)
    
    
    pass