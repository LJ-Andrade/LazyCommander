import json
from pathlib import Path

from platformdirs import user_data_dir

from src.models.command import Command


class JsonStore:
    def __init__(self, app_name: str = "LazyCommander"):
        self._data_dir = Path(user_data_dir(app_name, appauthor=False))
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._file_path = self._data_dir / "commands.json"

    def load(self) -> list[Command]:
        if not self._file_path.exists():
            return []
        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Command.from_dict(cmd) for cmd in data]
        except (json.JSONDecodeError, KeyError):
            return []

    def save(self, commands: list[Command]) -> None:
        data = [cmd.to_dict() for cmd in commands]
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add(self, command: Command) -> None:
        commands = self.load()
        commands.append(command)
        self.save(commands)

    def update(self, command: Command) -> None:
        commands = self.load()
        for i, cmd in enumerate(commands):
            if cmd.id == command.id:
                commands[i] = command
                break
        self.save(commands)

    def delete(self, command_id: str) -> None:
        commands = self.load()
        commands = [cmd for cmd in commands if cmd.id != command_id]
        self.save(commands)

    def get_by_id(self, command_id: str) -> Command | None:
        commands = self.load()
        for cmd in commands:
            if cmd.id == command_id:
                return cmd
        return None

    def get_by_name(self, name: str) -> Command | None:
        commands = self.load()
        for cmd in commands:
            if cmd.name == name:
                return cmd
        return None
