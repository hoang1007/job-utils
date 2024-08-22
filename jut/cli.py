from jut.registry import register_group, init_registry
# from jut.commands.hello_world import helloworld

@register_group(default=True)
def cli():
    pass

def main():
    init_registry()
    cli()
