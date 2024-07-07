import random
import pygame
from pythonperlin import perlin
from tile import *
# TILESIZE = 200



def randomColor():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    color = (r,g,b)
    return color


class Grid(pygame.sprite.Sprite):
    
    
    def __init__(self,image,rect):
        super().__init__()
        self.image = image
        self.rect = rect
        self.tiles = pygame.sprite.Group()
        self.backgroundTiles = pygame.sprite.Group()
        self.loaded = False
    
    def move(self,x,y):
        self.rect.centerx += x
        self.rect.centery += y
        if not self.loaded:
            for tile in self.tiles.sprites():
                tile.move(x,y)
            for tile in self.backgroundTiles.sprites():
                tile.move(x,y)

class ScreenReference():
    def __init__(self,rect):
        self.rect = rect
            
        pass

    def move(self,x,y):
        self.rect.centerx += x
        self.rect.centery += y




class ProceduralMap():
    
    
    def __init__(self,screen,seed = 0):
        self.tiles = pygame.sprite.Group()
        self.backgroundTiles = pygame.sprite.Group()
        self.offloadedTiles = pygame.sprite.Group()
        self.grid = pygame.sprite.Group()
        
        self.size = random.randint(1,1)
        
        self.screenarea = ScreenReference(screen.get_rect())


        self.color1 = randomColor()
        # print(color1)
        self.color2 = randomColor()
        
        self.generateTile(self.color1, self.color2)
        self.generateGrid()
        self.name = self.generateWorldName()
        self.dayColor = self.color1
        self.nightColor = self.color2
        self.stank = random.randint(255//6,(255//2))
        self.dayduration = random.randint(100,1000)
        self.time = 0

        pass
    
    def getAtmosphere(self):
        self.time = (self.time + 1) % self.dayduration
        if self.time > (self.dayduration // 2):
            return self.nightColor
        else:
            return self.dayColor

    def generateGrid(self):
        gridsize = TILESIZE*20
        # gridsize = TILESIZE*2
        # gridsize = TILESIZE*40
        print(gridsize)
        gridSprites = pygame.sprite.Group()
        
        for x in range(0,gridsize*10,gridsize-1):
            for y in range(0,gridsize*10,gridsize-1):
                # print(x,y)
                gridtile = Tile("white",gridsize)
                gridtile.move(x-1,y-1)
                gridSprites.add(gridtile)
        # print(len(gridSprites.sprites()))
        for grid in gridSprites.sprites():
            newimage = pygame.surface.Surface((gridsize,gridsize))
            newimage.fill("black")
            newrect = newimage.get_rect()
            newrect.centerx = grid.rect.centerx
            newrect.centery = grid.rect.centery
            newGrid = Grid(newimage,newrect)
        # print(newGrid.rect.centerx,newGrid.rect.centery)
            # print(len(newGrid.backgroundTiles.sprites()+newGrid.tiles.sprites()))
            # newGrid.image = 
            # newGrid.rect = 
            for tile in self.offloadedTiles.sprites():
                if newGrid.rect.colliderect(tile):
                    if type(tile) == BackgroundTile:
                        # lasttile = tile
                        newGrid.backgroundTiles.add(tile)
                        self.offloadedTiles.remove(tile)
                    if type(tile) == Tile:
                        # lasttile = tile
                        newGrid.tiles.add(tile)
                        self.offloadedTiles.remove(tile)
            print(len(newGrid.backgroundTiles.sprites()+newGrid.tiles.sprites()))
            self.grid.add(newGrid)
        print(len(self.grid.sprites()))
        pass


    def generateWorldName(self):
        firstsyl = ["end","wilt","bark","fire","fawn","aura"]
        secondsyl = ["er","or","e","a"]
        endsyl = ["ian","wood","town"]
        sylables = random.randint(1,10)
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
        self.dens = 6*self.size
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
        
        # print(screenarea)
        screenarea = screen.get_rect()
        # self.tiles = pygame.sprite.Group()
        # self.backgroundTiles = pygame.sprite.Group()
        count = 0
        for cube in self.grid.sprites():
            if cube.rect.colliderect(screenarea):
                count += 1
                # print("collision",cube.rect.centerx,cube.rect.centery)
                # self.tiles = grid.tiles
                cube.loaded = True
                self.tiles.add(cube.tiles.sprites())
                self.backgroundTiles.add(cube.backgroundTiles.sprites())
                # self.backgroundTiles = grid.backgroundTiles
            else:
                self.tiles.remove(cube.tiles)
                cube.loaded = False
                self.backgroundTiles.remove(cube.backgroundTiles)
                # self.backgroundTiles = grid.backgroundTiles
        print("count",count)
        print("tiles",len(self.tiles.sprites()))
        print("backgroundTiles",len(self.backgroundTiles.sprites()))
            # lasttile = self.offloadedTiles.sprites()[0]
        # for tile in self.offloadedTiles.sprites():
        #     if screenarea.colliderect(tile):
        #         print("Collision")
        #         if type(tile) == BackgroundTile:
        #             # lasttile = tile
        #             self.backgroundTiles.add(tile)
        #             self.offloadedTiles.remove(tile)
        #         if type(tile) == Tile:
        #             # lasttile = tile
        #             self.tiles.add(tile)
        #             self.offloadedTiles.remove(tile)
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
        # print("Offloaded: ",len(self.offloadedTiles.sprites()))
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
            
        # print("tiles rendered:", count)


    
    def save(self):
        
        pass

# print(ProceduralMap.generateName(self=None))
