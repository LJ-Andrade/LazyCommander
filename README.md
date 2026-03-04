# LazyCommander

A TUI command launcher for quick command execution.

## Requirements

- Python 3.10+
- Windows or Linux

## Installation

```bash
pip install -e .
```

## Usage

```bash
python -m src.app
```

Or simply:

```bash
lazycommander
```

## Keybindings

| Key | Action |
|-----|--------|
| ↑ / ↓ | Navigate command list |
| Enter | Execute selected command |
| Ctrl+N | Add new command |
| Ctrl+E | Edit selected command |
| Ctrl+F | Search/filter commands |
| Delete | Delete selected command |
| Escape | Cancel / Close |
| Ctrl+Q | Quit application |

## Data Storage

Commands are stored in:
- **Windows:** `%APPDATA%/LazyCommander/commands.json`
- **Linux:** `~/.lazycommander/commands.json`
