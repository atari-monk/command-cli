import argparse
from src.commands.add import add_command
from src.commands.list import list_commands


def main():
    parser = argparse.ArgumentParser(description="Command Saver CLI Tool")
    subparsers = parser.add_subparsers()

    # Add
    p_add = subparsers.add_parser("add", help="Add a new command")
    p_add.add_argument("command", help="The command string")
    p_add.add_argument("description", help="Description of the command")
    p_add.add_argument("--tags", help="Comma-separated tags", default="")
    p_add.set_defaults(func=add_command)

    # List
    p_list = subparsers.add_parser("list", help="List all saved commands")
    p_list.set_defaults(func=list_commands)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()