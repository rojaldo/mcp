# Quickstart: MCP GUI Client

**Feature**: 002-mcp-gui-client
**Date**: 2026-04-22

## Prerequisites

- Python 3.11 or higher
- MCP Test Questions Server (feature 001-mcp-test-questions) running
- tkinter (usually included with Python)

## Installation

```bash
# Clone and navigate to project
cd /path/to/test_sample

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

## Running the Application

```bash
# Start the GUI client
python -m mcp_gui_client.main
```

On first run, the settings dialog will appear to configure the MCP server connection.

## Configuration

Default configuration file: `~/.mcp_gui_client/config.json`

```json
{
  "server_command": "python",
  "server_args": ["-m", "mcp_test_questions.server"],
  "working_directory": "/path/to/test_sample",
  "auto_connect": true
}
```

## Basic Usage

### Creating a Question

1. Click **New Question** button in toolbar
2. Fill in question text
3. Add at least 2 answer options
4. Select the correct answer from the dropdown
5. Click **Create** button
6. Question appears in the list with success message

### Browsing Questions

1. Questions appear in the left panel list
2. Click a question to view details in right panel
3. Use **Refresh** button to reload from server
4. Use **Random** button to get a random question

### Editing a Question

1. Select question from list
2. Click **Edit** button in detail panel
3. Modify fields in the form
4. Click **Save** to update
5. List refreshes with changes

### Deleting a Question

1. Select question from list
2. Click **Delete** button in detail panel
3. Confirm deletion in dialog
4. Question is removed from list

### Switching View Formats

1. Select a question to view
2. Use **Format Switcher** dropdown in detail panel
3. Choose from:
   - **Formatted**: User-friendly card display
   - **JSON**: Raw data with syntax highlighting
   - **Markdown**: Formatted text with checkmarks

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/mcp_gui_client --cov-report=term-missing

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
```

### Code Quality

```bash
# Linting
ruff check src/

# Type checking
mypy src/

# Format code
ruff format src/
```

## Troubleshooting

### Connection Failed
- Ensure MCP server is running: `python -m mcp_test_questions.server`
- Check server command and arguments in settings
- Verify working directory in settings

### Empty Question List
- Server may have no questions yet
- Click **Refresh** to reload
- Check status bar for errors

### UI Not Responding
- Server may be slow or unresponsive
- Check status bar for connection status
- Restart the application

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New Question |
| Ctrl+R | Refresh List |
| Ctrl+S | Save (in edit mode) |
| Delete | Delete selected question |
| Escape | Cancel / Close dialog |