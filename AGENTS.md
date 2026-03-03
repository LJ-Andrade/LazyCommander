# Project Instructions

> These instructions are loaded into the LLM context for every session.
> Customize them per project by filling in the placeholders marked with `[TODO]`.

---

## Project Overview

- **Name:** LazyCommander
- **Type:** TUI (Terminal User Interface) - Command Launcher
- **Tech Stack:** Python + Textual
- **Package Manager:** pip

## Project Structure

```
├── src/            # Source code
├── tests/          # Test files
├── docs/           # Documentation
├── AGENTS.md       # This file — LLM instructions
├── SPECS.md        # Technical specifications for current work
├── PLAN.md         # Task checklist / roadmap
├── DEVLOG.md       # Development log / changelog
└── PROJECT_CONTEXT.md  # Deep project context and architecture notes
```

## Code Standards

- **Language for code and comments:** English
- **Language for user communication:** Spanish
- All commits and branch names must be in English
- [TODO: Add coding conventions specific to your stack]

## External File References

When you encounter a file reference below, read it on a **need-to-know basis** using your Read tool. Do NOT preload all references upfront.

| Reference | When to read |
|-----------|-------------|
| `SPECS.md` | Before writing any implementation — contains current technical specs |
| `PLAN.md` | Before starting work — contains the task checklist and priorities |
| `DEVLOG.md` | When asked for a checkpoint or to review progress |
| `PROJECT_CONTEXT.md` | When you need deep architectural context about the project |

---

## Development Workflow

Follow this phased approach for any non-trivial task. For quick fixes, skip to Phase 4.

### Phase 1 — Discovery

- Analyze relevant files to understand the current state
- Generate a short "Technical Proposal" with your findings
- **Ask for user approval before proceeding**

### Phase 2 — Specification

- Generate or update `SPECS.md` with:
  - Data contracts / interfaces
  - UI changes (if applicable)
  - Edge cases and constraints
- **Ask for user approval before proceeding**

### Phase 3 — Planning

- Generate a numbered checklist in `PLAN.md`
- One task per file or logical unit
- Mark dependencies between tasks

### Phase 4 — Execution

- Apply changes file by file, following the plan
- Stay focused on the current task — do not scope-creep
- After each logical unit, verify it works before moving on

---

## Core Rules

1. **No Vibe Coding** — If information is missing, **stop and ask**. Never guess requirements.
2. **Review Gate** — No code is written without explicit user approval on the spec and plan.
3. **Context Isolation** — Treat each task as a fresh cycle. Re-read relevant files instead of relying on stale context.
4. **Incremental Changes** — Make small, testable changes. Do not rewrite large sections at once.
5. **Artifact Persistence** — Always update `PLAN.md` and `DEVLOG.md` to maintain state across sessions.

---

## Quick Commands

These are shorthand instructions you can use in chat:

| Command | Action |
|---------|--------|
| `/explore` | Analyze impact of an idea — run Phase 1 only |
| `/spec` | Draft technical specifications — run Phase 2 |
| `/plan` | Generate a task checklist — run Phase 3 |
| `/build` | Start implementation — run Phase 4 |
| `/checkpoint` | Update DEVLOG.md, create a git commit, ask about push |

---

## Checkpoint Protocol

When a **checkpoint** is requested:
1. Update `DEVLOG.md` with completed features and relevant notes.
2. Create a Git commit with a descriptive message (in English).
3. Ask the user whether to push to the remote repository.
