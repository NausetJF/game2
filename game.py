import player
import map_levels

import pygame
import random
import gc
from pythonperlin import perlin
# import colour
import otherentities
pygame.init()

screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True

mapStage = map_levels.ProceduralMap()
player = player.Player() 
entity = otherentities.Entity(50,50)
entities = [entity]

while running: 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #coasting 
    
    player.move(0,0)
    
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_r]:
        del mapStage
        mapStage = map_levels.ProceduralMap()
        while (pygame.sprite.spritecollideany(player.body,mapStage.tiles)):
            mapStage = map_levels.ProceduralMap()
        
        # TILESIZE = random.randint(2,60)
    player.update(mapStage)
    if keys[pygame.K_q]:
        running = False   
    if keys[pygame.K_f]:
        print()
    
    
    # print(keys)
    # print(player.position.x,player.position.y)
    
    
    #moving the camera 
    for tile in mapStage.tiles.sprites():
        tile.move(player.velocity.x,player.velocity.y)
    for tile in mapStage.backgroundTiles.sprites():
        tile.move(player.velocity.x,player.velocity.y)
    for tile in mapStage.offloadedTiles.sprites():
        tile.move(player.velocity.x,player.velocity.y)
    for thing in entities:
        thing.move(player.velocity.x,player.velocity.y)
        screen.blit(thing.image,thing.rect)
    
    
    
     
    screen.fill("black")
    
    
    
    
    mapStage.updates(screen)
    mapStage.draw(screen,player)
    for thing in entities:
        screen.blit(thing.image,thing.rect)
    pygame.display.flip()

    hudfont = pygame.font.SysFont(None,size=50,bold=True,italic=True)
    MapName = mapStage.name
    hudimg = hudfont.render(MapName,True,"white","black")


    screen.blit(hudimg,(10,10))

    
    clock.tick(60*2)
    
    
    pass
