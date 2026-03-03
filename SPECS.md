# LazyCommander - Technical Specification

## Project Overview

- **Name:** LazyCommander
- **Type:** TUI Command Launcher
- **Core Functionality:** Quick command runner - store shell commands with custom names, browse them in a list, select and execute with Enter

---

## Data Model

### Command Entity
```python
Command:
  - id: str (UUID)
  - name: str (user-friendly label, max 50 chars)
  - command: str (the actual shell command)
  - description: str (optional, max 200 chars)
  - created_at: datetime
  - last_used: datetime (nullable)
  - use_count: int (default 0)
```

### Storage
- **Format:** JSON file
- **Location:** `{user_data_dir}/lazycommander/commands.json`
- **User data dir:** `~/.lazycommander/` on Linux/Mac, `%APPDATA%/LazyCommander/` on Windows

---

## UI Layout

### Main Screen (Split View)
```
┌─────────────────────────────────────────────────────────┐
│  LazyCommander                              [Ctrl+Q]   │
├───────────────────────┬─────────────────────────────────┤
│  Commands             │  Command Details                │
│  ─────────────────    │  ─────────────────────────────  │
│  > git status         │  Name: git status               │
│    npm run dev        │  Command: git status            │
│    docker ps          │  Description: Check repo status │
│    python test.py     │  Use count: 5                   │
│                       │                                 │
│                       │  [Enter] Run   [Ctrl+E] Edit    │
│                       │  [Ctrl+N] New  [Del] Delete     │
├───────────────────────┴─────────────────────────────────┤
│  ↑↓ Navigate  Enter Run  Ctrl+N New  Ctrl+E Edit  Del  │
└─────────────────────────────────────────────────────────┘
```

- **Left Panel (40%):** List of saved commands (navigable)
- **Right Panel (60%):** Selected command details + action buttons
- **Footer:** Keybindings hint bar

---

## Core Features

### F1: View Commands List
- Display all saved commands in left panel
- Show name truncated to 30 chars in list view
- Highlight selected item with different color
- Sort by: last_used descending (default), name alphabetically, use_count descending

### F2: Add New Command
- Trigger: Ctrl+N or button in details panel
- Modal form with fields: name, command, description
- Validation: name and command required, name must be unique
- Save to JSON file on submit

### F3: Edit Command
- Trigger: Ctrl+E or Edit button
- Same form as Add, pre-filled with current data
- Update JSON on save

### F4: Delete Command
- Trigger: Delete key
- Confirmation dialog before deletion
- Remove from JSON file

### F5: Execute Command
- Trigger: Enter key or Run button
- Execute via `subprocess.run(shell=True)` (cross-platform)
- Show output in a modal or new panel (or just run and let user see terminal)
- Update last_used and use_count after execution

### F6: Search/Filter Commands
- Trigger: Ctrl+F or `/` key
- Filter list by name or command text (case-insensitive)
- Show filtered results in real-time

### F7: Import/Export Commands
- Trigger: Ctrl+I (import), Ctrl+Shift+E (export)
- Export: save commands.json to user-chosen location
- Import: load commands from user-chosen JSON file

---

## Keybindings

| Key | Action |
|-----|--------|
| ↑ / ↓ | Navigate command list |
| Enter | Execute selected command |
| Ctrl+N || Ctrl+E | Edit selected command |
 Add new command |
| Ctrl+F | Search/filter commands |
| Delete | Delete selected command |
| Ctrl+Q | Quit application |
| Escape | Close modal / cancel operation |

---

## Edge Cases & Constraints

1. **Empty state:** Show friendly message "No commands yet. Press Ctrl+N to add one."
2. **Invalid JSON file:** Create new empty file, show warning
3. **Command execution fails:** Show error message in modal, don't crash
4. **Very long command output:** Truncate or allow scroll (future enhancement)
5. **Duplicate names:** Prevent, show validation error
6. **Special characters in commands:** Support shell metacharacters, escape properly

---

## Visual Design

- **Theme:** Dark mode by default (terminal-friendly)
- **Colors:**
  - Background: `#1e1e2e` (dark blue-gray)
  - Primary accent: `#89b4fa` (soft blue)
  - Secondary: `#45475a` (muted gray)
  - Text: `#cdd6f4` (light gray)
  - Success: `#a6e3a1` (green)
  - Error: `#f38ba8` (red)
- **ASCII Logo (header):** Simple "LC>" prompt style
- **Animations:** Fade-in for modals, smooth list scrolling

---

## Acceptance Criteria

- [ ] App launches and shows split-view UI
- [ ] Can add a new command with name and command text
- [ ] Can see list of commands on left panel
- [ ] Can navigate with arrow keys
- [ ] Can select a command and see details on right panel
- [ ] Can execute a command with Enter
- [ ] Can edit existing commands
- [ ] Can delete commands with confirmation
- [ ] Can filter/search commands
- [ ] Data persists between app restarts (JSON)
- [ ] Works on Windows (primary) and Linux
- [ ] ASCII art header/logo displays correctly
- [ ] Keybindings work as documented

---

## Future Enhancements (Out of Scope for v1)

- Command output panel
- Command categories/groups
- Favorites / pinned commands
- Command history
- Multiple command profiles
- Syntax highlighting for output
