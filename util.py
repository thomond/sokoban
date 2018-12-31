import numpy as np
import pyxel
from const import * 

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Rect:
    def __init__(self,pos,dimen):
        self.topleft = [ pos[0],pos[1] ]
        self.topright = [ pos[0]+dimen[0],pos[1] ]
        self.bottomleft = [ pos[0],pos[1]+dimen[1] ]
        self.bottomright = [ pos[0]+dimen[0],pos[1]+dimen[1] ]

    def intersects(self, rect1):
        if np.all(np.greater_equal(self.topleft, rect1.topleft)) and np.all(np.less_equal(self.topright, rect1.topright)) and np.all(np.greater_equal(self.bottomleft, rect1.bottomleft)) and np.all(np.less_equal(self.bottomright, rect1.bottomright)):
            #print("Intersects")
            return True
        else: return False
            
    def draw(self):
        pyxel.rectb(self.topleft[0],self.topleft[1],self.bottomright[0],self.bottomright[1],2)

class Actor:
    def __init__(self):
        PyxelActor.__init__(self,pos,dimen)
        
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

class Color:
    RED = 8
    BLUE = 12
    GREEN = 11
    PURPLE = 2

class Frame:
    def __init__(self,x,y,w,h):
        self._w = w
        self._h = h
        self._x = x
        self._y = y

    @property
    def w(self):
        return self._w
    @property
    def h(self):
        return self._h
    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    @w.setter
    def w(self,val):
        self._w = val
    @h.setter
    def h(self,val):
        self._h = val
    @x.setter
    def x(self,val):
        self._x = val
    @y.setter
    def y(self,val):
         self.y = val

class Animation:
    @property
    def w(self):
        return self.animations[self.i].w
    @property
    def h(self):
        return self.animations[self.i].h
    @property
    def x(self):
        return self.animations[self.i].x
    @property
    def y(self):
        return self.animations[self.i].y
    
    
    def __init__(self, framedata,fsz):
        self.animations = list()
        for frame in framedata:
            self.animations.append( Frame(frame[0], frame[1], fsz[0], fsz[1] )) 
        self.i = 0
    def next(self):
        if len(self.animations) == self.i+1: self.i = 0
        else: self.i = self.i+1


class PyxelActor(Actor):
    def __init__(self, pos,dimen, color=-1, framedata=None, _id=None):
        Actor.__init__(self, pos,dimen)
        self.color = color
        self.imgBank = 0
        self.alpha = 14
        self.id = _id
        if framedata is None: pass
        elif type(framedata) is tuple : # single frame - no animation
            self.animations = Frame(framedata[0],framedata[1], dimen[0], dimen[1])
            self.ani = self.animations 

        elif len(framedata)>1:
            # Animation is a series of framing 
            self.animations = []
            for i in range(len(framedata)):
               self.animations.append(Animation(framedata[i], dimen))
            self.ani = self.animations[0] 
    def draw(self):
        if self.color != -1:
            pyxel.rect( self.position[0],self.position[1],  self.position[0]+self.dimensions [0], self.position[1]+self.dimensions [1], self.color)
        else:
            pyxel.blt(self.position[0], self.position[1] ,self.imgBank, self.ani.x , self.ani.y , self.ani.w , self.ani.h,self.alpha)
    
    def setAni(self,index):
        # TODO: check for presence of anis and indexis valid
        self.ani = self.animations[index]

        

