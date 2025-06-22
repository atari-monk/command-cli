from typing import List
from argparse import Namespace
from thefuzz import fuzz
from src.storage import load_commands

def search_commands(args: Namespace) -> None:
    commands = load_commands()
    found = False
    for cmd in commands:
        desc: str = str(cmd.description)
        tags_list: List[str] = list(cmd.tags) if hasattr(cmd, "tags") else []
        query_str: str = str(args.query).lower()
        desc_score = fuzz.partial_ratio(query_str, desc.lower()) # type: ignore
        tags_score = fuzz.partial_ratio(query_str, " ".join(tags_list).lower()) # type: ignore
        if desc_score > 70 or tags_score > 70:
            tags = ", ".join(tags_list) if tags_list else "-"
            print(f"{cmd.id[:8]} | {cmd.command} - {desc} ({tags})")
            found = True
    if not found:
        print("No matching commands found.")
