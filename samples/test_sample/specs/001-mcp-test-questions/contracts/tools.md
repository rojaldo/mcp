# MCP Tools Contract

**Feature**: 001-mcp-test-questions
**Date**: 2026-04-22

This document defines the MCP tools exposed by the Test Questions Server.

## Tool: create_question

Creates a new multiple-choice question.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| question_text | string | Yes | The text of the question |
| answer_options | array[string] | Yes | List of answer options (2-10 items) |
| correct_answer | string | Yes | The correct answer (must be in answer_options) |

### Returns

```json
{
  "id": "uuid-string",
  "question_text": "What is 2+2?",
  "answer_options": ["3", "4", "5", "6"],
  "correct_answer": "4",
  "created_at": "2026-04-22T10:00:00Z",
  "updated_at": "2026-04-22T10:00:00Z"
}
```

### Errors

| Code | Condition |
|------|-----------|
| InvalidParams | Fewer than 2 answer options |
| InvalidParams | correct_answer not in answer_options |
| InvalidParams | question_text empty |
| InvalidParams | More than 10 answer options |
| InvalidParams | Duplicate options in answer_options |

---

## Tool: get_question

Retrieves a question by ID or returns a random question.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| question_id | string | No | The question ID to retrieve. If omitted, returns random question. |

### Returns

```json
{
  "id": "uuid-string",
  "question_text": "What is 2+2?",
  "answer_options": ["3", "4", "5", "6"],
  "correct_answer": "4",
  "created_at": "2026-04-22T10:00:00Z",
  "updated_at": "2026-04-22T10:00:00Z"
}
```

### Errors

| Code | Condition |
|------|-----------|
| NotFound | question_id provided but question doesn't exist |
| Internal | No questions exist when requesting random |

---

## Tool: update_question

Updates an existing question. All fields are optional - only provided fields are updated.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| question_id | string | Yes | The question ID to update |
| question_text | string | No | New question text |
| answer_options | array[string] | No | New answer options |
| correct_answer | string | No | New correct answer |

### Returns

```json
{
  "id": "uuid-string",
  "question_text": "Updated question text?",
  "answer_options": ["A", "B", "C"],
  "correct_answer": "B",
  "created_at": "2026-04-22T10:00:00Z",
  "updated_at": "2026-04-22T11:00:00Z"
}
```

### Errors

| Code | Condition |
|------|-----------|
| NotFound | question_id doesn't exist |
| InvalidParams | correct_answer provided but not in existing or new answer_options |
| InvalidParams | answer_options provided with fewer than 2 items |
| InvalidParams | No fields provided to update |

### Notes

- If `answer_options` is updated, `correct_answer` must still be valid in the new options
- `correct_answer` validated against merged options if both provided
- `updated_at` timestamp auto-updated

---

## Tool: delete_question

Deletes a question by ID.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| question_id | string | Yes | The question ID to delete |

### Returns

```json
{
  "success": true,
  "deleted_id": "uuid-string"
}
```

### Errors

| Code | Condition |
|------|-----------|
| NotFound | question_id doesn't exist |

---

## Common Patterns

### Input Validation

All tools validate inputs using Pydantic models before processing:

```python
class CreateQuestionInput(BaseModel):
    question_text: str = Field(min_length=1, max_length=2000)
    answer_options: list[str] = Field(min_length=2, max_length=10)
    correct_answer: str
```

### Error Response Format

```json
{
  "error": {
    "code": "NotFound",
    "message": "Question with id 'uuid-string' not found"
  }
}
```

### Success Response Format

All successful responses include the complete affected resource(s).