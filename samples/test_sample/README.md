# MCP Test Questions Server

An MCP (Model Context Protocol) server for managing multiple-choice test questions. This server provides CRUD operations via MCP tools and exposes questions as resources with JSON and Markdown formats.

## Features

- **Create questions**: Add multiple-choice questions with correct answer marking
- **Retrieve questions**: Get questions by ID or get a random question
- **Update questions**: Partial updates to question text, options, or correct answer
- **Delete questions**: Remove questions from the store
- **Resource access**: Access questions via MCP resource URIs with JSON/Markdown formats

## Installation

```bash
# Clone the repository
git clone https://github.com/rojaldo/mcp.git
cd samples/test_sample

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

## Usage

### Running the Server

```bash
python -m mcp_test_questions.server
```

The server communicates via stdio - it reads JSON-RPC messages from stdin and writes responses to stdout.

### Claude Desktop Configuration

Add to your Claude Desktop config:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "test-questions": {
      "command": "python",
      "args": ["-m", "mcp_test_questions.server"],
      "cwd": "/path/to/test_sample"
    }
  }
}
```

## MCP Tools

### create_question

Create a new multiple-choice question.

```json
{
  "question_text": "What is 2+2?",
  "answer_options": ["3", "4", "5", "6"],
  "correct_answer": "4"
}
```

Returns the created question with generated ID and timestamps.

### get_question

Retrieve a question by ID or get a random question.

```json
{
  "question_id": "optional-uuid"
}
```

If `question_id` is omitted, returns a random question.

### update_question

Update an existing question. All fields are optional.

```json
{
  "question_id": "uuid",
  "question_text": "Updated question text?",
  "answer_options": ["A", "B", "C"],
  "correct_answer": "B"
}
```

### delete_question

Delete a question by ID.

```json
{
  "question_id": "uuid"
}
```

## MCP Resources

Questions can be accessed as resources with the URI pattern `question://{id}`:

- **JSON format**: `Accept: application/json`
- **Markdown format**: `Accept: text/markdown`

Example resource content (Markdown):

```markdown
# Question: 550e8400-e29b-41d4-a716-446655440000

## Question

What is the capital of France?

## Answer Options

1. London
2. Paris ✓
3. Berlin
4. Madrid

## Metadata

- **Created**: 2026-04-22T10:00:00Z
- **Last Updated**: 2026-04-22T10:00:00Z
```

## Development

### Running Tests

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

### Code Quality

```bash
# Linting
ruff check src/

# Type checking
mypy src/

# Format code
ruff format src/
```

## Data Persistence

Questions are automatically saved to `questions.json` in the working directory. To use a custom location:

```bash
export QUESTIONS_FILE=/path/to/questions.json
python -m mcp_test_questions.server
```

## License

MIT License