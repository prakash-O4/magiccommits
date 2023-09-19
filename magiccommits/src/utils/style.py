import click
import pyperclip
from magiccommits.src.exception.error import KnownError
from magiccommits.src.utils.custom.confirmation_input import get_confirmation

from magiccommits.src.utils.custom.input_validator import CustomIntRange
from magiccommits.src.utils.git import add_commit_message


def format_response(response_dict):
    for key, value in response_dict.items():
        formatted_key = click.style(key, fg='green', bold=True)
        formatted_value = click.style(str(value), fg='blue')
        click.echo(f"{formatted_key}: {formatted_value}")

def multiple_answers(commit_message, ticket, copy_commit):
    messages = commit_message
    click.echo(click.style("\nList of messages:", fg='cyan', bold=True))
    
    if ticket is not None:
        messages = [str(ticket) + ' ' + message for message in messages]

    for i, message in enumerate(messages, start=1):
        click.echo(click.style(f"{i}. {message}", fg='blue'))

    while True:
        try:
            selection = click.prompt(
                "\nSelect a message (enter the number)",
                type=CustomIntRange(1, len(messages)),
                err=True,
            )
            vals = get_confirmation()
            if vals:
                selected_message = messages[selection - 1]
                is_committed = add_commit_message(selected_message)
                if is_committed:
                    click.secho("✔ Successfully Committed", fg='green')
                else:
                    click.secho("Could not commit the message", fg='red')
            else:
                if copy_commit:
                    pyperclip.copy(messages[selection - 1])
                    click.secho("Message copied to clipboard", fg='green')
                else:
                    click.secho("Set copy_commit to True to copy the commit", fg='yellow')
            break
        except KnownError:
            click.secho("\nInvalid input. Please enter a valid number from the list.", fg='red')
        except Exception as e:
            click.secho(f"\nexit code 1", fg='red', nl=True)
            break