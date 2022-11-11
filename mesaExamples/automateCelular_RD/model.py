from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid

from cell import Cell

class ConwaysCelularAuto(Model):
    def __init__(self, height=50, width=50, density = 0.1):
        self.schedule = SimultaneousActivation(self)
        self.grid= Grid(height,width,torus=True)

        for (contents, x,y) in self.grid.coord_iter():
            cell = Cell((x,y),self)
            if self.random.random()<density:
                cell.state= cell.ALIVE
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)
        self.running= True

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()