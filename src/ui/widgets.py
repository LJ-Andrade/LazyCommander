from textual.widgets import ListView, ListItem, Static


class CommandListView(ListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_title = "Commands"


class CommandListItem(ListItem):
    def __init__(self, command_id: str, name: str, use_count: int = 0, **kwargs):
        super().__init__(Static(name), **kwargs)
        self.command_id = command_id
        self.use_count = use_count
        self.command_name = name


class DetailsPanel(Static):
    def __init__(self, **kwargs):
        super().__init__("", **kwargs)
        self._content = ""

    def update_content(self, name: str = "", command: str = "", description: str = "", use_count: int = 0, last_used: str = "") -> None:
        if not name:
            self.update("[dim]No command selected[/dim]")
            return
        
        self.update(
            f"[bold]Name:[/bold] {name}\n\n"
            f"[bold]Command:[/bold] [primary]{command}[/primary]\n\n"
            f"[bold]Description:[/bold] {description or '[dim]No description[/dim]'}\n\n"
            f"[bold]Times used:[/bold] {use_count}\n"
            f"[bold]Last used:[/bold] {last_used or '[dim]Never[/dim]'}"
        )


class HeaderBar(Static):
    def __init__(self, **kwargs):
        super().__init__("", **kwargs)


class FooterBar(Static):
    def __init__(self, **kwargs):
        super().__init__("", **kwargs)
