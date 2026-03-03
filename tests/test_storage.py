import json
import tempfile
from pathlib import Path

import pytest

from src.models.command import Command
from src.storage.json_store import JsonStore


class TestJsonStore:
    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as td:
            yield Path(td)

    @pytest.fixture
    def store(self, temp_dir, monkeypatch):
        def mock_user_data_dir(app_name: str) -> str:
            return str(temp_dir)

        monkeypatch.setattr("src.storage.json_store.user_data_dir", mock_user_data_dir)
        return JsonStore()

    def test_load_empty(self, store):
        commands = store.load()
        assert commands == []

    def test_add_command(self, store):
        cmd = Command(name="test", command="echo hello")
        store.add(cmd)
        commands = store.load()
        assert len(commands) == 1
        assert commands[0].name == "test"

    def test_update_command(self, store):
        cmd = Command(name="test", command="echo hello")
        store.add(cmd)
        cmd.command = "echo updated"
        store.update(cmd)
        commands = store.load()
        assert commands[0].command == "echo updated"

    def test_delete_command(self, store):
        cmd = Command(name="test", command="echo hello")
        store.add(cmd)
        store.delete(cmd.id)
        commands = store.load()
        assert len(commands) == 0

    def test_get_by_id(self, store):
        cmd = Command(name="test", command="echo hello")
        store.add(cmd)
        found = store.get_by_id(cmd.id)
        assert found is not None
        assert found.name == "test"

    def test_get_by_name(self, store):
        cmd = Command(name="test", command="echo hello")
        store.add(cmd)
        found = store.get_by_name("test")
        assert found is not None
        assert found.command == "echo hello"

    def test_get_by_name_not_found(self, store):
        found = store.get_by_name("nonexistent")
        assert found is None


class TestCommand:
    def test_to_dict(self):
        cmd = Command(name="test", command="echo hello", description="A test")
        data = cmd.to_dict()
        assert data["name"] == "test"
        assert data["command"] == "echo hello"
        assert data["description"] == "A test"
        assert "id" in data
        assert "created_at" in data

    def test_from_dict(self):
        data = {
            "id": "test-id",
            "name": "test",
            "command": "echo hello",
            "description": "A test",
            "created_at": "2024-01-01T00:00:00",
            "last_used": None,
            "use_count": 5,
        }
        cmd = Command.from_dict(data)
        assert cmd.id == "test-id"
        assert cmd.name == "test"
        assert cmd.use_count == 5
