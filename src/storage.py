import json
from pathlib import Path
from typing import List
from src.model import Command

DB_PATH = Path("commands.json")

def load_commands() -> List[Command]:
    if not DB_PATH.exists():
        return []
    with open(DB_PATH, "r") as f:
        data = json.load(f)
        return [Command(**item) for item in data]

def save_commands(commands: List[Command]) -> None:
    with open(DB_PATH, "w") as f:
        json.dump([command.__dict__ for command in commands], f, indent=2)
