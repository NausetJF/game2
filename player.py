
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

        
        pass


    def move(self,x,y):
        # print(x,y)
        IsMoving = x != 0 or y != 0
        if IsMoving: 
            self.velocity.x += x*3
            self.velocity.y += y*3
            
            self.position.x += self.velocity.x
            self.position.y += self.velocity.y
        else:
            self.velocity.x = self.velocity.x//2
            self.velocity.y = self.velocity.y//2
            if abs(self.velocity.x) == 1 or abs(self.velocity.y) == 1:
                self.stop()
            
        print("")
        print("position: ",self.position.x,self.position.y)
        print("velocity: ",self.velocity.x,self.velocity.y)

    def stop(self):
        self.velocity.x = 0
        self.velocity.y = 0
        
        