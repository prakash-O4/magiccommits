import click

from magiccommits.src.exception.error import KnownError


def handleError(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KnownError as e:
            click.echo(click.style(f'❌ {e}', fg='red'))
    return wrapper
