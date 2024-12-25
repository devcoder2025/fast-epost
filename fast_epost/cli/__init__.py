import click
from typing import Optional

@click.group()
def cli():
    """Fast-Epost CLI tool for development operations"""
    pass

@cli.command()
@click.option('--port', default=5000)
def dev(port: int):
    """Run development server with hot reload"""
    server = DevServer('app.py', port)
    server.start()
    
@cli.command()
def test():
    """Run test suite"""
    click.echo("Running tests...")
