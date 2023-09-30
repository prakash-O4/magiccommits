import click
from magiccommits.src.exception.error import KnownError, NetworkError


def handleError(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KnownError as e:
            click.secho(click.style(f'❌ {e}', fg='red'))
            click.get_current_context().exit(code=1)
        except NetworkError as e:
            click.secho(e.error.get('message'),fg='red')
            click.get_current_context().exit(code=1)
        except KeyboardInterrupt as e:
            click.secho("Exit code 1",fg='red')
            click.get_current_context().exit(code=1)
        except Exception as e:
            click.secho("Oops, we got an untracked error, Please report it to https://github.com/prakash-O4/magiccommits/issues.",fg='red')
            click.get_current_context().exit(code=1)
    return wrapper
