import pyxel
import numpy as np

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

class PyxelActor(Actor):
    def __init__(self, pos, dimen, color=0):
        Actor.__init__(self, pos,dimen)
        self.color = color
    def draw(self):
        pyxel.rect(self.position[0],self.position[1],self.position[0]+self.dimensions[0], self.position[1]+self.dimensions [1],  self.color)


class Box(PyxelActor):
    def __init__(self, pos,dimen):
        PyxelActor.__init__(self,pos,dimen,Color.BLUE)
        self.onTarget =  False;
        
    def update(self):
        if not self.blocked:
            self.move(self.speed)
        self.blocked = False
        self.speed = [0,0]


class Wall(PyxelActor):
    def __init__(self, pos,dimen):
        PyxelActor.__init__(self,pos,dimen,Color.PURPLE)
        
    def update(self):
        pass

class Player(PyxelActor):
    def __init__(self, pos,dimen):
        PyxelActor.__init__(self,pos,dimen,Color.RED )
    def update(self):
        if not self.blocked:
            self.move(self.speed)
        self.blocked = False
        self.speed = [0,0]
        
      
class Target(PyxelActor):
    def __init__(self, pos,dimen):
        PyxelActor.__init__(self,pos,dimen,Color.GREEN) 
        self.fulfilled = False 
    def update(self):
        if self.fulfilled:
            self.color = 3
        else:
            self.color = Color.GREEN



class App:
    ACTOR_SIZE = [8,8]
    def __init__(self):
        pyxel.init(255,255,scale=4 )
       
        self.actors = []
        self.level = 1
        self.complete = True # Set to true so first level will be read
        self.targetsleft=0
        pyxel.run(self.update, self.draw)
        
    
    def reset(self):
        self.actors = []
        self.player=None 
        #lf.level = 1
        self.complete = False
        self.targetsleft=0
 

    def readFromFile(self,fn, lvl=1):
        x = 0
        y = 0
        marker = "\0"
        i = 1

        with open(fn, 'r') as f:# Read until Level is reached
           for line in f:
                if marker in line:
                    i = i+1
                if lvl != i:
                    continue
                
                x = 0
                y += App.ACTOR_SIZE[1]
                for char in line:
                    if char == '#': self.actors.append(Wall([x,y],App.ACTOR_SIZE))
                    if char == '@': self.player = Player([x,y],App.ACTOR_SIZE)
                    if char == '.': self.actors.append(Target([x,y],App.ACTOR_SIZE))
                    if char == '*': pass # box + target
                    if char == '+': 
                        self.player = Player([x,y],App.ACTOR_SIZE)# Player + target
                        self.actors.append(Target([x,y],App.ACTOR_SIZE))
                    if char == '$': self.actors.append(Box([x,y],App.ACTOR_SIZE))
                    if char == ' ': pass
                    x += App.ACTOR_SIZE[0]
    def checkCollision(self, obj):
        for actor in self.actors:
            if obj.collidesWith(actor.rect()):
                 # collison behaviours
                if  isinstance(actor, Target) and isinstance(obj, Box):
                    # Ontarget
                    actor.fulfilled = True
                elif isinstance(actor, Target) and isinstance(obj, Player):
                    # Ontarget
                    actor.fulfilled = False
                elif  isinstance(actor, Wall):
                    obj.blocked = True
                    self.player.blocked = True
                elif isinstance(obj, Box) and isinstance(actor, Box):
                    obj.blocked = True
                    self.player.blocked = True
                elif isinstance(actor, Box):
                    actor.speed = obj.speed
                    self.checkCollision(actor)

    def update(self):
        # either first load or is complete
        if self.complete == True:
            self.reset()
            self.readFromFile("/home/john/level.data",self.level)
             
        # Do any screen updates
        if pyxel.btnp(pyxel.KEY_W):
            self.player.speed[1]=-self.ACTOR_SIZE[1]
        elif pyxel.btnp(pyxel.KEY_S):
            self.player.speed[1]=self.ACTOR_SIZE[1]
        elif pyxel.btnp(pyxel.KEY_D):
            self.player.speed[0]=self.ACTOR_SIZE[0]
        elif pyxel.btnp(pyxel.KEY_A):
            self.player.speed[0]=-self.ACTOR_SIZE[0];
        elif pyxel.btnp(pyxel.KEY_R):
            self.complete=True  
        elif pyxel.btnp(pyxel.KEY_N ):
            self.complete=True
            self.level=self.level+1
        
        else: self.player.speed = [0,0]
        # Updated actors
        self.checkCollision(self.player)
        
        # Reset target count and then update based on each target's state
        self.targetsleft=0
        for actor in self.actors: 
            if isinstance(actor, Target) and not actor.fulfilled: 
                 self.targetsleft =  self.targetsleft+1
            actor.update()
        #If target count stillzero, the level is complete
        if self.targetsleft==0: 
            self.complete=True
            self.level=self.level+1
        self.player.update()
        

    
    def draw(self):
        pyxel.cls(0)
        for actor in self.actors:
            actor.draw()
        self.player.draw()
        pyxel.text(0, 0, "Targets left: " + str(self.targetsleft), 5)
        pyxel.text(0, 7,"Level: "+ str(self.level), 5)
App()
