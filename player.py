import map_levels
import pygame


class Position():
    def __init__(self,x,y):
            
        self.x = x
        self.y = y
        
        
        pass

#just controls the camera 
class Player():
    
    def __init__(self,x = 0, y = 0):
        self.position = Position(x,y)
        self.velocity = Position(x,y)
        self.body = pygame.sprite.Sprite()
        self.body.image = pygame.Surface((30,30))
        self.body.image.fill("white")
        self.body.rect = self.body.image.get_rect()
        self.body.rect.centerx += 1280//2
        self.body.rect.centery += 720//2
        
        
        pass

    def update(self,mapstage):
        
        keys = pygame.key.get_pressed()
        touchedObject = pygame.sprite.spritecollideany(self.body,mapstage.tiles)
        # print("touchedObject: ",touchedObject)
        if keys[pygame.K_w]:
            self.collisionPhysics(touchedObject, 0, 4)
        if keys[pygame.K_s]:
            # self.move(0,-4)
            self.collisionPhysics(touchedObject, 0, -4)
        if keys[pygame.K_a]:
            # self.move(4,0)
            self.collisionPhysics(touchedObject, 4, 0)
        if keys[pygame.K_d]:
            # self.move(-4,0)
            self.collisionPhysics(touchedObject, -4, 0)

    def collisionPhysics(self, touchedObject, x, y):
        if touchedObject == None or str(type(touchedObject)) == "<class 'maplevel.BackgroundTile'>":
            self.move(x,y)
        else: 
            dirx = (self.body.rect.centerx - touchedObject.rect.centerx)//4
            diry = (self.body.rect.centery - touchedObject.rect.centery)//4
            print(type(touchedObject))
            print("collision knockback: ",dirx,diry)
            if dirx < diry:
                self.move(-dirx,0)
            else:
                self.move(0,-diry)
    
    
    def move(self,x,y):
        # print(x,y)
        IsMoving = x != 0 or y != 0
        if IsMoving: 
            self.velocity.x += x
            self.velocity.y += y
            
            self.position.x += self.velocity.x
            # self.body.rect.centerx += self.velocity.x
            self.position.y += self.velocity.y
            # self.body.rect.centery += self.velocity.y
        else:
            self.velocity.x = self.velocity.x//2
            self.velocity.y = self.velocity.y//2
            if abs(self.velocity.x) == 1 or abs(self.velocity.y) == 1:
                self.stop()
        
        # self.body.rect.centerx = self.position.x
        # self.body.rect.centery = self.position.y
        
        # print("")
        # print("position: ",self.position.x,self.position.y)
        # print("velocity: ",self.velocity.x,self.velocity.y)

    def stop(self):
        self.velocity.x = 0
        self.velocity.y = 0
        
        