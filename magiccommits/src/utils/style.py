import click
import pyperclip
from magiccommits.src.exception.error import KnownError
from magiccommits.src.utils.custom.confirmation_input import get_confirmation

from magiccommits.src.utils.custom.input_validator import CustomIntRange
from magiccommits.src.utils.custom.interactive_terminal import select
from magiccommits.src.utils.git import add_commit_message, push_to_origin


def format_response(response_dict):
    for key, value in response_dict.items():
        formatted_key = click.style(key, fg='green', bold=True)
        formatted_value = click.style(str(value), fg='blue')
        click.echo(f"{formatted_key}: {formatted_value}")

def multiple_answers(commit_message, ticket, copy_commit):
    messages = commit_message
    click.echo(click.style("\nList of messages:", fg='cyan', bold=True))
    
    try:
        if ticket is not None:
            messages = [str(ticket) + ' ' + message for message in messages]

        selected_index = select(messages)
        selected_message = messages[selected_index]
        click.echo(click.style("\nSelect given options:", fg='cyan', bold=True))

        confirmation_index = select(["Commit","Commit and Push","Cancel"])
        if confirmation_index == 0 or confirmation_index == 1:
            is_committed = add_commit_message(selected_message)
            if is_committed:
                if(confirmation_index == 1):
                    is_pushed = push_to_origin()
                    click.secho('push it to origin')
                if(confirmation_index == 0):
                    click.secho("✔ Successfully Committed", fg='green')
                elif (confirmation_index == 1 and is_pushed):
                    click.secho("✔ Successfully Committed and pushed to origin", fg='green')
                elif (not is_pushed):
                    click.secho("Message is committed, Could not pushed it to origin", fg='red')
            else:
                click.secho("Could not commit the message", fg='red')
        else:
            if copy_commit:
                pyperclip.copy(selected_message)
                click.secho("Message copied to clipboard", fg='green')
            else:
                click.secho("Set copy_commit to True to copy the commit", fg='yellow')
    except KeyboardInterrupt:
        click.secho("Exit code 1",fg='red')
    except Exception as e:
        raise e