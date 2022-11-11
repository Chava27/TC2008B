from mesa import Agent

class Cell(Agent):
    DEAD = 0
    ALIVE = 1

    def __init__(self, pos, model, init_state=DEAD):
        super().__init__(pos, model)
        self.x, self.y = pos
        self.pos= pos
        self.state = init_state
        self._nextState = None

    def isAlive(self):
        return self.state == self.ALIVE

    def isDead(self):
        return self.state == self.DEAD

    def coord_x(self):
        return self.x
    
    def coord_y(self):
        return self.y

    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)
    
    def upperNeigStatus(self,list):
        if list[0].isAlive() and list[1].isAlive() and list[2].isAlive():
            return False
        elif list[0].isAlive() and list[1].isAlive() and list[2].isDead():
            return True
        elif list[0].isAlive() and list[1].isDead() and list[2].isAlive():
            return False
        elif list[0].isAlive() and list[1].isDead() and list[2].isDead():
            return True
        elif list[0].isDead() and list[1].isAlive() and list[2].isAlive():
            return True
        elif list[0].isDead() and list[1].isAlive() and list[2].isDead():
            return False
        elif list[0].isDead() and list[1].isDead() and list[2].isAlive():
            return True
        else:
            return False
    
    def step(self):
        upper_neighbors= [neighbor for neighbor in self.neighbors() if neighbor.coord_y() == (self.coord_y()+1)%50]
        if self.upperNeigStatus(upper_neighbors):
            self._nextState= self.ALIVE
        else:
            self._nextState=self.DEAD

    def advance(self):
        self.state = self._nextState