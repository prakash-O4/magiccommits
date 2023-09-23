import click


def get_confirmation():
    while True:
        confirmation = click.prompt(
            "Enter [c/C] to commit or [cp/CP] to commit and push or [n/N] to cancel: ",
            default="n",
            show_default=False,
        ).lower()

        if confirmation.lower() == "c":
            return "c"
        elif confirmation.lower() == "cp":
            return "cp"
        elif confirmation.lower() == 'n':
            return "n"
        else:
            click.secho("\nInvalid input. Please enter [c/C] or [cp/CP] or [n/N].\n", fg='red')