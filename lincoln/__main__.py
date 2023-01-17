'''
Entry point for game.
'''
import typer

from lincoln import __app_name__
from lincoln.view import setup

def main():
    # initialize typer app
    setup.app(prog_name=__app_name__)
    
if __name__ == "__main__":
    main()