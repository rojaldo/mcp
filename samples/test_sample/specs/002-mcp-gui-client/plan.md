# Implementation Plan: MCP GUI Client

**Branch**: `002-mcp-gui-client` | **Date**: 2026-04-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-mcp-gui-client/spec.md`

## Summary

Build a cross-platform desktop GUI application that provides graphical access to all MCP Test Questions Server tools and resources. The application enables users to create, browse, edit, and delete test questions through intuitive visual components, with support for multiple view formats (formatted, JSON, Markdown).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: tkinter (GUI), mcp (MCP client protocol), httpx (async HTTP client)
**Storage**: Local config persistence (JSON file for connection settings)
**Testing**: pytest with pytest-qt (for Tkinter testing)
**Target Platform**: Cross-platform desktop (Windows/macOS/Linux)
**Project Type**: desktop-app (GUI application)
**Performance Goals**: <1s UI response, <2s question list load for 100 items
**Constraints**: Must connect to existing MCP server (feature 001), single-user context
**Scale/Scope**: Client for 100-1000 questions, local user configuration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Test-First Development | ✅ PASS | Tests will be written before implementation (TDD cycle enforced) |
| II. Code Review Standards | ✅ PASS | Standard PR workflow will apply |
| III. Static Analysis Enforcement | ✅ PASS | ruff for linting, mypy for type checking |
| IV. Documentation Quality | ✅ PASS | Public GUI components will be documented |
| V. CI Quality Gates | ✅ PASS | pytest coverage target 60% (GUI testing constraints) |

**Quality Gates Compliance:**
- Test Coverage: Target 60%+ for GUI (realistic for desktop apps with UI complexity)
- Lint Status: ruff with zero warnings policy
- Type Check: mypy for non-GUI modules
- Build Status: Clean Python package build

## Project Structure

### Documentation (this feature)

```text
specs/002-mcp-gui-client/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output - UI component specs
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/
└── mcp_gui_client/
    ├── __init__.py
    ├── main.py              # Application entry point
    ├── config.py            # Configuration management
    ├── mcp_client/
    │   ├── __init__.py
    │   ├── connection.py    # MCP server connection
    │   └── tools.py         # MCP tool invocations
    ├── views/
    │   ├── __init__.py
    │   ├── main_window.py   # Main application window
    │   ├── question_list.py # Question list view
    │   ├── question_form.py # Create/edit form
    │   ├── question_detail.py # Question detail panel
    │   └── settings_dialog.py # Connection settings
    ├── widgets/
    │   ├── __init__.py
    │   ├── status_bar.py    # Status bar component
    │   ├── format_switcher.py # View format toggle
    │   └── confirmation_dialog.py # Delete confirmation
    └── utils/
        ├── __init__.py
        └── validators.py    # Input validation helpers

tests/
├── __init__.py
├── conftest.py
├── unit/
│   ├── __init__.py
│   ├── test_validators.py
│   └── test_mcp_client.py
├── integration/
│   ├── __init__.py
│   └── test_gui_flows.py
└── contract/
    ├── __init__.py
    └── test_ui_contracts.py

pyproject.toml
```

**Structure Decision**: Single project with MVC-style separation - models in mcp_client/, views in views/, reusable widgets in widgets/. Clear separation between MCP communication layer and presentation layer.

## Complexity Tracking

> No constitution violations detected - aligns with simplicity principles. Using Tkinter (built-in) reduces external dependencies.