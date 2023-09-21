import click
import pyperclip
from magiccommits.src.exception.error import KnownError
from magiccommits.src.utils.custom.confirmation_input import get_confirmation

from magiccommits.src.utils.custom.input_validator import CustomIntRange
from magiccommits.src.utils.git import add_commit_message, push_to_origin


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
            if vals == 'c' or vals == 'cp':
                selected_message = messages[selection - 1]
                is_committed = add_commit_message(selected_message)
                if is_committed:
                    if(vals == 'cp'):
                        is_pushed = push_to_origin()
                        click.secho('push it to origin')
                    if(vals == 'c'):
                        click.secho("✔ Successfully Committed", fg='green')
                    elif (vals == 'cp' and is_pushed):
                        click.secho("✔ Successfully Committed and pushed to origin", fg='green')
                    elif (not is_pushed):
                        click.secho("Message is committed, Could not pushed it to origin", fg='red')
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