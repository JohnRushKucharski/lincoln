'''Manipulates model.'''
import tomli
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any

from lincoln import SUCCESS, FILE_ERROR, TOML_ERROR
from lincoln.model import system, node
#import ..model.system

# load game -> load_config.
# play game -> play_round.
# tear down.

@dataclass
class Game:
    directory: Path
    configfile: Path
    dbfile: Path
    system: system.System
    
    def play(self):
        # maybe calls play round.
        pass

def load(directory: Path) -> int:
    configs = [f for f in directory.glob('*.toml')]
    error, data = load_config(configs[0])
    error, system = load_system(data)
    if len(configs) != 1:
        return FILE_ERROR
    else:
        print(system)    
    return error

def load_system(data = Dict[str, Any]):
    return 0, system.factory(data)
    
    
def load_config(config: Path) -> Tuple[int, Dict[str, Any]]:
    # this does not report back the view it is run by a command like run game which holds the game while its needed, which returns errors and prints or querries users.
    try:
        with config.open('rb') as f:
            data = tomli.load(f)
        return SUCCESS, data
    except tomli.TOMLDecodeError:
        return TOML_ERROR, {}
    
   
        