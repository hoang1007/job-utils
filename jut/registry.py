from typing import Dict, Optional
import os
import importlib
import pkgutil
import click

# Create a register for group
class GroupRegistry:
    DEFAULT_KEY = "__default__"
    def __init__(self):
        self.store: Dict[str, click.Group] = {}

    def register(self, group: click.Group, name: Optional[str] = None, default: bool = False):
        name = name or group.name
        self.store[name] = group
        if default:
            self.store[self.DEFAULT_KEY] = group

    def get(self, name: str):
        return self.store.get(name)
    
    def get_default(self):
        return self.store.get(self.DEFAULT_KEY)
    
class CommandRegistry:
    def __init__(self):
        self.commands: Dict[str, click.Command] = {}
        self.groups: Dict[str, str] = {}

    def register(self, command: click.Command, name: Optional[str] = None, group: str = None):
        name = name or command.name
        self.commands[name] = command
        self.groups[name] = group

    def get(self, name: str):
        return self.commands.get(name)
    
    def get_group(self, name: str):
        return self.groups.get(name)


_GROUP_REGISTRY = GroupRegistry()
_COMMAND_REGISTRY = CommandRegistry()

def register_group(name: str = None, default: bool = False):
    def decorator(func):
        gr = click.group(name=name)(func)
        _GROUP_REGISTRY.register(gr, name=name, default=default)
        return gr

    return decorator

def register_command(name: str = None, group: str = None):
    def decorator(func):
        cmd = click.command(name=name)(func)
        _COMMAND_REGISTRY.register(cmd, name=name, group=group)
        print(_COMMAND_REGISTRY.commands)
        return cmd

    return decorator


def load_commands():
    # Get the directory of the current file
    commands_dir = os.path.join(os.path.dirname(__file__), 'commands')

    # Discover and import all modules in the commands directory
    for _, module_name, _ in pkgutil.iter_modules([commands_dir]):
        importlib.import_module(f'jut.commands.{module_name}')

def init_registry():
    load_commands()
    for name, command in _COMMAND_REGISTRY.commands.items():
        cmd_group_name = _COMMAND_REGISTRY.get_group(name)
        if cmd_group_name is not None:
            group = _GROUP_REGISTRY.get(cmd_group_name)
            assert group is not None, f"Group {cmd_group_name} not found"
        else:
            group = _GROUP_REGISTRY.get_default()
            assert group is not None, "Please provide a default group"
        group.add_command(command)
