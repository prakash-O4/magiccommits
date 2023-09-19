
import click

from magiccommits.src.exception.error import KnownError


class CustomIntRange(click.ParamType):
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def convert(self, value, param, ctx):
        try:
            value = int(value)
            if self.min_value <= value <= self.max_value:
                return value
        except ValueError:
            pass
        raise KnownError()