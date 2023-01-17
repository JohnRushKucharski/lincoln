'''
Provides config file functionality, using a toml configuration file.
'''

import shutil
import tomli, tomli_w
from pathlib import Path
from typing import Optional, Tuple

from lincoln import (DIR_ERROR, FILE_ERROR, TOML_ERROR, SUCCESS, __app_name__)

DEFAULT_DIRECTORY = str(Path.home().joinpath('lincoln'))
DEFAULT_SYSTEM_FILE = str(Path('lincoln/examples/lincoln.toml'))

def _new_app(directory: Path, configfile: Path) -> Tuple[int, Path]:
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        shutil.copy(str(configfile), str(directory.joinpath(configfile.name)))
        configfile = directory.joinpath(configfile.name) 
        if len([f for f in directory.glob('*.toml')]) != 1:
            return FILE_ERROR
    except OSError:
        return FILE_ERROR
    try:    
        with configfile.open('rb') as f:
            toml = tomli.load(f)
        toml['database'] = str(directory.joinpath('db.json'))
        with configfile.open('wb') as f:
            tomli_w.dump(toml, f)
    except tomli.TOMLDecodeError:
        return TOML_ERROR
    return SUCCESS

def _existing_app(directory: Path):
    if not directory.exists():
        return DIR_ERROR
    if len([f for f in directory.glob('*.toml')]) != 1:
        return FILE_ERROR         
    return SUCCESS
    
def init_app(directory: Path, configfile: Optional[Path] = None) -> int:
    '''Initialize application'''
    return _new_app(directory, configfile) if configfile is not None else _existing_app(directory)
            
# def init_app(directory: Path) -> int:   # returns codes
#     '''Initialize the application.'''
#     config_path = directory.joinpath('config.ini')
#     config_code = _init_config_file(directory, config_path) # function defined below.
#     if config_code != SUCCESS:
#         return config_code
#     db_path = directory.joinpath('db.json')
#     db_code = _create_db(config_path, db_path)                           # function defined below.
#     if db_code != SUCCESS:
#         return db_code
#     return SUCCESS 

# def _init_config_file(directory: Path, file: Path) -> int:
#     try:
#         directory.mkdir(exist_ok=True)
#         #CONFIG_DIR_PATH.mkdir(exist_ok=True)
#     except OSError:
#         return DIR_ERROR
#     try:
#         file.touch(exist_ok=True)
#         #CONFIG_FILE_PATH.touch(exist_ok=True)
#     except OSError:
#         return FILE_ERROR
#     return SUCCESS

# def _create_db(config_path: Path, db_path: Path) -> int:
#     config_parser = configparser.ConfigParser()
#     config_parser['General'] = {'database': str(db_path)}
#     try:
#         # 'w' is open to write
#         with config_path.open('w') as file:
#             config_parser.write(file)
#     except OSError:
#         return DB_WRITE_ERROR
#     return SUCCESS
          
