'''
Command Line Interface (CLI) for lincoln dam or watershed game.
'''

import typer

from pathlib import Path
# typer uses type hints
from typing import Optional

from lincoln import __app_name__, __version__, ERRORS
from lincoln.model import config, database

app = typer.Typer()

@app.command()
def init(db_path: str = typer.Option(str(database.DEFAULT_DB_FILE_PATH), '--database', '-db', prompt='game database location?')) -> None:
    '''Initialize the database.'''
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(f'Creating config file failed with "{ERRORS[app_init_error]}"',
                    fg=typer.colors.RED)
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(f'Creating database failed with "{ERRORS[db_init_error]}"',
                    fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(f'The game database is at: {db_path}',
                    fg=typer.colors.GREEN)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f'{__app_name__} v{__version__}') # typer equivalent of print()
        raise typer.Exit() # exits application "cleanly", typer.Exit() default is 0: "SUCCESS".

@app.callback()
def main(version: Optional[bool] = typer.Option(None, "--version", "-v", help='Show application version and exit.', callback=_version_callback, is_eager=True))-> None:
    # 'is_eager' tells typer that the version option has precendence over other commands.
    return