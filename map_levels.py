import random
import pygame
from pythonperlin import perlin
from tile import *
TILESIZE = 50



def randomColor():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    color = (r,g,b)
    return color
    
class ProceduralMap():
    
    
    def __init__(self,seed = 0):
        self.tiles = pygame.sprite.Group()
        self.backgroundTiles = pygame.sprite.Group()
        self.offloadedTiles = pygame.sprite.Group()

        
        self.color1 = randomColor()
        # print(color1)
        self.color2 = randomColor()
        self.generateTile(self.color1, self.color2)
        
            
        
        pass

    def generateTile(self, color1, color2,starx=0,stary=0):
        x = starx
        y = stary
        
        self.denx = 10
        self.deny = 10
        self.dens = 6
        self.octaves = 3
        noise = self.generatePerlin(self.denx, self.deny, self.dens, self.octaves) 
        for row in noise:
            x = starx
            for cell in row:
                self.buildTile(color1, color2, x, y, cell)
                x += 1
            y += 1
        
        self.generateGlobalRect()

    
    def generateGlobalRect(self):
        x,y = -1000000,-1000000
        x2,y2 = 1000000,1000000
        
        for tile in self.tiles.sprites():
            positionx = tile.rect.centerx
            positiony = tile.rect.centerx
            if positionx > x:
                x = positionx
            if positionx > x2:
                x2 = positionx
        
            if positiony > y:
                y = positiony
            if positiony > y2:
                y2 = positiony
        
        x2 = x2 - x
        y2 = y2 - y


        self.globalRect = pygame.rect.Rect(x,y,x2,y2)


        pass



    def generatePerlin(self, denx, deny, dens, octaves):
        noise = perlin((denx,deny),dens=dens,octaves=octaves)*255+255/2
        return noise

    def buildTile(self, color1, color2, x, y, cell,type = BackgroundTile):
        if cell > (255*3/4):
            add = cell//2
            color = color1
            newcolor = self.addheight(add, color)
            # newcolor = (0,0,0)
            tile = Tile(color = newcolor)
            tile.place(x,y)    
            self.offloadedTiles.add(tile)
        else:
            # floor = True
            add = cell//2
            color = color2
            newcolor = self.addheight(add, color)
            newcolor = self.darken(newcolor)
            tile = BackgroundTile(color = newcolor)
            tile.place(x,y)
            self.offloadedTiles.add(tile)
        
    def darken(self,color):
        newr = color[0]//2
        newg = color[1]//2
        newb = color[2]//2
        newcolor = (newr,newg,newb)
        return newcolor
        

    def addheight(self, add, color):
        newr = color[0] + add % 255
        newg = color[1] + add % 255
        newb = color[2] + add % 255
        newr = abs(int(newr)) % 255
        newg = abs(int(newg)) % 255
        newb = abs(int(newb)) % 255
        newcolor = (newr,newg,newb)
        return newcolor
    
    def updates(self,screen):
        
        screenarea = screen.get_rect()
        print(screenarea)
        for tile in self.offloadedTiles.sprites():
            if screenarea.colliderect(tile):
                print("Collision")
                if type(tile) == BackgroundTile:
                    self.backgroundTiles.add(tile)
                    self.offloadedTiles.remove(tile)
                if type(tile) == Tile:
                    self.tiles.add(tile)
                    self.offloadedTiles.remove(tile)
        print("Offloaded: ",len(self.offloadedTiles.sprites()))
        if screenarea.colliderect(self.globalRect):
            self.generateTile(self.color1, self.color2,0,-40)
        pass

    
    def draw(self,screen,player,hideUnseen = True):
        #unimplemented
        count = 0
        screenarea = screen.get_rect()
        for tile in self.backgroundTiles.sprites():
            if screenarea.colliderect(tile) and type(tile) == BackgroundTile:
                screen.blit(tile.image,tile.rect)
                count += 1
        
        screen.blit(player.body.image,player.body.rect)
        for tile in self.tiles.sprites():
            if screenarea.colliderect(tile) and type(tile) == Tile:
                screen.blit(tile.image,tile.rect)
                count += 1
        # if count < 230:
        #     self.generateTile(self.color1,self.color2,starx=0,stary=40)
            
        print("tiles rendered:", count)


    
    def save(self):
        
        pass

        
