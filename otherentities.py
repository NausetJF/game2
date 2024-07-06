import pygame


class Entity(pygame.sprite.Sprite):

    def __init__(self,x,y):
        
        self.image = pygame.Surface([30,30])
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.place(x,y)


        self.act = 0 
        self.actTolerance = 10
        
        pass

    def place(self,x,y):
        self.rect.centerx = x
        self.rect.centery = y
         
        pass

    def move(self,x,y):
        self.rect.centerx += x
        self.rect.centery += y

    def timeToAct(self):
        answer = self.act % self.actTolerance == 0
        if answer:
            print("time to act")
        self.act += 1 
        return answer

    def update(self):
        
        if self.timeToAct:
            self.move(1,0)
        
        
        pass