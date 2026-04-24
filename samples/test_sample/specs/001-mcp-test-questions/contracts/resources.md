# MCP Resources Contract

**Feature**: 001-mcp-test-questions
**Date**: 2026-04-22

This document defines the MCP resources exposed by the Test Questions Server.

## Resource: Question

Access individual questions via URI pattern.

### URI Template

```
question://{id}
```

Where `{id}` is the UUID of the question.

### Supported Formats

| MIME Type | Description |
|-----------|-------------|
| application/json | JSON representation of question |
| text/markdown | Human-readable Markdown format |

### JSON Format

Request: `Accept: application/json`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "question_text": "What is the capital of France?",
  "answer_options": ["London", "Paris", "Berlin", "Madrid"],
  "correct_answer": "Paris",
  "created_at": "2026-04-22T10:00:00Z",
  "updated_at": "2026-04-22T10:00:00Z"
}
```

### Markdown Format

Request: `Accept: text/markdown`

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

### Error Response

When requesting a non-existent question:

```json
{
  "error": {
    "code": "NotFound",
    "message": "Question resource not found: question://invalid-uuid"
  }
}
```

---

## Resource Template Registration

FastMCP resource template registration pattern:

```python
@mcp.resource("question://{question_id}")
async def get_question_resource(question_id: str) -> str:
    """Returns question data as JSON or Markdown based on accept header."""
    ...
```

---

## Resource Discovery

Clients can discover available questions by:

1. Creating questions via `create_question` tool (returns ID)
2. Getting random question via `get_question` tool (returns ID)
3. Constructing URIs from known IDs

Note: No list-all resource is provided initially to keep scope minimal. Questions are discovered through tool operations.