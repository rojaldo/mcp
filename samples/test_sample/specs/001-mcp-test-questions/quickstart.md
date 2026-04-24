# Quickstart: MCP Test Questions Server

**Feature**: 001-mcp-test-questions
**Date**: 2026-04-22

## Prerequisites

- Python 3.11 or higher
- pip package manager
- MCP client (e.g., Claude Desktop, or MCP inspector tool)

## Installation

```bash
# Clone and navigate to project
cd /path/to/mcp-test-questions

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Running the Server

```bash
# Run MCP server via stdio
python -m mcp_test_questions.server
```

The server communicates via stdio - it reads JSON-RPC messages from stdin and writes responses to stdout.

## Configuration for Claude Desktop

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "test-questions": {
      "command": "python",
      "args": ["-m", "mcp_test_questions.server"],
      "cwd": "/path/to/mcp-test-questions"
    }
  }
}
```

## Basic Usage Examples

### Creating a Question

In Claude Desktop or MCP client:

```
Use the create_question tool to create a math question:
- Question: "What is 7 x 8?"
- Options: ["54", "56", "58", "64"]
- Correct answer: "56"
```

Expected response:
```json
{
  "id": "generated-uuid",
  "question_text": "What is 7 x 8?",
  "answer_options": ["54", "56", "58", "64"],
  "correct_answer": "56"
}
```

### Retrieving a Question

```
Use get_question to retrieve the question with id "generated-uuid"
```

Or for a random question:
```
Use get_question without an id to get a random question
```

### Updating a Question

```
Use update_question to fix the question "generated-uuid":
- Change correct_answer to "56" (it was wrong before)
```

### Deleting a Question

```
Use delete_question to remove question "generated-uuid"
```

### Accessing via Resource URI

```
Read the resource at question://generated-uuid
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/mcp_test_questions --cov-report=term-missing

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/contract/
```

## Development Workflow

1. **Make changes** to source code
2. **Run linting**: `ruff check src/`
3. **Run type check**: `mypy src/`
4. **Run tests**: `pytest`
5. **Commit** when all checks pass

## Data Persistence

Questions are automatically saved to `questions.json` in the working directory. To use a different location:

```bash
export QUESTIONS_FILE=/path/to/questions.json
python -m mcp_test_questions.server
```

## Troubleshooting

### Server won't start
- Check Python version: `python --version` (need 3.11+)
- Verify dependencies: `pip list | grep fastmcp`

### Tools not appearing in Claude Desktop
- Check config file syntax
- Verify paths are absolute
- Restart Claude Desktop after config changes

### Questions not persisting
- Check file permissions in working directory
- Verify `QUESTIONS_FILE` path if using custom location