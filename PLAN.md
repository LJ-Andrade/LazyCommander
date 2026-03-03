# LazyCommander - Task Plan

## Phase 1: Project Setup

- [x] 1.1 Create project directory structure (`src/`, `tests/`, `docs/`)
- [x] 1.2 Create `pyproject.toml` with dependencies (textual, pytest)
- [x] 1.3 Create virtual environment and install dependencies
- [x] 1.4 Verify Textual installation with minimal "hello world"

## Phase 2: Core Data Layer

- [x] 2.1 Create `src/models/command.py` - Command dataclass/model
- [x] 2.2 Create `src/storage/json_store.py` - JSON persistence layer
- [x] 2.3 Create `src/storage/__init__.py` - storage module init
- [x] 2.4 Write unit tests for storage (test_save, test_load, test_crud)

## Phase 3: UI Skeleton

- [x] 3.1 Create `src/app.py` - Main Textual application class
- [x] 3.2 Create `src/ui/layout.py` - Main screen with Split layout
- [x] 3.3 Create `src/ui/widgets.py` - Custom widgets (command list, details panel)
- [x] 3.4 Create `src/ui/theme.py` - Color theme definitions
- [x] 3.5 Create `src/ui/modals.py` - Modal components (add/edit form)
- [x] 3.6 Wire up keybindings (navigation, quit)
- [x] 3.7 Test empty state UI

## Phase 4: Command Management (CRUD)

- [x] 4.1 Implement Add Command flow (Ctrl+N → modal → save)
- [x] 4.2 Implement Edit Command flow (Ctrl+E → modal → update)
- [x] 4.3 Implement Delete Command flow (Del → confirm → remove)
- [x] 4.4 Implement list navigation (↑/↓, selection highlight)
- [x] 4.5 Connect right panel to show selected command details
- [ ] 4.6 Write integration tests for CRUD operations

## Phase 5: Command Execution

- [x] 5.1 Implement execute_command() using subprocess
- [x] 5.2 Hook up Enter key to execute selected command
- [x] 5.3 Update last_used and use_count after execution
- [x] 5.4 Handle execution errors gracefully (show message)
- [x] 5.5 Test execution on Windows

## Phase 6: Search/Filter

- [x] 6.1 Implement Ctrl+F search activation
- [x] 6.2 Create search input modal
- [x] 6.3 Filter command list in real-time
- [x] 6.4 Clear filter (Escape)

## Phase 7: Import/Export

- [ ] 7.1 Implement Ctrl+I import (load from JSON file)
- [ ] 7.2 Implement Ctrl+Shift+E export (save to JSON file)
- [ ] 7.3 Add file picker using Textual's built-in or native dialog

## Phase 8: Polish & Testing

- [x] 8.1 Add ASCII logo header
- [x] 8.2 Verify all keybindings work
- [x] 8.3 Run full test suite, fix failures
- [x] 8.4 Test on Windows end-to-end
- [ ] 8.5 Test on Linux (if available)
- [ ] 8.6 Create basic README.md

---

## Dependencies

- **Priority:** Phase 2 → 3 → 4 → 5 → 6 → 7 → 8
- **Testing:** Run tests after each phase completion
- **No parallel work:** Complete one phase before starting next
