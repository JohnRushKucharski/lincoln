'''
Manages the simulation of the system for the length of a game.
'''
from dataclasses import dataclass
from typing import List

from lincoln.model.system import System

@dataclass
class Game:
    system: System
    # configurations
    seasons: List[str]
    
# nodes: scoring (<, =, > etc rules with points), objectives (win criteria) / anti-objectives (e.g. dont loose criteria)
# objectives -> cummulative or by round
# modes -> number of rounds, first to objective, last to loose

# game state variable: while playing = True, where playing is updated by examining objectives / anti-objectives
# node ; objective /anti-objective object with state variable has_met_requirement
