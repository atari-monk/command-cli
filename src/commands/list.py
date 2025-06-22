from src.storage import load_commands
from argparse import Namespace


def list_commands(args: Namespace) -> None:
    commands = load_commands()
    if not commands:
        print("No commands saved yet.")
        return
    for cmd in commands:
        tags = ", ".join(cmd.tags) if cmd.tags else "-"
        print(f"{cmd.id[:8]} | {cmd.command} - {cmd.description} ({tags})")
