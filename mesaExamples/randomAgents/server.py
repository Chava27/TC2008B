from model import RandomModel, ObstacleAgent, TrashAgent
from random import randint

from mesa.visualization.modules import CanvasGrid, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    if (isinstance(agent, TrashAgent)):
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.1

    return portrayal

model_params = {"N":3, "width":10, "height":10}
#Define the percentage
model_params["P"]= 50
#number of steps before ending
model_params["max_time"] = 100

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

bar_chart_s = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps",canvas_height=200,
        canvas_width=400)

bar_chart_t = BarChartModule(
    [{"Label":"Trash", "Color":"#72755E"}],
    scope="agent", sorting="ascending", sort_by="Trash",canvas_height=200,
        canvas_width=400)



server = ModularServer(RandomModel, [grid, bar_chart_s, bar_chart_t], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()