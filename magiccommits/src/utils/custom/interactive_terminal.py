from typing import List
import click
import readchar


class DefaultKeys:
    """List of default keybindings.

    Attributes:
        interrupt(List[str]): Keys that cause a keyboard interrupt.
        select(List[str]): Keys that trigger list element selection.
        confirm(List[str]): Keys that trigger list confirmation.
        delete(List[str]): Keys that trigger character deletion.
        down(List[str]): Keys that select the element below.
        up(List[str]): Keys that select the element above.
    """

    interrupt: List[str] = [readchar.key.CTRL_C, readchar.key.CTRL_D]
    select: List[str] = [readchar.key.SPACE]
    confirm: List[str] = [readchar.key.ENTER]
    delete: List[str] = [readchar.key.BACKSPACE]
    down: List[str] = [readchar.key.DOWN, "j"]
    up: List[str] = [readchar.key.UP, "k"]


def select(
    options,
    caption_indices=None,
    deselected_prefix="[ ] ",
    selected_prefix="[x] ",
    caption_prefix="",
    selected_index=0,
    confirm_on_select=True,
):
    print("\n" * (len(options) - 1))
    if caption_indices is None:
        caption_indices = []
    while True:
        print(f"\033[{len(options) + 1}A")
        for i, option in enumerate(options):
            if i not in caption_indices:
                line = selected_prefix + option if i == selected_index else deselected_prefix + option
                click.secho(message=line,fg='green') if i == selected_index else click.secho(message=line)
            elif i in caption_indices:
                print(f"\033[K{caption_prefix}{options[i]}")
        keypress = readchar.readkey()
        if keypress in DefaultKeys.up:
            new_index = selected_index
            while new_index > 0:
                new_index -= 1
                if new_index not in caption_indices:
                    selected_index = new_index
                    break
        elif keypress in DefaultKeys.down:
            new_index = selected_index
            while new_index < len(options) - 1:
                new_index += 1
                if new_index not in caption_indices:
                    selected_index = new_index
                    break
        elif (
            keypress in DefaultKeys.confirm
            or confirm_on_select
            and keypress in DefaultKeys.select
        ):
            break
        elif keypress in DefaultKeys.interrupt:
            raise KeyboardInterrupt
        
    return selected_index