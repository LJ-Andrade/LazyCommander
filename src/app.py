from datetime import datetime

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Static

from src.models.command import Command
from src.storage.json_store import JsonStore
from src.ui.theme import THEME
from src.ui.widgets import CommandListItem, CommandListView, DetailsPanel


class LazyCommanderApp(App):
    CSS = """
    Screen {
        background: $background;
    }
    
    #main-container {
        height: 100%;
    }
    
    #top-row {
        height: 60%;
    }
    
    #bottom-row {
        height: 30%;
        border-top: solid $secondary;
    }
    
    #footer {
        dock: bottom;
        height: 1;
        padding: 0 1;
        background: $surface;
        color: $text-muted;
    }
    
    #left-panel {
        width: 40%;
        border-right: solid $secondary;
    }
    
    #right-panel {
        width: 60%;
    }
    
    #command-list {
        height: 100%;
    }
    
    #details {
        padding: 2;
    }
    
    #output {
        padding: 1;
        background: #11111b;
        color: #cdd6f4;
    }
    
    #footer {
        dock: bottom;
        height: 1;
        padding: 0 1;
        background: $surface;
        color: $text-muted;
    }
    
    .panel {
        background: $background;
    }
    
    .hidden {
        display: none;
    }
    
    ListView > ListItem {
        padding: 0 1;
    }
    
    ListView > ListItem:hover {
        background: $surface;
    }
    
    #form-container {
        padding: 1;
        height: 100%;
    }
    
    #form-container Input {
        margin: 1 0;
    }
    
    #form-buttons {
        margin-top: 2;
    }
    
    #form-buttons Button {
        margin: 0 1;
    }
    
    
    #form-container Button {
        margin: 1 1;
    }
    
    #delete-confirm {
        height: 3;
        background: #f38ba8;
        color: #11111b;
        padding: 0 1;
    }
    
    .form-title {
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }
    
    .form-label {
        color: $text-muted;
    }
    """

    BINDINGS = [
        Binding("up", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("enter", "handle_enter", "Enter", show=False),
        Binding("ctrl+n", "add_command", "New"),
        Binding("ctrl+e", "edit_command", "Edit"),
        Binding("ctrl+f", "filter", "Search"),
        Binding("delete", "delete_command", "Delete"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("escape", "escape_mode", "Escape", show=False),
    ]

    themes = [THEME]

    def __init__(self):
        super().__init__()
        self.store = JsonStore()
        self.commands: list[Command] = []
        self.filter_text = ""
        self.mode = "list"  # "list", "form", "delete_confirm"
        self.form_command = None  # Command being edited (None = new)
        self.output_lines: list[str] = []

    def compose(self) -> ComposeResult:
        with Vertical(id="main-container"):
            with Horizontal(id="top-row", classes="panel"):
                with Vertical(id="left-panel", classes="panel"):
                    yield CommandListView(id="command-list")
                    yield Vertical(id="form-container", classes="hidden")
                with Vertical(id="right-panel", classes="panel"):
                    yield DetailsPanel(id="details")
            with Vertical(id="bottom-row", classes="panel"):
                yield Static("Output", classes="title")
                yield Static("", id="output")
            yield Static("Up/Down: Navigate | Enter: Run | Ctrl+N: New | Ctrl+E: Edit | Ctrl+F: Search | Del: Delete | Ctrl+Q: Quit", id="footer")

    def on_mount(self) -> None:
        self.title = "LazyCommander"
        self.commands = self.store.load()
        self.refresh_command_list()
        self.update_output("Ready. Press Ctrl+N to add a command.")

    def refresh_command_list(self) -> None:
        list_view = self.query_one("#command-list")
        list_view.clear()

        filtered = self.commands
        if self.filter_text:
            q = self.filter_text.lower()
            filtered = [c for c in self.commands if q in c.name.lower() or q in c.command.lower()]

        for cmd in filtered:
            item = CommandListItem(
                command_id=cmd.id,
                name=cmd.name,
                use_count=cmd.use_count,
            )
            list_view.append(item)

        if filtered:
            list_view.index = 0

        self.update_details_panel()

    def update_details_panel(self) -> None:
        list_view = self.query_one("#command-list")
        details = self.query_one("#details")

        if self.mode == "form":
            return

        if list_view.index is not None and list_view.index < len(list_view.children):
            item = list_view.children[list_view.index]
            cmd = self.store.get_by_id(item.command_id)
            if cmd:
                last_used = cmd.last_used.strftime("%Y-%m-%d %H:%M") if cmd.last_used else ""
                details.update_content(
                    name=cmd.name,
                    command=cmd.command,
                    description=cmd.description,
                    use_count=cmd.use_count,
                    last_used=last_used,
                )
                return

        details.update_content()

    def update_output(self, text: str) -> None:
        self.output_lines.append(text)
        if len(self.output_lines) > 100:
            self.output_lines = self.output_lines[-100:]
        output = self.query_one("#output")
        output.update("\n".join(self.output_lines))

    def clear_output(self) -> None:
        self.output_lines = []
        self.query_one("#output").update("")

    def show_form(self, command=None) -> None:
        self.mode = "form"
        self.form_command = command
        
        list_view = self.query_one("#command-list")
        form_container = self.query_one("#form-container")
        
        list_view.add_class("hidden")
        form_container.remove_class("hidden")
        
        form_container.remove_children()
        
        title_text = "Edit Command" if command else "Add New Command"
        
        form_container.mount(Static(title_text, classes="form-title"))
        form_container.mount(Static("Name:", classes="form-label"))
        form_container.mount(Input(placeholder="Command name", id="input-name"))
        form_container.mount(Static("Command:", classes="form-label"))
        form_container.mount(Input(placeholder="Command to execute", id="input-command"))
        form_container.mount(Static("Description:", classes="form-label"))
        form_container.mount(Input(placeholder="Description (optional)", id="input-description"))
        
        with Horizontal(id="form-buttons"):
            form_container.mount(Button("Cancel", id="btn-cancel", variant="default"))
            form_container.mount(Button("Save", id="btn-save", variant="primary"))
        
        if command:
            self.query_one("#input-name", Input).value = command.name
            self.query_one("#input-command", Input).value = command.command
            self.query_one("#input-description", Input).value = command.description or ""
        
        self.query_one("#input-name", Input).focus()
        
        self.query_one("#details").update_content()

    def hide_form(self) -> None:
        self.mode = "list"
        self.form_command = None
        
        list_view = self.query_one("#command-list")
        form_container = self.query_one("#form-container")
        
        form_container.add_class("hidden")
        list_view.remove_class("hidden")
        
        self.commands = self.store.load()
        self.refresh_command_list()

    def show_delete_confirm(self) -> None:
        list_view = self.query_one("#command-list")
        if list_view.index is None or list_view.index >= len(list_view.children):
            return
        
        item = list_view.children[list_view.index]
        cmd = self.store.get_by_id(item.command_id)
        if not cmd:
            return
        
        self.mode = "delete_confirm"
        
        form_container = self.query_one("#form-container")
        form_container.display = True
        
        form_container.remove_children()
        
        form_container.mount(Static(f"Delete '{cmd.name}'?", classes="form-title"))
        form_container.mount(Static("This action cannot be undone.", id="delete-confirm"))
        form_container.mount(Static("[Cancel] Esc  [Delete] Enter", id="form-hint"))

    def hide_delete_confirm(self) -> None:
        self.mode = "list"
        form_container = self.query_one("#form-container")
        form_container.add_class("hidden")
        list_view = self.query_one("#command-list")
        list_view.remove_class("hidden")

    def on_list_view_selected(self, event) -> None:
        self.update_details_panel()
        if self.mode == "list":
            self.action_execute()

    def action_cursor_up(self) -> None:
        if self.mode == "form":
            self.query_one("#input-name", Input).focus()
            return
        
        if self.mode == "delete_confirm":
            return
        
        list_view = self.query_one("#command-list")
        list_view.action_cursor_up()
        self.update_details_panel()

    def action_cursor_down(self) -> None:
        if self.mode == "form":
            return
        
        if self.mode == "delete_confirm":
            return
        
        list_view = self.query_one("#command-list")
        list_view.action_cursor_down()
        self.update_details_panel()

    def action_add_command(self) -> None:
        self.show_form(None)

    def action_edit_command(self) -> None:
        list_view = self.query_one("#command-list")
        if list_view.index is None or list_view.index >= len(list_view.children):
            return
        item = list_view.children[list_view.index]
        cmd = self.store.get_by_id(item.command_id)
        if cmd:
            self.show_form(cmd)

    def action_delete_command(self) -> None:
        self.show_delete_confirm()

    def action_handle_enter(self) -> None:
        if self.mode == "form":
            self.action_save_form()
        elif self.mode == "delete_confirm":
            self.action_confirm_delete()
        else:
            self.action_execute()

    def action_execute(self) -> None:
        if self.mode != "list":
            return
        
        list_view = self.query_one("#command-list")
        if list_view.index is None or list_view.index >= len(list_view.children):
            return
        item = list_view.children[list_view.index]
        cmd = self.store.get_by_id(item.command_id)
        if cmd:
            self.run_command(cmd)

    def action_filter(self) -> None:
        self.push_screen(SearchModal(), self._on_search)

    def action_escape_mode(self) -> None:
        if self.mode == "form":
            self.hide_form()
        elif self.mode == "delete_confirm":
            self.hide_delete_confirm()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if self.mode == "form":
            if event.button.id == "btn-cancel":
                self.hide_form()
            elif event.button.id == "btn-save":
                self.action_save_form()
        elif self.mode == "delete_confirm":
            if event.button.id == "btn-cancel":
                self.hide_delete_confirm()
            elif event.button.id == "btn-delete":
                self.action_confirm_delete()

    def action_save_form(self) -> None:
        if self.mode != "form":
            return
        
        name_input = self.query_one("#input-name", Input)
        command_input = self.query_one("#input-command", Input)
        desc_input = self.query_one("#input-description", Input)
        
        name = name_input.value.strip()
        command = command_input.value.strip()
        description = desc_input.value.strip()
        
        if not name or not command:
            self.update_output("Error: Name and command are required.")
            return
        
        if self.form_command:
            self.form_command.name = name
            self.form_command.command = command
            self.form_command.description = description
            self.store.update(self.form_command)
            self.update_output(f"Command '{name}' updated.")
        else:
            cmd = Command(name=name, command=command, description=description)
            self.store.add(cmd)
            self.update_output(f"Command '{name}' created.")
        
        self.hide_form()

    def action_confirm_delete(self) -> None:
        if self.mode != "delete_confirm":
            return
        
        list_view = self.query_one("#command-list")
        if list_view.index < len(list_view.children):
            item = list_view.children[list_view.index]
            cmd = self.store.get_by_id(item.command_id)
            if cmd:
                self.store.delete(item.command_id)
                self.update_output(f"Command '{cmd.name}' deleted.")
        
        self.hide_delete_confirm()
        self.commands = self.store.load()
        self.refresh_command_list()

    def _on_search(self, result) -> None:
        if result == "btn-clear":
            self.filter_text = ""
        elif result:
            input_search = self.screen.query_one("#input-search", Input)
            self.filter_text = input_search.value.strip()
        self.refresh_command_list()

    def run_command(self, cmd: Command) -> None:
        import subprocess

        self.clear_output()
        self.update_output(f"$ {cmd.command}")

        try:
            result = subprocess.run(
                cmd.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            cmd.last_used = datetime.now()
            cmd.use_count += 1
            self.store.update(cmd)
            self.commands = self.store.load()
            
            if result.stdout:
                self.update_output(result.stdout)
            if result.stderr:
                self.update_output(f"[ERROR] {result.stderr}")
            
            if result.returncode == 0:
                self.update_output(f"[Done] Exit code: {result.returncode}")
            else:
                self.update_output(f"[Failed] Exit code: {result.returncode}")
            
            self.refresh_command_list()
            
        except subprocess.TimeoutExpired:
            self.update_output("[ERROR] Command timed out.")
        except Exception as e:
            self.update_output(f"[ERROR] {str(e)}")


class SearchModal(ModalScreen):
    CSS = """
    ModalScreen .buttons-container {
        align-horizontal: center;
    }
    Button:focus {
        border: solid $accent;
    }
    Button {
        margin: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Search commands", id="modal-title", classes="modal-header")
        yield Input(placeholder="Type to search...", id="input-search")
        with Horizontal(classes="buttons-container"):
            yield Button("Clear", id="btn-clear", variant="default")
            yield Button("Close", id="btn-close", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-clear":
            self.dismiss(event.button.id)
        elif event.button.id == "btn-close":
            self.dismiss(self)

    def on_key(self, event) -> None:
        if event.key == "left":
            self._navigate_buttons(-1)
        elif event.key == "right":
            self._navigate_buttons(1)
        elif event.key == "enter":
            button = self.focused
            if button and hasattr(button, "id"):
                self.on_button_pressed(type("Event", (), {"button": button})())

    def _navigate_buttons(self, direction: int) -> None:
        buttons = list(self.query("Button"))
        if not buttons:
            return
        current = self.focused
        if current in buttons:
            idx = buttons.index(current)
            idx = (idx + direction) % len(buttons)
        else:
            idx = 0 if direction > 0 else len(buttons) - 1
        buttons[idx].focus()
