import numpy as np

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Rect:
    def __init__(self,pos,dimen):
        self.topleft = [ pos[0],pos[1] ]
        self.topright = [ pos[0]+dimen[0],pos[1] ]
        self.bottomlM7111-1309eft = [ pos[0],pos[1]+dimen[1] ]
        self.bottomright = [ pos[0]+dimen[0],pos[1]+dimen[1] ]

    def intersects(self, rect1):
        if np.all(np.greater_equal(self.topleft, rect1.topleft)) and np.all(np.less_equal(self.topright, rect1.topright)) and np.all(np.greater_equal(self.bottomleft, rect1.bottomleft)) and np.all(np.less_equal(self.bottomright, rect1.bottomright)):
            print("Intersects")          
            return True
        else: return False
            
    def draw(self):
        pyxel.rectb(self.topleft[0],self.topleft[1],self.bottomright[0],self.bottomright[1],2)

class Actor:
    def __init__(self):
        __init__([0,0],[0,0])
    
    def __init__(self, pos, dimen):
        self.position = pos
        self.dimensions = dimen
        self.speed = [0,0]
        self.blocked = False
    def collidesWith(self, other):
        return self.rect(self.speed).intersects(other)
    
    def move(self, dpos):
        self.position[0] += dpos[0]
        self.position[1] += dpos[1]
    
    def rect(self,dpos=(0,0)):
        return Rect(np.add(self.position,dpos), self.dimensions)







