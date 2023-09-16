import click
from magiccommits.src.utils.custom.confirmation_input import get_confirmation

from magiccommits.src.utils.custom.input_validator import CustomIntRange
from magiccommits.src.config import set_configs, get_config
from magiccommits.src.utils.git import get_staged_diff

@click.group(invoke_without_command=True)
# @click.option('--f', default=False, type=bool)
@click.pass_context
def cli(ctx):
    """This is the main command group."""
    if(ctx.invoked_subcommand is None):
        # check if git is initialized or not
        diff =  get_staged_diff()
        click.echo(diff)
        #start loading with message 
        # get the git diff 
        # if not diff is found then display message and exit the termainal with exit code 0
        # if diff is found then get all the configs 
        
    else:
        pass

@cli.command('config', short_help='Configuration for magiccommit')
@click.argument('mode',type=click.Choice(['get','set']))
@click.argument('key_value',nargs=-1)
def config(mode,key_value):
    """Set your configuration value for the magic commit [Learn More]"""
    if(mode == 'get'):
        config_value =  get_config(key_value)
        click.echo(config_value)
    elif(mode == 'set'):
        value = []
        for kv in key_value:
            splitted_text = str(kv).strip().split("=")
            if(len(splitted_text) > 1):
                value.append((splitted_text[0],splitted_text[1]))
                set_configs(value)


# Default behavior when no subcommand is provided
# @cli.command('config',short_help='Configuration for magiccommit')
# def default_action():
#     """This is the default action."""
#     click.echo("Running the default action")


def multiple_answers():
    """List messages."""
    messages = ["message1", "message2", "message3"]
     # Create a list of tuples for click.Choice options
    choices = [(str(i + 1), message) for i, message in enumerate(messages)]

    click.echo("List of messages:")
    for i, message in enumerate(messages, start=1):
        click.echo(f"{i}. {message}")
    while True:

        try:
            # Prompt the user to select a message with arrow key navigation
            selection = click.prompt(
                "\nSelect a message (enter the number)",
                type=CustomIntRange(1, len(messages)),
                err=True,
                # confirmation_prompt= "Do you want to commit this message into your repo?"
            )
            vals  = get_confirmation()
            if(vals):
                click.echo("push it")
                selected_message = messages[selection - 1]
                click.echo(f"Selected message: {selected_message}")
            else:
                click.echo("copy and exit the terminal")
            break  # Exit the loop if valid input is provided
        except click.exceptions.BadParameter:
            click.echo("Invalid input. Please enter a valid number from the list.")
        except Exception as e:
            click.echo("Wrong!!!!!")

