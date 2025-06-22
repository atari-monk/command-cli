# Design Document 

## Index

- [Init](#init)
- [One File](#one-file)
- [Edit](#edit)
- [Read](#read)
- [Pause](#pause)
- [Delete](#delete)
- [Export](#export)
- [Sum](#sum)
- [Tree](#tree)

## Init 

[Top](#design-document)

Listen, I want to get 25 minutes with coding, but I am thinking about what kind of project I do. Maybe some app, but for example, to store commands in some data storage, let's do some model first.And the fastest way to code this app would be to create a model first, and then some CLI app with basic storage in the file, I think. This is the fastest way to get moving. And when it will be used, then we will expand for API and some shit.

Got it — you're aiming for a quick 25-minute sprint to build something small but useful, with the potential to grow later. Here's a lean plan based on your idea:

---

### 🧠 **App Idea: Command Saver (CLI tool)**

A simple CLI tool that lets you store, view, and search frequently used terminal commands with a description. Later, you can expand this into an API, web UI, or even a VSCode extension.

---

### ⚙️ MVP Scope (25-minute version)

* **Model**: Each command has:

* `id`: unique identifier (e.g. UUID or incrementing)
* `command`: the shell command string
* `description`: short description
* `tags`: list of tags (optional)
* `created_at`: timestamp

* **Storage**: JSON file on disk (super simple)

* **CLI commands**:

* `add`: Add a new command
* `list`: Show all commands
* `search`: Search by keyword in description or tags

---

### 🧱 1. Data Model (`models.py` or inline)

```python
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid

@dataclass
class Command:
id: str
command: str
description: str
tags: list[str]
created_at: str

@staticmethod
def create(command, description, tags):
return Command(
id=str(uuid.uuid4()),
command=command,
description=description,
tags=tags,
created_at=datetime.utcnow().isoformat()
)
```

---

### 🧪 2. Basic Storage (`storage.py` or inline)

```python
import json
from pathlib import Path

DB_PATH = Path("commands.json")

def load_commands():
if not DB_PATH.exists():
return []
with open(DB_PATH, "r") as f:
return json.load(f)

def save_commands(commands):
with open(DB_PATH, "w") as f:
json.dump(commands, f, indent=2)
```

---

### 🧰 3. CLI Interface (`main.py`)

```python
import argparse
from models import Command
from storage import load_commands, save_commands

def add(args):
commands = load_commands()
new_cmd = Command.create(args.command, args.description, args.tags.split(",") if args.tags else [])
commands.append(asdict(new_cmd))
save_commands(commands)
print("✅ Command added.")

def list_cmds(args):
commands = load_commands()
for cmd in commands:
print(f"{cmd['id'][:8]} | {cmd['command']} - {cmd['description']} ({', '.join(cmd['tags'])})")

def search(args):
commands = load_commands()
for cmd in commands:
if args.query in cmd["description"] or args.query in " ".join(cmd["tags"]):
print(f"{cmd['id'][:8]} | {cmd['command']} - {cmd['description']}")

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# Add
parser_add = subparsers.add_parser("add")
parser_add.add_argument("command")
parser_add.add_argument("description")
parser_add.add_argument("--tags", default="")
parser_add.set_defaults(func=add)

# List
parser_list = subparsers.add_parser("list")
parser_list.set_defaults(func=list_cmds)

# Search
parser_search = subparsers.add_parser("search")
parser_search.add_argument("query")
parser_search.set_defaults(func=search)

args = parser.parse_args()
args.func(args)
```

---

### ✅ Run Examples

```bash
python main.py add "git status" "Check git status" --tags git
python main.py list
python main.py search git
```

---

### 🔮 Next Steps (for later)

* Add editing/removing commands
* Export to Markdown
* Build a small REST API (Flask/FastAPI)
* Add fuzzy search
* Build TUI with `Textual` or `curses`

---

Want me to pack this into a single file version for ultra-fast start?

## One File

[Top](#design-document)

OK, put it in my file, put it in my one file for fast start.

Perfect — here’s the **one-file version** of your Command Saver CLI app.

Just copy-paste this into a file called `cmd_saver.py`, and you're ready to go:

```python
import argparse
import json
import uuid
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

# ---------- Model ----------
@dataclass
class Command:
id: str
command: str
description: str
tags: list[str]
created_at: str

@staticmethod
def create(command, description, tags):
return Command(
id=str(uuid.uuid4()),
command=command,
description=description,
tags=tags,
created_at=datetime.utcnow().isoformat()
)

# ---------- Storage ----------
DB_PATH = Path("commands.json")

def load_commands():
if not DB_PATH.exists():
return []
with open(DB_PATH, "r") as f:
return json.load(f)

def save_commands(commands):
with open(DB_PATH, "w") as f:
json.dump(commands, f, indent=2)

# ---------- CLI Actions ----------
def add_command(args):
commands = load_commands()
new_cmd = Command.create(args.command, args.description, args.tags.split(",") if args.tags else [])
commands.append(asdict(new_cmd))
save_commands(commands)
print("✅ Command added.")

def list_commands(args):
commands = load_commands()
if not commands:
print("No commands saved yet.")
return
for cmd in commands:
tags = ", ".join(cmd["tags"]) if cmd["tags"] else "-"
print(f"{cmd['id'][:8]} | {cmd['command']} - {cmd['description']} ({tags})")

def search_commands(args):
commands = load_commands()
found = False
for cmd in commands:
if args.query.lower() in cmd["description"].lower() or args.query.lower() in " ".join(cmd["tags"]).lower():
tags = ", ".join(cmd["tags"]) if cmd["tags"] else "-"
print(f"{cmd['id'][:8]} | {cmd['command']} - {cmd['description']} ({tags})")
found = True
if not found:
print("No matching commands found.")

# ---------- CLI Setup ----------
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

# Search
p_search = subparsers.add_parser("search", help="Search commands by keyword")
p_search.add_argument("query", help="Search keyword")
p_search.set_defaults(func=search_commands)

args = parser.parse_args()
if hasattr(args, "func"):
args.func(args)
else:
parser.print_help()

if __name__ == "__main__":
main()
```

---

### ✅ Quick Start

Run in terminal:

```bash
python cmd_saver.py add "git log --oneline" "Compact git log" --tags git,log
python cmd_saver.py list
python cmd_saver.py search log
```

---

Let me know if you want it to auto-create the JSON file, support editing, or auto-backup on write.

## Edit

[Top](#design-document)

OK, these next steps you mentioned, implement one of them now.

Nice — let's build on the momentum.

Let’s implement this next step:

### 🔄 **Command Editing**

You'll be able to edit a saved command by its ID.

---

### ✅ What's Changing:

* New subcommand: `edit`
* You can update:

* the command string
* the description
* the tags
* It won't overwrite fields you don’t update (non-destructive)

---

Here's the **updated one-file version** with `edit` included (replaces your current file):

```python
import argparse
import json
import uuid
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

# ---------- Model ----------
@dataclass
class Command:
id: str
command: str
description: str
tags: list[str]
created_at: str

@staticmethod
def create(command, description, tags):
return Command(
id=str(uuid.uuid4()),
command=command,
description=description,
tags=tags,
created_at=datetime.utcnow().isoformat()
)

# ---------- Storage ----------
DB_PATH = Path("commands.json")

def load_commands():
if not DB_PATH.exists():
return []
with open(DB_PATH, "r") as f:
return json.load(f)

def save_commands(commands):
with open(DB_PATH, "w") as f:
json.dump(commands, f, indent=2)

# ---------- CLI Actions ----------
def add_command(args):
commands = load_commands()
new_cmd = Command.create(args.command, args.description, args.tags.split(",") if args.tags else [])
commands.append(asdict(new_cmd))
save_commands(commands)
print("✅ Command added.")

def list_commands(args):
commands = load_commands()
if not commands:
print("No commands saved yet.")
return
for cmd in commands:
tags = ", ".join(cmd["tags"]) if cmd["tags"] else "-"
print(f"{cmd['id'][:8]} | {cmd['command']} - {cmd['description']} ({tags})")

def search_commands(args):
commands = load_commands()
found = False
for cmd in commands:
if args.query.lower() in cmd["description"].lower() or args.query.lower() in " ".join(cmd["tags"]).lower():
tags = ", ".join(cmd["tags"]) if cmd["tags"] else "-"
print(f"{cmd['id'][:8]} | {cmd['command']} - {cmd['description']} ({tags})")
found = True
if not found:
print("No matching commands found.")

def edit_command(args):
commands = load_commands()
updated = False
for cmd in commands:
if cmd["id"].startswith(args.id):
if args.command:
cmd["command"] = args.command
if args.description:
cmd["description"] = args.description
if args.tags is not None:
cmd["tags"] = args.tags.split(",") if args.tags else []
updated = True
break
if updated:
save_commands(commands)
print("✏️ Command updated.")
else:
print(f"No command found with ID starting with '{args.id}'")

# ---------- CLI Setup ----------
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

# Search
p_search = subparsers.add_parser("search", help="Search commands by keyword")
p_search.add_argument("query", help="Search keyword")
p_search.set_defaults(func=search_commands)

# Edit
p_edit = subparsers.add_parser("edit", help="Edit an existing command")
p_edit.add_argument("id", help="ID (or partial ID) of the command to edit")
p_edit.add_argument("--command", help="New command string")
p_edit.add_argument("--description", help="New description")
p_edit.add_argument("--tags", help="New comma-separated tags (empty to clear)")
p_edit.set_defaults(func=edit_command)

args = parser.parse_args()
if hasattr(args, "func"):
args.func(args)
else:
parser.print_help()

if __name__ == "__main__":
main()
```

---

### 🧪 How to Use the Edit Feature:

1. List commands:

```bash
python cmd_saver.py list
```

2. Pick the short ID (first few characters)

3. Edit the description:

```bash
python cmd_saver.py edit a1b2c3d4 --description "Updated description"
```

You can also update multiple things at once:

```bash
python cmd_saver.py edit a1b2c3d4 --command "new command" --tags linux,shell
```

---

Let me know if you want to **delete** commands next — or add backup/versioning.

## Read

[Top](#design-document)

Yeah, I want the right commands, the read commands.

Great — you're talking about a way to **view (read)** specific command entries in more detail, probably by ID. Let's add a `read` command to show full info for one saved command.

---

### ✅ Feature: `read` Command

You’ll be able to:

* View a single command entry by its ID (partial or full).
* See its command, description, tags, and creation date.

---

### 🔧 Add this to your existing one-file CLI

Here’s the **updated section** to add to your file (`cmd_saver.py`):

#### 🧩 1. Add this new function:

```python
def read_command(args):
commands = load_commands()
for cmd in commands:
if cmd["id"].startswith(args.id):
print(f"🆔 ID: {cmd['id']}")
print(f"📅 Created: {cmd['created_at']}")
print(f"💻 Command: {cmd['command']}")
print(f"📝 Description: {cmd['description']}")
print(f🏷️  Tags: {', '.join(cmd['tags']) if cmd['tags'] else '-'}")
return
print(f"No command found with ID starting with '{args.id}'")
```

#### 🧩 2. Add to the CLI setup:

In the `main()` function, add:

```python
# Read
p_read = subparsers.add_parser("read", help="View details of a command by ID")
p_read.add_argument("id", help="ID (or partial ID) of the command to view")
p_read.set_defaults(func=read_command)
```

---

### 📦 Now You Can Run:

```bash
python cmd_saver.py list
```

Copy the ID from any row, then:

```bash
python cmd_saver.py read a1b2c3d4
```

You'll get output like:

```
🆔 ID: a1b2c3d4-xxxx-xxxx-xxxx-xxxxxxxxxxxx
📅 Created: 2025-06-22T12:34:56
💻 Command: git push origin main
📝 Description: Push code to main branch
🏷️  Tags: git, push
```

---

Want the next step? I can add:

* `delete` command
* fuzzy matching for search
* export to Markdown
* backup before saving

Pick one and I’ll build it.

## Pause

[Top](#design-document)

Yeah, just not do the next topic.

You got it — we’ll pause here. You’ve now got:

* ✅ Add
* ✅ List
* ✅ Search
* ✅ Edit
* ✅ Read

All packed in one single-file CLI app — lean, fast, and expandable later.

If you ever want to:

* Turn this into an API
* Build a web or terminal UI
* Sync to cloud (or Git)
* Add encryption/protection

Just say the word and we’ll take the next step. 🚀

Let me know if you want help cleaning up, packaging, or running it anywhere.

## Delete

[Top](#design-document)

No, you misunderstood me. I said TWO next topics.

Ahh, got it now — thanks for clarifying! You want **two more features** added next. Let’s do that.

Here are **two solid next steps** to stack on what we already built:

---

### 🔥 Feature 1: `delete` Command

Let you delete a saved command by ID (full or partial).

### 🔥 Feature 2: Auto Backup Before Save

Each time you save (add/edit/delete), it creates a timestamped backup of `commands.json`.

---

### 🧠 Updates to Add in Your File (`cmd_saver.py`)

#### 🔧 1. `delete_command()` function:

```python
def delete_command(args):
commands = load_commands()
new_commands = [cmd for cmd in commands if not cmd["id"].startswith(args.id)]
if len(new_commands) == len(commands):
print(f"No command found with ID starting with '{args.id}'")
return
backup_commands()  # <-- backup before deleting
save_commands(new_commands)
print("🗑️ Command deleted.")
```

---

#### 🔧 2. `backup_commands()` function:

```python
def backup_commands():
if not DB_PATH.exists():
return
timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
backup_path = DB_PATH.with_name(f"commands_backup_{timestamp}.json")
with open(DB_PATH, "r") as original, open(backup_path, "w") as backup:
backup.write(original.read())
```

---

#### 🔧 3. Call backup inside `save_commands()`:

Update this function:

```python
def save_commands(commands):
backup_commands()  # <-- new line
with open(DB_PATH, "w") as f:
json.dump(commands, f, indent=2)
```

Now every save creates a backup like:

```
commands_backup_20250622143010.json
```

---

#### 🔧 4. Add CLI for `delete` in `main()`:

```python
# Delete
p_delete = subparsers.add_parser("delete", help="Delete a command by ID")
p_delete.add_argument("id", help="ID (or partial ID) of the command to delete")
p_delete.set_defaults(func=delete_command)
```

---

### 🧪 Example Usage

```bash
python cmd_saver.py delete a1b2c3d4
```

And you’ll find a backup saved in the same folder.

---

You’re now running a **safe, editable, deletable CLI tool** with **auto backup**, all in one file. You’re pretty much 80% of the way to a legit app.

Ready for export, sync, encryption, or a GUI when you are. Just say the next two.

## Export

[Top](#design-document)

Next.

Let’s go — here are the **next two features** added to your one-file CLI app:

---

### 🧩 Feature 3: **Export to Markdown**

Save all commands into a nice `commands.md` file.

### 🧩 Feature 4: **Fuzzy Search**

Instead of exact keyword matching, it finds *similar* words in description/tags using fuzzy matching (great for typos or partial words).

---

### ✅ Updated Code Blocks for Your File (`cmd_saver.py`)

#### 1. Install requirement for fuzzy search:

```bash
pip install thefuzz[speedup]
```

Add this import at the top of your file:

```python
from thefuzz import fuzz
```

---

#### 2. 🆕 Update `search_command()` to support fuzzy matching:

Replace your existing `search_commands()` with this:

```python
def search_commands(args):
commands = load_commands()
found = False
for cmd in commands:
desc_score = fuzz.partial_ratio(args.query.lower(), cmd["description"].lower())
tags_score = fuzz.partial_ratio(args.query.lower(), " ".join(cmd["tags"]).lower())
if desc_score > 70 or tags_score > 70:
tags = ", ".join(cmd["tags"]) if cmd["tags"] else "-"
print(f"{cmd['id'][:8]} | {cmd['command']} - {cmd['description']} ({tags})")
found = True
if not found:
print("No matching commands found.")
```

---

#### 3. 🆕 Add `export_markdown()` function:

```python
def export_markdown(args):
commands = load_commands()
if not commands:
print("Nothing to export.")
return

lines = ["# Saved Commands\n"]
for cmd in commands:
lines.append(f"## `{cmd['command']}`")
lines.append(f"- **Description**: {cmd['description']}")
lines.append(f"- **Tags**: {', '.join(cmd['tags']) if cmd['tags'] else '-'}")
lines.append(f"- **Created**: {cmd['created_at']}")
lines.append("")

with open("commands.md", "w") as f:
f.write("\n".join(lines))

print("📝 Exported to `commands.md`.")
```

---

#### 4. Add `export` command to CLI setup:

Inside the `main()` function:

```python
# Export
p_export = subparsers.add_parser("export", help="Export all commands to Markdown")
p_export.set_defaults(func=export_markdown)
```

---

### 🧪 Usage Examples

```bash
python cmd_saver.py search docker  # Now fuzzy
python cmd_saver.py export         # Generates `commands.md`
```

---

### 📘 Sample Markdown Output

```markdown
# Saved Commands

## `git status`

- **Description**: Check status of current branch
- **Tags**: git, status
- **Created**: 2025-06-22T14:09:10

## `docker ps -a`
- **Description**: List all Docker containers
- **Tags**: docker, containers
- **Created**: 2025-06-22T14:12:55

```

---

Let me know when you're ready for the **next two**. Here are a few options you can pick from:

* 🔐 Encrypt the storage file
* 🌍 Sync to Git or remote server
* 📦 Turn into a Python package
* 💻 Build a simple terminal UI
* 🧠 Tag suggestions based on command content

Just say the word.

## Sum

[Top](#design-document)

Can you put all that we came up with this discussion into one file now?

Absolutely! Here’s your full-featured **single Python file** with everything we’ve built so far — add, list, search (with fuzzy), read, edit, delete, auto backup, and export to Markdown.

---

### Save this as `cmd_saver.py` and run away:

```python
import argparse
import json
import uuid
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from thefuzz import fuzz

# ---------- Model ----------
@dataclass
class Command:
id: str
command: str
description: str
tags: list[str]
created_at: str

@staticmethod
def create(command, description, tags):
return Command(
id=str(uuid.uuid4()),
command=command,
description=description,
tags=tags,
created_at=datetime.utcnow().isoformat()
)

# ---------- Storage ----------
DB_PATH = Path("commands.json")

def load_commands():
if not DB_PATH.exists():
return []
with open(DB_PATH, "r") as f:
return json.load(f)

def backup_commands():
if not DB_PATH.exists():
return
timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
backup_path = DB_PATH.with_name(f"commands_backup_{timestamp}.json")
with open(DB_PATH, "r") as original, open(backup_path, "w") as backup:
backup.write(original.read())

def save_commands(commands):
backup_commands()  # Backup before save
with open(DB_PATH, "w") as f:
json.dump(commands, f, indent=2)

# ---------- CLI Actions ----------
def add_command(args):
commands = load_commands()
new_cmd = Command.create(args.command, args.description, args.tags.split(",") if args.tags else [])
commands.append(asdict(new_cmd))
save_commands(commands)
print("✅ Command added.")

def list_commands(args):
commands = load_commands()
if not commands:
print("No commands saved yet.")
return
for cmd in commands:
tags = ", ".join(cmd["tags"]) if cmd["tags"] else "-"
print(f"{cmd['id'][:8]} | {cmd['command']} - {cmd['description']} ({tags})")

def search_commands(args):
commands = load_commands()
found = False
for cmd in commands:
desc_score = fuzz.partial_ratio(args.query.lower(), cmd["description"].lower())
tags_score = fuzz.partial_ratio(args.query.lower(), " ".join(cmd["tags"]).lower())
if desc_score > 70 or tags_score > 70:
tags = ", ".join(cmd["tags"]) if cmd["tags"] else "-"
print(f"{cmd['id'][:8]} | {cmd['command']} - {cmd['description']} ({tags})")
found = True
if not found:
print("No matching commands found.")

def read_command(args):
commands = load_commands()
for cmd in commands:
if cmd["id"].startswith(args.id):
print(f"🆔 ID: {cmd['id']}")
print(f"📅 Created: {cmd['created_at']}")
print(f"💻 Command: {cmd['command']}")
print(f"📝 Description: {cmd['description']}")
print(f"🏷️ Tags: {', '.join(cmd['tags']) if cmd['tags'] else '-'}")
return
print(f"No command found with ID starting with '{args.id}'")

def edit_command(args):
commands = load_commands()
updated = False
for cmd in commands:
if cmd["id"].startswith(args.id):
if args.command:
cmd["command"] = args.command
if args.description:
cmd["description"] = args.description
if args.tags is not None:
cmd["tags"] = args.tags.split(",") if args.tags else []
updated = True
break
if updated:
save_commands(commands)
print("✏️ Command updated.")
else:
print(f"No command found with ID starting with '{args.id}'")

def delete_command(args):
commands = load_commands()
new_commands = [cmd for cmd in commands if not cmd["id"].startswith(args.id)]
if len(new_commands) == len(commands):
print(f"No command found with ID starting with '{args.id}'")
return
save_commands(new_commands)
print("🗑️ Command deleted.")

def export_markdown(args):
commands = load_commands()
if not commands:
print("Nothing to export.")
return

lines = ["# Saved Commands\n"]
for cmd in commands:
lines.append(f"## `{cmd['command']}`")
lines.append(f"- **Description**: {cmd['description']}")
lines.append(f"- **Tags**: {', '.join(cmd['tags']) if cmd['tags'] else '-'}")
lines.append(f"- **Created**: {cmd['created_at']}")
lines.append("")

with open("commands.md", "w") as f:
f.write("\n".join(lines))

print("📝 Exported to `commands.md`.")

# ---------- CLI Setup ----------
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

# Search
p_search = subparsers.add_parser("search", help="Search commands by keyword")
p_search.add_argument("query", help="Search keyword")
p_search.set_defaults(func=search_commands)

# Read
p_read = subparsers.add_parser("read", help="View details of a command by ID")
p_read.add_argument("id", help="ID (or partial ID) of the command to view")
p_read.set_defaults(func=read_command)

# Edit
p_edit = subparsers.add_parser("edit", help="Edit an existing command")
p_edit.add_argument("id", help="ID (or partial ID) of the command to edit")
p_edit.add_argument("--command", help="New command string")
p_edit.add_argument("--description", help="New description")
p_edit.add_argument("--tags", help="New comma-separated tags (empty to clear)")
p_edit.set_defaults(func=edit_command)

# Delete
p_delete = subparsers.add_parser("delete", help="Delete a command by ID")
p_delete.add_argument("id", help="ID (or partial ID) of the command to delete")
p_delete.set_defaults(func=delete_command)

# Export
p_export = subparsers.add_parser("export", help="Export all commands to Markdown")
p_export.set_defaults(func=export_markdown)

args = parser.parse_args()
if hasattr(args, "func"):
args.func(args)
else:
parser.print_help()

if __name__ == "__main__":
main()
```

---

### 🔥 Quick Setup Notes:

* You’ll need to install the fuzzy search library:

```bash
pip install thefuzz[speedup]
```

* Run commands like:

```bash
python cmd_saver.py add "git status" "Show git status" --tags git,version-control
python cmd_saver.py list
python cmd_saver.py search git
python cmd_saver.py read a1b2c3
python cmd_saver.py edit a1b2c3 --description "Updated description"
python cmd_saver.py delete a1b2c3
python cmd_saver.py export
```

---

You’ve got a fully featured, easy-to-expand CLI app — all in one neat file!

If you want help turning this into a server, GUI, or package next, just shout.

## Tree

[Top](#design-document)

I think I will start from this, but I will separate all of this into different files, so main, data model, commands, and so on.

That’s a solid plan! Splitting it into separate files will make your code way easier to maintain and expand over time. Here’s a simple suggested structure you might consider:

```
cmd_saver/
│
├── main.py             # CLI entrypoint, argument parsing, command dispatch
├── model.py            # Command dataclass and any model logic
├── storage.py          # Load, save, backup commands
├── commands/           # Each command handler in its own file or grouped logically
│   ├── add.py
│   ├── list.py
│   ├── search.py
│   ├── read.py
│   ├── edit.py
│   ├── delete.py
│   └── export.py
└── requirements.txt    # e.g. thefuzz[speedup]
```

### Benefits of this approach:

* **Separation of concerns:** Clean, focused files.
* **Easier testing:** Test each command or module independently.
* **Team collaboration:** Others can jump in on just one part.
* **Faster iteration:** Find and fix bugs faster.

---

If you want, I can help you scaffold this structure with starter files and example imports! Just say the word. Otherwise, good luck and enjoy coding your project! 🚀

