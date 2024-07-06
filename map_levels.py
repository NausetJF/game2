import random
import pygame
from pythonperlin import perlin
from tile import *
TILESIZE = 200



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
        
        self.name = self.generateWorldName()
        self.atmosphereColor = randomColor()
        self.nightColor = randomColor()
        self.dayduration = random.randint(10,500)
        self.size = random.randint(100,1000)
        
        pass
    

    def generateWorldName(self):
        firstsyl = ["end","wilt","bark","fire","fawn","aura"]
        secondsyl = ["er","or","e","a"]
        endsyl = ["ian","wood","town"]
        sylables = random.randint(2,3)
        if sylables == 2:
            name = random.choice(firstsyl)+random.choice(endsyl)
        else:
            name = random.choice(firstsyl)+random.choice(secondsyl)+random.choice(endsyl)
        return name


    def generateTile(self, color1, color2,starx=0,stary=0):
        x = starx
        y = stary
        
        self.denx = 20
        self.deny = 20
        self.dens = 6
        self.octaves = 3
        noise = self.generatePerlin(self.denx, self.deny, self.dens, self.octaves) 
        for row in noise:
            x = starx
            for cell in row:
                self.buildTile(color1, color2, x, y, cell)
                x += 1
            y += 1

    
    

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
            # lasttile = self.offloadedTiles.sprites()[0]
        for tile in self.offloadedTiles.sprites():
            if screenarea.colliderect(tile):
                print("Collision")
                if type(tile) == BackgroundTile:
                    # lasttile = tile
                    self.backgroundTiles.add(tile)
                    self.offloadedTiles.remove(tile)
                if type(tile) == Tile:
                    # lasttile = tile
                    self.tiles.add(tile)
                    self.offloadedTiles.remove(tile)
            # else:
            #     lastilex = lasttile.rect.centerx
            #     lastiley = lasttile.rect.centery
            #     positionx = screenarea.centerx
            #     positiony = screenarea.centery

            #     directionx = positionx - lastilex
            #     directiony = positiony - lastiley
            #     if directionx > directiony:
            #         directiony = 0
            #         self.generateTile(self.color1,self.color2,40,0)
            #     if directiony > directionx:
            #         directionx = 0
            #         self.generateTile(self.color1,self.color2,0,40)
                
            #     pass
        print("Offloaded: ",len(self.offloadedTiles.sprites()))
        # if not screenarea.colliderect(self.globalRect):
        #     print("Outside")
        #     self.generateTile(self.color1, self.color2,0,-40)
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

# print(ProceduralMap.generateName(self=None))
