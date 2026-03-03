from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Command:
    name: str
    command: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    last_used: datetime | None = None
    use_count: int = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "command": self.command,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "use_count": self.use_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Command":
        return cls(
            id=data["id"],
            name=data["name"],
            command=data["command"],
            description=data.get("description", ""),
            created_at=datetime.fromisoformat(data["created_at"]),
            last_used=datetime.fromisoformat(data["last_used"]) if data.get("last_used") else None,
            use_count=data.get("use_count", 0),
        )
