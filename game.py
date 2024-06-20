import player
import maplevel

import pygame
import random
import gc
from pythonperlin import perlin
# import colour

pygame.init()

screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True


mapstage = maplevel.ProcMap()
player = player.Player() 


while running: 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #coasting 
    
    player.move(0,0)
    
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_r]:
        del mapstage
        mapstage = maplevel.ProcMap()
        # TILESIZE = random.randint(2,60)
    if keys[pygame.K_w]:
        player.move(0,4)
    if keys[pygame.K_s]:
        player.move(0,-4)
    if keys[pygame.K_a]:
        player.move(4,0)
    if keys[pygame.K_d]:
        player.move(-4,0)
    if keys[pygame.K_q]:
        running = False   
    if keys[pygame.K_f]:
        print()
    
    
    # print(keys)
    # print(player.position.x,player.position.y)
    for tile in mapstage.tiles.sprites():
        tile.move(player.velocity.x,player.velocity.y)
    
    
    
    
    screen.fill("black")
    
    
    
    
    
    mapstage.tiles.draw(screen)
    pygame.display.flip()
    
    # clock.tick(60)
    
    
    pass