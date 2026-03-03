from datetime import datetime

from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.theme import Theme
from textual.widgets import Input, Static

from src.models.command import Command
from src.storage.json_store import JsonStore
from src.ui.modals import (
    CommandFormModal,
    ConfirmDeleteModal,
    MessageModal,
    SearchModal,
)
from src.ui.theme import THEME
from src.ui.widgets import CommandListItem, CommandListView, DetailsPanel


class LazyCommanderApp(App):
    CSS = """
    Screen {
        background: $background;
    }
    
    #header {
        height: auto;
        background: $surface;
        padding: 1;
    }
    
    #footer {
        height: auto;
        background: $surface;
        padding: 0 1;
        dock: bottom;
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
    
    .panel {
        background: $background;
    }
    
    ListView > ListItem {
        padding: 0 1;
    }
    
    ListView > ListItem:hover {
        background: $surface;
    }
    """

    BINDINGS = [
        Binding("up", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("enter", "execute", "Run", show=False),
        Binding("ctrl+n", "add_command", "New"),
        Binding("ctrl+e", "edit_command", "Edit"),
        Binding("ctrl+f", "filter", "Search"),
        Binding("delete", "delete_command", "Delete"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("escape", "close_modal", "Close", show=False),
    ]

    themes = [THEME]

    def __init__(self):
        super().__init__()
        self.store = JsonStore()
        self.commands: list[Command] = []
        self.filter_text = ""

    def compose(self):
        yield Static(
            r"""
  _    _      _ _       
 | |  | |    | | |      
 | |__| | ___| | | ___  
 |  __  |/ _ \ | |/ _ \ 
 | |  | |  __/ | | (_) |
 |_|  |_|\___|_|_|\___/ 
                        
LazyCommander v0.1.0
""",
            markup=True,
        )
        with Horizontal():
            with Vertical(classes="panel"):
                yield CommandListView(id="command-list")
            with Vertical(classes="panel"):
                yield DetailsPanel(id="details")
        yield Static(
            "↑↓ Navigate | Enter Run | Ctrl+N New | Ctrl+E Edit | Ctrl+F Search | Del Delete | Ctrl+Q Quit",
            markup=True,
        )

    def on_mount(self) -> None:
        self.title = "LazyCommander"
        self.commands = self.store.load()
        self.refresh_command_list()

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

        if not list_view.index is None and list_view.index < len(list_view.children):
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

    def on_list_view_selected(self, event) -> None:
        self.update_details_panel()

    def action_cursor_up(self) -> None:
        list_view = self.query_one("#command-list")
        list_view.action_cursor_up()
        self.update_details_panel()

    def action_cursor_down(self) -> None:
        list_view = self.query_one("#command-list")
        list_view.action_cursor_down()
        self.update_details_panel()

    def action_add_command(self) -> None:
        self.push_screen(CommandFormModal(), self._on_add_command)

    def _on_add_command(self, data) -> None:
        if data:
            self._on_command_form_submit(data)

    def action_edit_command(self) -> None:
        list_view = self.query_one("#command-list")
        if list_view.index is None or list_view.index >= len(list_view.children):
            return
        item = list_view.children[list_view.index]
        cmd = self.store.get_by_id(item.command_id)
        if cmd:
            self.push_screen(CommandFormModal(cmd), self._on_edit_command)

    def _on_edit_command(self, data) -> None:
        if data:
            self._on_command_form_submit(data)

    def action_delete_command(self) -> None:
        list_view = self.query_one("#command-list")
        if list_view.index is None or list_view.index >= len(list_view.children):
            return
        item = list_view.children[list_view.index]
        cmd = self.store.get_by_id(item.command_id)
        if cmd:
            self.push_screen(ConfirmDeleteModal(cmd.name), self._on_delete_confirm)

    def _on_delete_confirm(self, result) -> None:
        if result == "btn-delete":
            list_view = self.query_one("#command-list")
            if list_view.index < len(list_view.children):
                item = list_view.children[list_view.index]
                self.store.delete(item.command_id)
                self.commands = self.store.load()
                self.refresh_command_list()

    def action_execute(self) -> None:
        list_view = self.query_one("#command-list")
        if list_view.index is None or list_view.index >= len(list_view.children):
            return
        item = list_view.children[list_view.index]
        cmd = self.store.get_by_id(item.command_id)
        if cmd:
            self.run_command(cmd)

    def action_filter(self) -> None:
        self.push_screen(SearchModal(), self._on_search)

    def _on_search(self, result) -> None:
        if result == "btn-clear":
            self.filter_text = ""
        elif result:
            input_search = self.screen.query_one("#input-search", Input)
            self.filter_text = input_search.value.strip()
        self.refresh_command_list()

    def _on_command_form_submit(self, data: dict) -> None:
        name = data.get("name", "")
        command = data.get("command", "")
        description = data.get("description", "")
        is_edit = data.get("edit", False)
        original_cmd = data.get("original_command")

        if not name or not command:
            self.push_screen(MessageModal("Name and command are required.", "Validation Error"))
            return

        if is_edit and original_cmd:
            original_cmd.name = name
            original_cmd.command = command
            original_cmd.description = description
            self.store.update(original_cmd)
        else:
            cmd = Command(name=name, command=command, description=description)
            print(f"[DEBUG] Adding command: {cmd}")
            self.store.add(cmd)

        self.commands = self.store.load()
        self.refresh_command_list()

    def _on_delete_confirm(self, screen: ConfirmDeleteModal) -> None:
        if screen.id == "btn-delete":
            list_view = self.query_one("#command-list")
            if list_view.index < len(list_view.children):
                item = list_view.children[list_view.index]
                self.store.delete(item.command_id)
                self.commands = self.store.load()
                self.refresh_command_list()

    def _on_search(self, screen: SearchModal) -> None:
        if screen.id == "btn-clear":
            self.filter_text = ""
        else:
            input_search = screen.query_one("#input-search", Input)
            self.filter_text = input_search.value.strip()
        self.refresh_command_list()

    def run_command(self, cmd: Command) -> None:
        import subprocess

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
            self.refresh_command_list()

            output = result.stdout if result.stdout else result.stderr
            self.push_screen(MessageModal(f"Command executed.\n\nOutput:\n{output[:500]}", "Execution Complete"))
        except subprocess.TimeoutExpired:
            self.push_screen(MessageModal("Command timed out.", "Error"))
        except Exception as e:
            self.push_screen(MessageModal(f"Error: {str(e)}", "Error"))
