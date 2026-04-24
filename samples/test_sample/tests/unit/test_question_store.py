"""Unit tests for QuestionStore."""

from datetime import datetime
from pathlib import Path

import pytest

from mcp_test_questions.models.question import Question
from mcp_test_questions.storage.question_store import (
    NotFoundError,
    QuestionStore,
    StoreEmptyError,
)


class TestQuestionStore:
    """Test QuestionStore CRUD operations."""

    def test_create_question(self, question_store: QuestionStore) -> None:
        """Test creating a new question."""
        question = question_store.create(
            question_text="What is 2+2?",
            answer_options=["3", "4", "5", "6"],
            correct_answer="4",
        )
        assert question.id
        assert question.question_text == "What is 2+2?"
        assert question.correct_answer == "4"

    def test_create_generates_unique_ids(self, question_store: QuestionStore) -> None:
        """Test that create generates unique IDs."""
        q1 = question_store.create(
            question_text="Q1?",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        q2 = question_store.create(
            question_text="Q2?",
            answer_options=["C", "D"],
            correct_answer="C",
        )
        assert q1.id != q2.id

    def test_create_sets_timestamps(self, question_store: QuestionStore) -> None:
        """Test that create sets created_at and updated_at."""
        before = datetime.utcnow()
        question = question_store.create(
            question_text="Q?",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        after = datetime.utcnow()
        assert before <= question.created_at <= after
        assert before <= question.updated_at <= after

    def test_get_question_by_id(self, populated_store: QuestionStore) -> None:
        """Test retrieving a question by ID."""
        all_questions = populated_store.get_all()
        first_question = all_questions[0]
        retrieved = populated_store.get(first_question.id)
        assert retrieved is not None
        assert retrieved.id == first_question.id
        assert retrieved.question_text == first_question.question_text

    def test_get_nonexistent_returns_none(self, question_store: QuestionStore) -> None:
        """Test that getting nonexistent ID returns None."""
        result = question_store.get("nonexistent-id")
        assert result is None

    def test_get_random_question(self, populated_store: QuestionStore) -> None:
        """Test getting a random question."""
        question = populated_store.get_random()
        assert question is not None
        assert isinstance(question, Question)

    def test_get_random_on_empty_store_raises(self, question_store: QuestionStore) -> None:
        """Test that get_random on empty store raises StoreEmptyError."""
        with pytest.raises(StoreEmptyError):
            question_store.get_random()

    def test_update_question_text(self, populated_store: QuestionStore) -> None:
        """Test updating question text."""
        import time

        question = populated_store.create(
            question_text="Original",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        original_updated_at = question.updated_at
        time.sleep(0.001)

        updated = populated_store.update(question.id, question_text="Updated")
        assert updated.question_text == "Updated"
        assert updated.answer_options == question.answer_options
        assert updated.updated_at >= original_updated_at

    def test_update_question_options(self, populated_store: QuestionStore) -> None:
        """Test updating answer options."""
        question = populated_store.create(
            question_text="Q?",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        updated = populated_store.update(
            question.id, answer_options=["X", "Y"], correct_answer="X"
        )
        assert updated.answer_options == ["X", "Y"]
        assert updated.correct_answer == "X"

    def test_update_correct_answer_only(self, populated_store: QuestionStore) -> None:
        """Test updating only correct answer."""
        question = populated_store.create(
            question_text="Q?",
            answer_options=["A", "B", "C"],
            correct_answer="A",
        )
        updated = populated_store.update(question.id, correct_answer="B")
        assert updated.correct_answer == "B"
        assert updated.answer_options == ["A", "B", "C"]

    def test_update_nonexistent_raises(self, question_store: QuestionStore) -> None:
        """Test that updating nonexistent ID raises NotFoundError."""
        with pytest.raises(NotFoundError):
            question_store.update("nonexistent-id", question_text="New")

    def test_update_invalid_correct_answer_raises(
        self, populated_store: QuestionStore
    ) -> None:
        """Test that setting correct_answer not in options raises error."""
        question = populated_store.create(
            question_text="Q?",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        with pytest.raises(ValueError, match="must be in"):
            populated_store.update(question.id, correct_answer="Z")

    def test_delete_question(self, populated_store: QuestionStore) -> None:
        """Test deleting a question."""
        question = populated_store.create(
            question_text="To delete",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        populated_store.delete(question.id)
        assert populated_store.get(question.id) is None

    def test_delete_nonexistent_raises(self, question_store: QuestionStore) -> None:
        """Test that deleting nonexistent ID raises NotFoundError."""
        with pytest.raises(NotFoundError):
            question_store.delete("nonexistent-id")

    def test_persistence_to_file(
        self, temp_questions_file: Path, question_store: QuestionStore
    ) -> None:
        """Test that questions persist to file."""
        question_store.create(
            question_text="Persistent?",
            answer_options=["Yes", "No"],
            correct_answer="Yes",
        )
        assert temp_questions_file.exists()

        new_store = QuestionStore(file_path=temp_questions_file)
        all_questions = new_store.get_all()
        assert len(all_questions) == 1
        assert all_questions[0].question_text == "Persistent?"

    def test_get_all(self, populated_store: QuestionStore) -> None:
        """Test getting all questions."""
        all_questions = populated_store.get_all()
        assert len(all_questions) == 3

    def test_count(self, populated_store: QuestionStore) -> None:
        """Test counting questions."""
        assert populated_store.count() == 3