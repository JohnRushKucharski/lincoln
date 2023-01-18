'''
Command Line Interface (CLI) for lincoln dam or watershed game.
'''
import typer
from rich import print

from pathlib import Path
# typer uses type hints
from typing import Optional

from lincoln import __app_name__, __version__
from lincoln.controller import config, model_control

app = typer.Typer()

def setup(directory: Path, tomlfile: Path = None):
    data = config.init_app(directory, tomlfile)
    return model_control.load_system(data)

@app.command()
def new(directory_location: str = typer.Option(config.DEFAULT_DIRECTORY, '--directory', '-d', help='Target location of game directory.'),
        inputfile_location: str = typer.Option(config.DEFAULT_SYSTEM_FILE, '--input', '-i', help='Game configuration file.')) -> None:
    '''Setup new game.'''
    system = setup(Path(directory_location), Path(inputfile_location))
    print(system)  
    
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