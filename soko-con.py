class Box(PyxelActor):
    def __init__(self, pos,dimen):
        PyxelActor.__init__(self,pos,dimen)
        self.onTarget = False;
    def update(self):
        if not self.blocked:
            self.move(self.speed)
        self.blocked = False
        self.speed = [0,0]
    def draw(self):
        pyxel.rect( self.position[0],self.position[1],  self.position[0]+self.dimensions [0], self.position[1]+self.dimensions [1], 3)

class Wall(PyxelActor):
    def __init__(self, pos,dimen):
        PyxelActor.__init__(self,pos,dimen)
    def update(self):
        pass
    def draw(self):
        pyxel.rect( self.position[0],self.position[1],  self.position[0]+self.dimensions [0], self.position[1]+self.dimensions [1], 1)

class Player(PyxelActor):
    def __init__(self, pos,dimen):
        PyxelActor.__init__(self,pos,dimen)
    def update(self):
        if not self.blocked:
            self.move(self.speed)
        self.blocked = False
        self.speed = [0,0]
        
    def draw(self):
        #pyxel.circ( self.position[0],self.position[1],  self.dimensions [0]/1.6, 3)
        pyxel.rect( self.position[0],self.position[1],  self.position[0]+self.dimensions [0], self.position[1]+self.dimensions [1], 2)

class Target(Actor):
    def __init__(self, pos,dimen):
        PyxelActor.__init__(self,pos,dimen)
        self.fulfilled = False
        self.color = 2
    def update(self):
        if self.fulfilled:
            self.color = 4
        else: self.color = 2
    def draw(self):
        pyxel.rectb(self.position[0],self.position[1],self.position[0]+self.dimensions[0], self.position[1]+self.dimensions [1],  self.color)


class App:
    ACTOR_SIZE = [8,8]
    
    def __init__(self):
        pyxel.init(1024, 980)
        self.actors = []
        self.readFromFile("levels.txt")
        pyxel.run(self.update, self.draw)
        self.targetsleft=0
M7111-1309M7111-1309M7111-1309    def readFromFile(self,fn, lvl=1):
        x = 0
        y = 0
        marker = "\0"
        i = 1

        with open(fn, 'r') as f:
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
                    if char == '*': pass
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
        # Do any screen updates
        if pyxel.btnp(pyxel.KEY_W):
            self.player.speed[1]=-self.ACTOR_SIZE[1]
        elif pyxel.btnp(pyxel.KEY_S):
            self.player.speed[1]=self.ACTOR_SIZE[1]
        elif pyxel.btnp(pyxel.KEY_D):
            self.player.speed[0]=self.ACTOR_SIZE[0]
        elif pyxel.btnp(pyxel.KEY_A):
            self.player.speed[0]=-self.ACTOR_SIZE[0];
        else: self.player.speed = [0,0]
        # Updated actors
        self.checkCollision(self.player)
        
        self.targetsleft=0
        for actor in self.actors: 
            if isinstance(actor, Target) and not actor.fulfilled: 
                 self.targetsleft =  self.targetsleft+1
            actor.update()
        self.player.update()
        

    
    def draw(self):
        pyxel.cls(0)
        for actor in self.actors:
            actor.draw()
        self.player.draw()
        pyxel.text(0, 0, "Targets left: " + str(self.targetsleft), 5)
App()
