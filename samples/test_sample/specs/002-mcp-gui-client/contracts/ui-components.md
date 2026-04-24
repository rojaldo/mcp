# UI Component Contracts

**Feature**: 002-mcp-gui-client
**Date**: 2026-04-22

This document defines the GUI component contracts and their interactions.

## Main Window

### Purpose
Primary application window containing all views and controls.

### Layout Structure
```
┌──────────────────────────────────────────────────────┐
│ Menu Bar: [File] [Edit] [View] [Help]                │
├──────────────────────────────────────────────────────┤
│ Tool Bar: [New Question] [Refresh] [Random] [Settings]│
├────────────────────┬─────────────────────────────────┤
│                    │                                 │
│ Question List      │   Question Detail Panel        │
│ (scrollable)       │   - Question Text              │
│                    │   - Answer Options              │
│ ┌──────────────┐   │   - Correct Answer             │
│ │ Question 1   │   │   - Format Switcher             │
│ │ Question 2   │   │   - [Edit] [Delete] buttons    │
│ │ Question 3   │   │                                 │
│ │ ...          │   │                                 │
│ └──────────────┘   │                                 │
│                    │                                 │
├────────────────────┴─────────────────────────────────┤
│ Status Bar: [Connection Status] [Operation Result]   │
└──────────────────────────────────────────────────────┘
```

### Responsibilities
- Window lifecycle management
- Menu and toolbar actions
- View coordination
- Status bar updates

---

## Question List Panel

### Purpose
Display scrollable list of all questions with preview information.

### Events
| Event | Callback | Description |
|-------|----------|-------------|
| selection_change | on_question_selected(question_id) | User clicks a question |
| double_click | on_question_edit(question_id) | Double-click to edit |
| right_click | show_context_menu() | Context menu (edit/delete) |

### Methods
| Method | Returns | Description |
|--------|---------|-------------|
| refresh() | None | Reload questions from server |
| get_selected() | str \| None | Get selected question ID |
| set_questions(questions) | None | Update list contents |
| clear() | None | Clear list |

### Display Format
Each list item shows:
- Question text (truncated to 50 chars)
- Number of options
- Status indicator (correct/warning)

---

## Question Form Panel

### Purpose
Create and edit questions with input validation.

### Fields
| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| question_text | Text | Required, 1-2000 chars | Question prompt |
| answer_options | List | 2-10 items, each 1-500 chars | Answer choices |
| correct_answer | Select | Must be in options | Correct selection |

### Methods
| Method | Returns | Description |
|--------|---------|-------------|
| validate() | bool | Check all fields valid |
| get_data() | dict | Get form data as dict |
| populate(question) | None | Fill form with existing question |
| clear() | None | Reset all fields |
| set_mode(mode) | None | Set 'create' or 'edit' mode |

### Events
| Event | Callback | Description |
|-------|----------|-------------|
| submit | on_submit() | Create/update button clicked |
| cancel | on_cancel() | Cancel button clicked |
| field_change | on_field_change() | Any field modified |

### Validation Rules
- Question text not empty
- At least 2 answer options
- At most 10 answer options
- No duplicate options
- Correct answer selected from options

---

## Question Detail Panel

### Purpose
Display single question with format switching support.

### View Formats
| Format | Description |
|--------|-------------|
| formatted | User-friendly card display |
| json | Raw JSON with syntax highlighting |
| markdown | Markdown rendering with checkmarks |

### Methods
| Method | Returns | Description |
|--------|---------|-------------|
| display(question, format) | None | Show question in specified format |
| clear() | None | Clear panel |
| get_format() | str | Current display format |

### Events
| Event | Callback | Description |
|-------|----------|-------------|
| edit_click | on_edit(question_id) | Edit button clicked |
| delete_click | on_delete(question_id) | Delete button clicked |
| format_change | on_format_change(format) | Format switcher changed |

---

## Format Switcher

### Purpose
Toggle between view formats for question display.

### Options
| Option | Label | Icon |
|--------|-------|------|
| formatted | Formatted | 📝 |
| json | JSON | { } |
| markdown | Markdown | 📋 |

### Methods
| Method | Returns | Description |
|--------|---------|-------------|
| get_format() | str | Current selected format |
| set_format(format) | None | Set display format |

---

## Confirmation Dialog

### Purpose
Confirm destructive operations (delete).

### Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| title | str | Dialog title |
| message | str | Confirmation message |
| confirm_text | str | Confirm button label |
| cancel_text | str | Cancel button label |

### Returns
| Result | Description |
|--------|-------------|
| True | User confirmed |
| False | User cancelled |

### Methods
| Method | Returns | Description |
|--------|---------|-------------|
| show() | bool | Display dialog and get result |

---

## Status Bar

### Purpose
Display connection status and operation results.

### Sections
| Section | Content |
|---------|---------|
| Connection | Connected/Disconnected indicator |
| Operation | Last operation result |
| Count | Question count |

### Methods
| Method | Returns | Description |
|--------|---------|-------------|
| set_status(message) | None | Show status message |
| set_connection(connected) | None | Update connection indicator |
| set_count(count) | None | Update question count |

---

## Settings Dialog

### Purpose
Configure MCP server connection.

### Fields
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| server_command | str | "python" | Command to run server |
| server_args | str | "-m mcp_test_questions.server" | Server arguments |
| working_dir | str | "" | Optional working directory |
| auto_connect | bool | True | Connect on startup |

### Methods
| Method | Returns | Description |
|--------|---------|-------------|
| show() | bool | Display dialog, returns True if saved |
| get_config() | ConnectionConfig | Get current config |
| test_connection() | bool | Test connection with current settings |

### Events
| Event | Callback | Description |
|-------|----------|-------------|
| save | on_save(config) | Save button clicked |
| test | on_test() | Test connection button clicked |
| cancel | on_cancel() | Cancel button clicked |