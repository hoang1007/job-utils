from jut.registry import register_command


@register_command(name="greet")
def greet():
    print("Hello, world!")
