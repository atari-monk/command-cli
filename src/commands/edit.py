from src.storage import load_commands, save_commands
from argparse import Namespace


def edit_command(args: Namespace) -> None:
    commands = load_commands()
    updated = False

    for cmd in commands:
        if cmd.id.startswith(args.id):
            if args.command:
                cmd.command = args.command
            if args.description:
                cmd.description = args.description
            if args.tags is not None:
                cmd.tags = args.tags.split(",") if args.tags else []

            updated = True
            break

    if updated:
        save_commands(commands)
        print("✏️ Command updated.")
    else:
        print(f"No command found with ID starting with '{args.id}'")
