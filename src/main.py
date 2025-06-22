import argparse
from src.commands.add import add_command
from src.commands.delete import delete_command
from src.commands.edit import edit_command
from src.commands.list import list_commands
from src.commands.read import read_command


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

    # Edit
    p_edit = subparsers.add_parser("edit", help="Edit an existing command")
    p_edit.add_argument("id", help="ID (or partial ID) of the command to edit")
    p_edit.add_argument("--command", help="New command string")
    p_edit.add_argument("--description", help="New description")
    p_edit.add_argument("--tags", help="New comma-separated tags (empty to clear)")
    p_edit.set_defaults(func=edit_command)

    # Read
    p_read = subparsers.add_parser("read", help="View details of a command by ID")
    p_read.add_argument("id", help="ID (or partial ID) of the command to view")
    p_read.set_defaults(func=read_command)

    # Delete
    p_delete = subparsers.add_parser("delete", help="Delete a command by ID")
    p_delete.add_argument("id", help="ID (or partial ID) of the command to delete")
    p_delete.set_defaults(func=delete_command)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()