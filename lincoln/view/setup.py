'''
Command Line Interface (CLI) for lincoln dam or watershed game.
'''

import typer
import tomli
import tomli_w

from pathlib import Path
# typer uses type hints
from typing import Optional, List, Tuple

from lincoln import __app_name__, __version__, ERRORS
from lincoln.controller import config, model_control

app = typer.Typer()

def setup(directory: Path, tomlfile: Path = None):
    init_error = config.init_app(directory, tomlfile)
    # int = 0 is false
    if init_error:
        typer.secho(f'Creating config file failed with "{ERRORS[init_error]}"',
                    fg=typer.colors.RED)
        raise typer.Exit(init_error)
    else:
        if tomlfile is not None:
            typer.secho(f'New game directory created at: {str(directory)}',
                        fg=typer.colors.GREEN)
        else:
            typer.secho(f'Game directory and configuration file found at: {directory}.',
                        fg=typer.colors.GREEN)

def load(directory: Path):
    load_error = model_control.load(directory)
    typer.Exit(1)

# def _setup_config_file(location: Path) -> None:
#     app_init_error = config.init_app(location)
#     if app_init_error:
#         typer.secho(f'Creating config file failed with "{ERRORS[app_init_error]}"',
#                     fg=typer.colors.RED)
#         raise typer.Exit(1)

# def _setup_empty_database(location: Path) -> None:
#     db_path = location.joinpath('db.json')
#     db_init_error = database.init_database(db_path)
#     if db_init_error:
#         typer.secho(f'Creating database failed with "{ERRORS[db_init_error]}"',
#                     fg=typer.colors.RED)
#         raise typer.Exit(1)
#     else:
#         typer.secho(f'Empty game database created in game directory at: {db_path}',
#                     fg=typer.colors.GREEN)

# def _read_file(filepath: Path) -> None:
#     # 'rb' is open to read as binary file
#     with filepath.open('rb') as f:
#         toml_dict1 = tomli.load(f)
#     toml_dict1['database'] = 'its here'
#     with filepath.open('wb') as f:
#         tomli_w.dump(toml_dict1, f)
        
#     with filepath.open('rb') as f:
#         toml_dict2 = tomli.load(f)
#     print(toml_dict2)
#         # try: 
#         #     toml_dict = tomli.load(f)
#         #     print(toml_dict)
#         # except tomli.TOMLDecodeError:
#         #     print(f'File: {str(filepath)} contains invalid TOML.')

@app.command()
def new(directory_location: str = typer.Option(config.DEFAULT_DIRECTORY, '--directory', '-d', help='Target location of game directory.'),
        inputfile_location: str = typer.Option(config.DEFAULT_SYSTEM_FILE, '--input', '-i', help='Game configuration file.')) -> None:
    '''Setup new game.'''
    directory = Path(directory_location)
    setup(directory, Path(inputfile_location))
    load(directory)
    
@app.command()
def existing(directory_location: str = typer.Argument(..., help='Location of existing game directory, containing *.toml, and *.json files.')) -> None:
    '''Load existing game.'''
    setup(Path(directory_location))

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f'{__app_name__} v{__version__}') # typer equivalent of print()
        raise typer.Exit() # exits application "cleanly", typer.Exit() default is 0: "SUCCESS".

@app.callback()
def main(version: Optional[bool] = typer.Option(None, "--version", "-v", help='Show application version and exit.', callback=_version_callback, is_eager=True))-> None:
    # 'is_eager' tells typer that the version option has precendence over other commands.
    return