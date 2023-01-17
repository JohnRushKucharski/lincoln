import json
import configparser
from pathlib import Path
from typing import List, Dict, NamedTuple, Any

from lincoln import DB_WRITE_ERROR, DB_READ_ERROR, JSON_ERROR, SUCCESS

# TODO: #1 need to make a directory for each game by name, this should be where config file is stored.
# DEFAULT_DB_FILE_PATH = Path.home().joinpath('db.json')

def get_db_path(config_file: Path) -> Path:
    '''Return current path to database.'''
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser['General']['database'])

def init_database(db_path: Path) -> int:
    '''Create database.'''
    try:
        db_path.write_text('[]') # empty file.
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
    
class DB(NamedTuple):
    data: List[Dict[str,Any]]
    error: int

class DBHandler:
    '''DB transaction manager.'''
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_db(self) -> DB:
        try:
            # 'r' is open to read
            with self._db_path.open('r') as db:
                try:
                    return DB(json.load(db), SUCCESS)
                # catches wrong json format
                except json.JSONDecodeError:
                    return DB([], JSON_ERROR)
        # catches IO errors
        except OSError:
            return DB([], DB_READ_ERROR)
    
    def write_db(self, entries: List[Dict[str, Any]]) -> DB:
        try:
            with self._db_path.open('w') as db:
                # indent just for readability
                # need to check how this appends.
                json.dump(entries, db, indent=4)
            return DB
        except:
            pass
    
    