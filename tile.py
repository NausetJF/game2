
import pygame


TILESIZE = 50

class Tile(pygame.sprite.Sprite):
    
    def __init__(self,color,size = TILESIZE,solid = True):
        super().__init__()
        if solid == True: 
            size += 20
        self.image = pygame.Surface([size,size])
        # print(color)
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
        