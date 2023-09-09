import click
from magiccommits.src import config
from magiccommits.src.exception.error_handler import handleError
from magiccommits.src.exception.error import error
from magiccommits.src.utils import git

# @click.command()
# @click.option('--count',default=1, help='number of counters')
# @click.argument('name')
# def hello(count,name):
#     for x in range(count):
#         click.echo(f'Hello {name}')

@click.command()
@click.argument('mode',type=click.Choice(['get','set']))
@click.argument('key_value',nargs=-1)
@handleError
def cli(mode,key_value):
    """A command line tool for creating awesome commit messages."""
    #git.assert_git_repo()
    if(mode == 'get'):
        config_value =  config.get_config(key_value)
        click.echo(config_value)
    elif(mode == 'set'):
        value = []
        for kv in key_value:
            splitted_text = str(kv).strip().split("=")
            if(len(splitted_text) > 1):
                value.append((splitted_text[0],splitted_text[1]))
                config.set_configs(value)
                click.echo(f"values are {value}")
            else:
                error("Invalid format")
    else:
        click.echo("Invalid mode: Please use get or set")        

