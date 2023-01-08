'''
Entry point for game.
'''

from lincoln import __app_name__
from lincoln.view import cli

def main():
    # initialize typer app
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()