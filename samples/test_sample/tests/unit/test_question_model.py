"""Unit tests for Question model."""

import uuid
from datetime import datetime

import pytest
from pydantic import ValidationError

from mcp_test_questions.models.question import Question


class TestQuestionModel:
    """Test Question Pydantic model validation."""

    def test_create_valid_question(self) -> None:
        """Test creating a valid question."""
        question = Question(
            id=str(uuid.uuid4()),
            question_text="What is 2+2?",
            answer_options=["3", "4", "5", "6"],
            correct_answer="4",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        assert question.question_text == "What is 2+2?"
        assert len(question.answer_options) == 4
        assert question.correct_answer == "4"

    def test_question_id_is_uuid_string(self) -> None:
        """Test that question ID is a valid UUID string."""
        question = Question(
            id=str(uuid.uuid4()),
            question_text="Test?",
            answer_options=["A", "B"],
            correct_answer="A",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        uuid.UUID(question.id)

    def test_empty_question_text_fails(self) -> None:
        """Test that empty question text is rejected."""
        with pytest.raises(ValidationError):
            Question(
                id=str(uuid.uuid4()),
                question_text="",
                answer_options=["A", "B"],
                correct_answer="A",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

    def test_too_long_question_text_fails(self) -> None:
        """Test that question text over 2000 chars is rejected."""
        with pytest.raises(ValidationError):
            Question(
                id=str(uuid.uuid4()),
                question_text="x" * 2001,
                answer_options=["A", "B"],
                correct_answer="A",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

    def test_minimum_two_options_required(self) -> None:
        """Test that fewer than 2 answer options is rejected."""
        with pytest.raises(ValidationError):
            Question(
                id=str(uuid.uuid4()),
                question_text="Test?",
                answer_options=["A"],
                correct_answer="A",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

    def test_maximum_ten_options_allowed(self) -> None:
        """Test that more than 10 answer options is rejected."""
        options = [str(i) for i in range(11)]
        with pytest.raises(ValidationError):
            Question(
                id=str(uuid.uuid4()),
                question_text="Test?",
                answer_options=options,
                correct_answer="0",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

    def test_correct_answer_not_in_options_fails(self) -> None:
        """Test that correct_answer must be in answer_options."""
        with pytest.raises(ValidationError, match="must be in answer_options"):
            Question(
                id=str(uuid.uuid4()),
                question_text="Test?",
                answer_options=["A", "B"],
                correct_answer="C",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

    def test_duplicate_options_rejected(self) -> None:
        """Test that duplicate options are rejected."""
        with pytest.raises(ValidationError, match="duplicate"):
            Question(
                id=str(uuid.uuid4()),
                question_text="Test?",
                answer_options=["A", "A", "B"],
                correct_answer="A",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

    def test_option_too_long_rejected(self) -> None:
        """Test that options over 500 chars are rejected."""
        long_option = "x" * 501
        with pytest.raises(ValidationError):
            Question(
                id=str(uuid.uuid4()),
                question_text="Test?",
                answer_options=[long_option, "B"],
                correct_answer=long_option,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

    def test_model_serialization(self) -> None:
        """Test that Question can be serialized to dict/JSON."""
        question = Question(
            id=str(uuid.uuid4()),
            question_text="Test?",
            answer_options=["A", "B"],
            correct_answer="A",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        data = question.model_dump()
        assert isinstance(data, dict)
        assert "id" in data
        assert "question_text" in data
        assert data["correct_answer"] == "A"

    def test_model_deserialization(self) -> None:
        """Test that Question can be created from dict."""
        data = {
            "id": str(uuid.uuid4()),
            "question_text": "Test?",
            "answer_options": ["A", "B"],
            "correct_answer": "A",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        question = Question.model_validate(data)
        assert question.question_text == "Test?"