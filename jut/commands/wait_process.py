import click
from jut.registry import register_command


@register_command()
@click.argument("command")
def exec_after(
    command,
):
    pass
