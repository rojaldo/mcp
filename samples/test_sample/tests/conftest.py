"""Pytest fixtures for MCP Test Questions Server and GUI Client tests."""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Generator

import pytest

from mcp_test_questions.models.question import Question
from mcp_test_questions.storage.question_store import QuestionStore


@pytest.fixture
def sample_question_data() -> dict[str, str | list[str]]:
    """Sample question data for testing."""
    return {
        "question_text": "What is 2+2?",
        "answer_options": ["3", "4", "5", "6"],
        "correct_answer": "4",
    }


@pytest.fixture
def sample_question(sample_question_data: dict[str, str | list[str]]) -> Question:
    """Sample Question instance for testing."""
    return Question(
        id=str(uuid.uuid4()),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        **sample_question_data,
    )


@pytest.fixture
def temp_questions_file(tmp_path: Path) -> Path:
    """Temporary questions.json file for testing."""
    return tmp_path / "questions.json"


@pytest.fixture
def question_store(temp_questions_file: Path) -> Generator[QuestionStore, None, None]:
    """QuestionStore instance with temporary file storage."""
    store = QuestionStore(file_path=temp_questions_file)
    yield store
    if temp_questions_file.exists():
        temp_questions_file.unlink()


@pytest.fixture
def populated_store(
    question_store: QuestionStore, sample_question_data: dict[str, str | list[str]]
) -> QuestionStore:
    """QuestionStore pre-populated with sample questions."""
    question_store.create(
        question_text="What is 2+2?",
        answer_options=["3", "4", "5", "6"],
        correct_answer="4",
    )
    question_store.create(
        question_text="What is the capital of France?",
        answer_options=["London", "Paris", "Berlin", "Madrid"],
        correct_answer="Paris",
    )
    question_store.create(
        question_text="What is 7 x 8?",
        answer_options=["54", "56", "58", "64"],
        correct_answer="56",
    )
    return question_store


@pytest.fixture
def sample_question_dict() -> dict[str, object]:
    """Sample question as dictionary for GUI tests."""
    return {
        "id": str(uuid.uuid4()),
        "question_text": "What is 2+2?",
        "answer_options": ["3", "4", "5", "6"],
        "correct_answer": "4",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }


@pytest.fixture
def sample_questions_list(sample_question_dict: dict[str, object]) -> list[dict[str, object]]:
    """List of sample questions for GUI list view tests."""
    questions = [sample_question_dict]
    for i in range(3):
        q = sample_question_dict.copy()
        q["id"] = str(uuid.uuid4())
        q["question_text"] = f"Question {i + 2}?"
        questions.append(q)
    return questions


@pytest.fixture
def mock_mcp_response(sample_question_dict: dict[str, object]) -> dict[str, object]:
    """Mock MCP tool response for create_question."""
    return {
        "content": [
            {"type": "text", "text": f"Created question with ID: {sample_question_dict['id']}"}
        ]
    }


@pytest.fixture
def mock_mcp_get_response(sample_question_dict: dict[str, object]) -> dict[str, object]:
    """Mock MCP tool response for get_question."""
    import json
    return {
        "content": [
            {"type": "text", "text": json.dumps(sample_question_dict)}
        ]
    }


@pytest.fixture
def mock_mcp_list_response(sample_questions_list: list[dict[str, object]]) -> dict[str, object]:
    """Mock MCP tool response for list_questions."""
    import json
    return {
        "content": [
            {"type": "text", "text": json.dumps(sample_questions_list)}
        ]
    }