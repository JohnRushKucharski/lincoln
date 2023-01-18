'''
Provides config file functionality, using a toml configuration file.
'''

import shutil
import tomli
from pathlib import Path
from typing import Optional, Dict, Any

from lincoln.utilities import exception_handler
from lincoln import __app_name__

DEFAULT_DIRECTORY = str(Path.home().joinpath('lincoln'))
DEFAULT_SYSTEM_FILE = str(Path('lincoln/examples/lincoln.toml'))

class ConfigurationError(Exception):
    pass

def init_app(directory: Path, configfile: Optional[Path] = None) -> int:
    '''Initialize application'''
    return configure_new_app(directory, configfile) if configfile is not None else configure_existing_app(directory)

def configure_new_app(directory: Path, config_file: Path) -> Dict[str, Any]:
    configure_directory(directory, True)
    file = move_config_file(directory, config_file)
    return load_configuration_data(file)

def configure_existing_app(directory: Path) -> Dict[str, Any]:
    configure_directory(directory, False)
    file = find_config_file(directory)
    return load_configuration_data(file)

@exception_handler(ConfigurationError, 1)
def configure_directory(directory: Path, new: bool = True) -> None:
    if new:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError:
            raise ConfigurationError(f'A directory at: {str(directory)} could not be created or established.')
    else: # existing directory
        if not directory.exists():
            raise ConfigurationError(f'No directory exists at: {str(directory)}.')

@exception_handler(ConfigurationError, 2)
def move_config_file(directory: Path, config_file: Path) -> Path:
    try:
        shutil.copy(str(config_file), str(directory.joinpath(config_file.name)))
    except OSError:
        raise ConfigurationError(f'The configuration file could not be moved from: {str(config_file)} to {str(directory.joinpath(config_file.name))}.')
    return find_config_file(directory)
        
@exception_handler(ConfigurationError, 2)
def find_config_file(directory: Path) -> Path:
    configs = [f for f in directory.glob('*.toml')]
    if len(configs) != 1:
        raise ConfigurationError(f'More than one .toml configuration file was found at: {str(directory)}.')
    return configs[0]

@exception_handler(ConfigurationError, 3) 
def load_configuration_data(config_file: Path) -> Dict[str, Any]:
    try:           
        with config_file.open('rb') as f:
            data = tomli.load(f)
        return data
    except tomli.TOMLDecodeError:
        raise ConfigurationError(f'The {str(config_file)} configuration file, could not be decoded by the toml file reader.')
          
