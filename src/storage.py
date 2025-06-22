from datetime import datetime
import json
from pathlib import Path
from typing import List
from src.model import Command

DB_PATH = Path(r"C:\atari-monk\code\command-cli\src\commands.json")

def load_commands() -> List[Command]:
    if not DB_PATH.exists():
        return []
    with open(DB_PATH, "r") as f:
        data = json.load(f)
        return [Command(**item) for item in data]

def save_commands(commands: List[Command]) -> None:
    backup_commands()
    with open(DB_PATH, "w") as f:
        json.dump([command.__dict__ for command in commands], f, indent=2)

def backup_commands():
    if not DB_PATH.exists():
        return
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = DB_PATH.with_name(f"commands_backup_{timestamp}.json")
    with open(DB_PATH, "r") as original, open(backup_path, "w") as backup:
        backup.write(original.read())