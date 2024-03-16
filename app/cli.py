import click
from .utils import clone_repo, get_repo_name

def register_cli(app):
    @app.cli.command()
    def clone():
        # Your code here
        click.echo('Cloning repo')

    # Add more commands as needed
