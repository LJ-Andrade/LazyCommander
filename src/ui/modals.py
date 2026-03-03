from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Static, TextArea


class CommandFormModal(ModalScreen):
    def __init__(self, command=None, **kwargs):
        super().__init__(**kwargs)
        self.command = command
        self._is_edit = command is not None

    def compose(self) -> ComposeResult:
        title = "Edit Command" if self._is_edit else "Add New Command"
        yield Static(title, id="modal-title", classes="modal-header")
        with Vertical(id="form-container", classes="modal-content"):
            yield Input(placeholder="Command name", id="input-name")
            yield Input(placeholder="Command to execute", id="input-command")
            yield Input(placeholder="Description (optional)", id="input-description")
        with Horizontal(id="modal-buttons"):
            yield Button("Cancel", id="btn-cancel", variant="default")
            yield Button("Save", id="btn-save", variant="primary")

    def on_mount(self) -> None:
        print("[DEBUG] CommandFormModal mounted")
        if self.command:
            self.query_one("#input-name", Input).value = self.command.name
            self.query_one("#input-command", Input).value = self.command.command
            self.query_one("#input-description", Input).value = self.command.description or ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancel":
            self.dismiss(None)
        elif event.button.id == "btn-save":
            data = {
                "name": self.query_one("#input-name", Input).value.strip(),
                "command": self.query_one("#input-command", Input).value.strip(),
                "description": self.query_one("#input-description", Input).value.strip(),
                "edit": self._is_edit,
                "original_command": self.command,
            }
            self.dismiss(data)


class ConfirmDeleteModal(ModalScreen):
    def __init__(self, command_name: str, **kwargs):
        super().__init__(**kwargs)
        self.command_name = command_name

    def compose(self) -> ComposeResult:
        yield Static(f"Delete '{self.command_name}'?", id="modal-title", classes="modal-header")
        yield Static("This action cannot be undone.", id="modal-message")
        with Horizontal(id="modal-buttons"):
            yield Button("Cancel", id="btn-cancel", variant="default")
            yield Button("Delete", id="btn-delete", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancel":
            self.dismiss(None)
        elif event.button.id == "btn-delete":
            self.dismiss(event.button.id)


class SearchModal(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Static("Search commands", id="modal-title", classes="modal-header")
        yield Input(placeholder="Type to search...", id="input-search")
        with Horizontal(id="modal-buttons"):
            yield Button("Clear", id="btn-clear", variant="default")
            yield Button("Close", id="btn-close", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-clear":
            self.dismiss(event.button.id)
        elif event.button.id == "btn-close":
            self.dismiss(self)


class MessageModal(ModalScreen):
    def __init__(self, message: str, title: str = "Message", **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.title_text = title

    def compose(self) -> ComposeResult:
        yield Static(self.title_text, id="modal-title", classes="modal-header")
        yield Static(self.message, id="modal-message")
        with Horizontal(id="modal-buttons"):
            yield Button("OK", id="btn-ok", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(self)
