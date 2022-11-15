from mesa import Agent

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0
        self.trash_taken= 0

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) 

        #For every possible steps, it is important to know which of them does the agent can move to. If the next cell to move contains trash or is empty it can move.
        next_steps = []
        for step in possible_steps:
            #cell container gets the agent that is in the cell to move. If there is a trash agent or it is empty then it is considered as true, thus a possibility of moving. If it is not a valid move then then it adds a bool False.
            cell_container= self.model.grid.get_cell_list_contents(step)
            if not self.model.grid.is_cell_empty(step):
                if cell_container[0].unique_id == "trash":
                    next_steps.append(True)
                else:
                    next_steps.append(False)
            else:
                next_steps.append(True)

        #While this list comprehension returns us new list which only contains the steps that meet the condions necesary for moving
        next_moves = [p for p,f in zip(possible_steps, next_steps) if f == True]
    
        #Now that we have the possible moves it is important to consider if there is no possible move for the agent, in which it has to stay in its current position
        if len(next_moves) > 0:
            for move in next_moves:
                #If the current possible movement has a TrashAgent then it can move to that cell. Whith this condition it will always try to move to spaces where there is trash.
                if not self.model.grid.is_cell_empty(move):
                    if self.model.grid.get_cell_list_contents(move)[0].unique_id == "trash":
                        next_move = move
                    break
                else:
                    next_move = self.random.choice(next_moves)
        else:
            next_move = self.pos

        # Now move:
        if self.random.random() < 0.1:
            self.model.grid.move_agent(self, next_move)
            self.steps_taken+=1
            #If the cell that it founds contains a trash it is reomoved and we add a trash cleaned by that agent.
            if self.model.grid.get_cell_list_contents(next_move)[0].unique_id== "trash":
                self.model.grid.remove_agent(self.model.grid.get_cell_list_contents(next_move)[0])
                self.trash_taken += 1
                


    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        # self.direction = self.random.randint(0,8)
        # print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()

class TrashAgent(Agent):
    """
    Trash agent. Must be eliminated when interaction with Random Agent.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

class ObstacleAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  
