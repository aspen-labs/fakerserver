"""Command-line interface for the fake data API server."""

import click
from .server import start_server


@click.command()
@click.option(
    '-H', '--host',
    default='0.0.0.0',
    help='Host address to bind to',
    show_default=True
)
@click.option(
    '-p', '--port',
    type=int,
    default=8000,
    help='Port number to listen on',
    show_default=True
)
@click.option(
    '-v', '--verbose',
    is_flag=True,
    help='Enable verbose logging'
)
def main(host, port, verbose):
    """Start a multithreaded fake data generation API server."""
    start_server(host, port, verbose)


if __name__ == '__main__':
    main()
