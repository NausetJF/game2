import random
import pygame
from pythonperlin import perlin

TILESIZE = 50



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
                self.buildTile(color1, color2, x, y, cell)
                x += 1
            y += 1
            
            
        
        pass

    def buildTile(self, color1, color2, x, y, cell,type = BackgroundTile):
        if cell > (255/2):
            add = cell//2
            color = color1
            newcolor = self.addheight(add, color)
            tile = BackgroundTile(color = newcolor)
            tile.place(x,y)    
        else:
            add = cell//2
            color = color2
            newcolor = self.addheight(add, color)
            tile = Tile(color = newcolor)
            tile.place(x,y)
        self.tiles.add(tile)
        

    def addheight(self, add, color):
        newr = color[0] + add % 255
        newg = color[1] + add % 255
        newb = color[2] + add % 255
        newr = abs(int(newr)) % 255
        newg = abs(int(newg)) % 255
        newb = abs(int(newb)) % 255
        newcolor = (newr,newg,newb)
        return newcolor
    
    
    def draw(self,screen,hideUnseen = True):
        #unimplemented
        count = 0
        screenarea = screen.get_rect()
        for tile in self.tiles.sprites():
            if screenarea.colliderect(tile):
                screen.blit(tile.image,tile.rect)
                count += 1
        print("tiles rendered:", count)
        
        
