from argparse import Namespace
from src.storage import load_commands


def read_command(args: Namespace) -> None:
    commands = load_commands()
    for cmd in commands:
        if cmd.id.startswith(args.id):
            print(f"🆔 ID: {cmd.id}")
            print(f"📅 Created: {cmd.created_at}")
            print(f"💻 Command: {cmd.command}")
            print(f"📝 Description: {cmd.description}")
            print(f"🏷️  Tags: {', '.join(cmd.tags) if cmd.tags else '-'}")
            return
    print(f"No command found with ID starting with '{args.id}'")