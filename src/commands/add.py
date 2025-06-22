from src.model import Command
from src.storage import load_commands, save_commands
from argparse import Namespace


def add_command(args: Namespace) -> None:
    commands = load_commands()
    new_cmd = Command.create(args.command, args.description, args.tags.split(",") if args.tags else [])
    commands.append(new_cmd)
    save_commands(commands)
    print("✅ Command added.")