# Data Model: MCP Test Questions Server

**Feature**: 001-mcp-test-questions
**Date**: 2026-04-22

## Entities

### Question

Core entity representing a multiple-choice test question.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | str | UUID format, auto-generated, immutable | Unique identifier |
| question_text | str | Required, 1-2000 chars | The question prompt |
| answer_options | list[str] | Required, 2-10 items, each 1-500 chars | List of possible answers |
| correct_answer | str | Required, must exist in answer_options | The correct answer |
| created_at | datetime | Auto-generated, immutable | Creation timestamp |
| updated_at | datetime | Auto-updated on modification | Last modification timestamp |

**Identity Rules**:
- ID is UUID v4 generated on creation
- IDs are immutable and never reused
- No natural key alternative (UUID provides uniqueness)

**State Transitions**:
```
[Doesn't Exist] --create--> [Active]
[Active] --update--> [Active] (fields modified)
[Active] --delete--> [Deleted] (removed from store)
```

**Validation Rules**:
- VR-001: `question_text` cannot be empty
- VR-002: `answer_options` must contain at least 2 items
- VR-003: `answer_options` must contain at most 10 items
- VR-004: `correct_answer` must exist in `answer_options`
- VR-005: No duplicate options in `answer_options`

### QuestionStore

Storage abstraction managing question persistence.

**Responsibilities**:
- Add, retrieve, update, delete questions
- Random question selection
- Persist to JSON file on changes
- Load from JSON file on initialization

**Invariants**:
- All questions stored are valid (validated before storage)
- IDs are unique within the store
- Random selection uniformly distributed

## Relationships

No relationships between entities - Questions are standalone.

```
┌─────────────┐
│   Question  │
├─────────────┤
│ id          │
│ question_   │
│   text      │
│ answer_     │
│   options   │
│ correct_    │
│   answer    │
│ created_at  │
│ updated_at  │
└─────────────┘
       │
       │ managed by
       ▼
┌─────────────┐
│ QuestionStore│
├─────────────┤
│ questions:  │
│   dict      │
│ file_path:  │
│   Path      │
└─────────────┘
```

## Data Volume Assumptions

- **Typical**: 50-200 questions
- **Maximum**: 1000 questions (can be increased with migration to database)
- **Question text**: Average 100 characters
- **Options per question**: 4 options
- **Total storage**: ~500KB for 1000 questions

## Persistence Format

JSON file structure:

```json
{
  "version": "1.0",
  "questions": {
    "uuid-1": {
      "id": "uuid-1",
      "question_text": "What is 2+2?",
      "answer_options": ["3", "4", "5", "6"],
      "correct_answer": "4",
      "created_at": "2026-04-22T10:00:00Z",
      "updated_at": "2026-04-22T10:00:00Z"
    }
  }
}
```

**Migration Path**: Schema version field supports future migrations.