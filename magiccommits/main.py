import click
from magiccommits.src.commands.config import config
from magiccommits.src.commands.mc import mc

#local import
from magiccommits.src.exception.error_handler import handleError
@click.group(invoke_without_command=True)
@click.option('-t','--ticket',help='Set the ticket number')
@click.option('-a','--add',is_flag=True, flag_value=True,help='Perform [git add .] operation')
@click.option('-u','--update',is_flag=True, flag_value=True,help='Perform [git add --update] operation')
@click.version_option(message="Magiccommit v0.5-dev" ,help='Current version of magiccommit')
@click.pass_context
@handleError
def cli(ctx,ticket,add,update):
    """This is the main command group."""
    mc(ctx=ctx,ticket=ticket,add=add,update=update)


cli.add_command(config)