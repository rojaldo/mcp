# Data Model: MCP GUI Client

**Feature**: 002-mcp-gui-client
**Date**: 2026-04-22

## Entities

### Question (from MCP Server)

The GUI client displays questions from the MCP server. Structure matches server contracts.

| Field | Type | Description |
|-------|------|-------------|
| id | str | UUID from server |
| question_text | str | Question prompt |
| answer_options | list[str] | Answer choices |
| correct_answer | str | Correct option |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Modification timestamp |

**Note**: Questions are not stored locally - fetched from server on demand.

### ConnectionConfig

Local configuration for MCP server connection.

| Field | Type | Description |
|-------|------|-------------|
| server_command | str | Command to start MCP server |
| server_args | list[str] | Arguments for server command |
| working_directory | str | Optional working directory |
| auto_connect | bool | Connect on startup |

**Storage Location**: `~/.mcp_gui_client/config.json`

**Default Values**:
- `server_command`: "python"
- `server_args`: ["-m", "mcp_test_questions.server"]
- `auto_connect`: True

### AppState

Runtime application state.

| Field | Type | Description |
|-------|------|-------------|
| connected | bool | Connection status |
| selected_question_id | str \| None | Currently selected question |
| view_format | str | Current view format (formatted/json/markdown) |
| questions_cache | dict[str, Question] | Cached questions for list |

**State Transitions**:
```
[Disconnected] --connect--> [Connected]
[Connected] --disconnect--> [Disconnected]
[Connected] --select_question--> [Question_Selected]
[Question_Selected] --deselect--> [Connected]
```

## GUI Component State

### ListPanel State

| State | Description |
|-------|-------------|
| Empty | No questions loaded |
| Loading | Fetching questions from server |
| Populated | Questions displayed in list |
| Error | Failed to load questions |

### FormPanel State

| State | Description |
|-------|-------------|
| Empty | New question form, all fields blank |
| Editing | Pre-populated with existing question |
| Validating | Client-side validation in progress |
| Submitting | Sending to server |
| Success | Question created/updated |
| Error | Validation or server error |

### DetailPanel State

| State | Description |
|-------|-------------|
| Empty | No question selected |
| Loading | Fetching question details |
| Displaying | Question shown in selected format |
| Error | Failed to load question |

## Relationships

```
┌─────────────────┐
│ ConnectionConfig│
├─────────────────┤
│ server_command  │
│ server_args     │
│ auto_connect    │
└─────────────────┘
        │
        │ used by
        ▼
┌─────────────────┐
│   AppState      │
├─────────────────┤
│ connected       │
│ questions_cache │◄─── cache of
│ view_format     │        │
└─────────────────┘        │
        │                   │
        │                   ▼
        │          ┌─────────────────┐
        │          │    Question      │
        │          ├─────────────────┤
        │          │ id              │
        │          │ question_text   │
        │          │ answer_options  │
        │          │ correct_answer  │
        │          └─────────────────┘
        │
        │ controls
        ▼
┌─────────────────────────────────────┐
│         GUI Components               │
├─────────────────────────────────────┤
│ ListPanel (browse questions)        │
│ FormPanel (create/edit)             │
│ DetailPanel (view formats)          │
│ SettingsDialog (config connection)  │
└─────────────────────────────────────┘
```

## Data Flow

### Create Question Flow

```
User Input → FormPanel.validate() → FormPanel.get_data()
    → MCPClient.create_question() → Server Response
    → AppState.questions_cache.update() → ListPanel.refresh()
```

### View Question Flow

```
ListPanel.selection → AppState.selected_question_id
    → MCPClient.get_question(id) → Server Response
    → DetailPanel.display(format=view_format)
```

### Update Question Flow

```
DetailPanel.edit_click → FormPanel.populate(question)
    → User edits → FormPanel.validate() → FormPanel.get_data()
    → MCPClient.update_question(id, data) → Server Response
    → AppState.questions_cache.update() → ListPanel.refresh()
```

## Persistence

Only configuration is persisted locally:
- Connection settings stored in JSON file
- Questions fetched from server each session
- No local question storage (server is source of truth)