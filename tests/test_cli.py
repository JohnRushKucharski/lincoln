'''
Tests typer lincoln game CLI
'''

from typer.testing import CliRunner

from lincoln import __app_name__, __version__
from lincoln.view import cli

runner = CliRunner() # typer testing utility

def test_version():
    result = runner.invoke(cli.app, ['--version'])
    assert result.exit_code == 0 # exits a SUCCESS (i think)
    assert f'{__app_name__} v{__version__}\n' in result.stdout # prints expected output (using echo)