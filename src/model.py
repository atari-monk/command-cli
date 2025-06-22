from dataclasses import dataclass
from datetime import datetime
from typing import List
import uuid

@dataclass
class Command:
    id: str
    command: str
    description: str
    tags: List[str]
    created_at: str

    @staticmethod
    def create(command: str, description: str, tags: List[str]) -> 'Command':
        return Command(
            id=str(uuid.uuid4()),
            command=command,
            description=description,
            tags=tags or [],
            created_at=datetime.now().isoformat()
        )