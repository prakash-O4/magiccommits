import click


def get_confirmation():
    while True:
        confirmation = click.prompt(
            "Do you want to commit this message into your repo? (yes/no)",
            default="no",
            show_default=False,
        ).lower()

        if confirmation in ("yes", "y"):
            return True
        elif confirmation in ("no", "n"):
            return False
        else:
            click.echo("Invalid input. Please enter 'yes/y' or 'no/n'.")