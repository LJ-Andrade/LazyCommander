from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static

from src.ui.theme import ASCII_LOGO
from src.ui.widgets import CommandListView, DetailsPanel, HeaderBar, FooterBar


class MainLayout(Container):
    def compose(self) -> ComposeResult:
        yield HeaderBar(id="header")
        with Horizontal():
            with Vertical(id="left-panel", classes="panel"):
                yield CommandListView(id="command-list")
            with Vertical(id="right-panel", classes="panel"):
                yield DetailsPanel(id="details")
        yield FooterBar(id="footer")


class Header(Static):
    def compose(self) -> ComposeResult:
        yield Static(ASCII_LOGO, markup=True)


class Footer(Static):
    KEYBINDS = [
        ("up", "cursor_up", "↑"),
        ("down", "cursor_down", "↓"),
        ("enter", "execute", "Run"),
        ("ctrl+n", "add_command", "New"),
        ("ctrl+e", "edit_command", "Edit"),
        ("ctrl+f", "filter", "Search"),
        ("delete", "delete_command", "Del"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        parts = []
        for key, action, label in self.KEYBINDS:
            parts.append(f"[dim]{key}[/dim] {label}")
        yield Static("  |  ".join(parts), markup=True)
