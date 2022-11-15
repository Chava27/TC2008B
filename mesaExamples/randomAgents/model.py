from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agent import RandomAgent, ObstacleAgent, TrashAgent

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, P, max_time, width, height):
        self.max_time=max_time
        self.time = 0
        self.num_agents = N
        self.num_trash_percentage= P
        self.grid = MultiGrid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True 

        self.datacollector = DataCollector( 
        agent_reporters={
            "Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0,
            "Trash": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0
            }
        )

        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.grid.place_agent(obs, pos)

        # Add the agent to a random empty grid cell
        for i in range(self.num_agents):
            a = RandomAgent(i+1000, self) 
            self.schedule.add(a)
            #pos_agent = lambda w, h: (self.random.randrange(1,w-1), self.random.randrange(1,h-1))
            #position = pos_agent(self.grid.width, self.grid.height)
            #All agents start at random position
            #self.grid.place_agent(a, position)
            ##All agents start at the same position
            self.grid.place_agent(a, (1,1))

        # Add the trash to a random empty grid cell
        #Define possible cells that might containt trash (exclude borders and cell that contains the Roomba Agents 1,1)
        possible_cells = round(((width*height)-((width*2)-((height-2)))-1)*(P*0.01))

        for i in range(possible_cells):
            a= TrashAgent("trash", self)
            #Define possible position of trash, not counting the borders
            pos_trash= lambda w, h: (self.random.randrange(1,w), self.random.randrange(1,h))
            pos = pos_trash(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_trash(self.grid.width, self.grid.height)
            self.grid.place_agent(a, pos)
            
        self.datacollector.collect(self) #collect the data from the steps  

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)
        self.time +=1
        if self.time == self.max_time - 1:
            self.running = False