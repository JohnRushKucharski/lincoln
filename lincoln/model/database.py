import configparser
from pathlib import Path

from lincoln import DB_WRITE_ERROR, SUCCESS

# TODO: #1 need to make a directory for each game by name, this should be where config file is stored.
DEFAULT_DB_FILE_PATH = Path.home().joinpath('db.json')

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