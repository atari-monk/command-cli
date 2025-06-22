from argparse import Namespace
from src.storage import load_commands


def export_markdown(args: Namespace) -> None:
    commands = load_commands()
    if not commands:
        print("Nothing to export.")
        return

    lines = ["# Saved Commands\n"]
    for cmd in commands:
        lines.append(f"## `{cmd.command}`")
        lines.append(f"- **Description**: {cmd.description}")
        lines.append(f"- **Tags**: {', '.join(cmd.tags) if cmd.tags else '-'}")
        lines.append(f"- **Created**: {cmd.created_at}")
        lines.append("")

    with open("commands.md", "w") as f:
        f.write("\n".join(lines))

    print("📝 Exported to `commands.md`.")