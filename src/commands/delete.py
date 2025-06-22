from argparse import Namespace
from src.storage import backup_commands, load_commands, save_commands


def delete_command(args: Namespace) -> None:
    commands = load_commands()
    new_commands = [cmd for cmd in commands if not cmd.id.startswith(args.id)]
    if len(new_commands) == len(commands):
        print(f"No command found with ID starting with '{args.id}'")
        return
    backup_commands()
    save_commands(new_commands)
    print("🗑️ Command deleted.")