"""Integration tests for MCP tools."""

import json
import pytest

from mcp_test_questions.storage.question_store import QuestionStore


class TestCreateQuestionIntegration:
    """Integration tests for create_question tool."""

    def test_create_question_success(self, question_store: QuestionStore) -> None:
        """Test successful question creation."""
        result = question_store.create(
            question_text="What is 2+2?",
            answer_options=["3", "4", "5", "6"],
            correct_answer="4",
        )
        assert result.id
        assert result.question_text == "What is 2+2?"
        assert result.correct_answer == "4"

    def test_create_question_persists(self, question_store: QuestionStore) -> None:
        """Test that created question persists and can be retrieved."""
        created = question_store.create(
            question_text="Test persistence",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        retrieved = question_store.get(created.id)
        assert retrieved is not None
        assert retrieved.question_text == "Test persistence"


class TestGetQuestionIntegration:
    """Integration tests for get_question tool."""

    def test_get_question_by_id(self, populated_store: QuestionStore) -> None:
        """Test getting question by ID."""
        all_questions = populated_store.get_all()
        first = all_questions[0]
        result = populated_store.get(first.id)
        assert result is not None
        assert result.id == first.id

    def test_get_random_question(self, populated_store: QuestionStore) -> None:
        """Test getting random question."""
        result = populated_store.get_random()
        assert result is not None
        assert result.id in [q.id for q in populated_store.get_all()]

    def test_get_nonexistent_returns_none(self, question_store: QuestionStore) -> None:
        """Test that nonexistent ID returns None."""
        result = question_store.get("nonexistent-id")
        assert result is None


class TestUpdateQuestionIntegration:
    """Integration tests for update_question tool."""

    def test_update_question_text(self, populated_store: QuestionStore) -> None:
        """Test updating question text."""
        question = populated_store.create(
            question_text="Original",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        updated = populated_store.update(question.id, question_text="Updated")
        assert updated.question_text == "Updated"
        assert updated.answer_options == ["A", "B"]

    def test_update_options_with_correct_answer(
        self, populated_store: QuestionStore
    ) -> None:
        """Test updating options when correct_answer is provided."""
        question = populated_store.create(
            question_text="Test?",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        updated = populated_store.update(
            question.id, answer_options=["X", "Y"], correct_answer="Y"
        )
        assert updated.answer_options == ["X", "Y"]
        assert updated.correct_answer == "Y"


class TestDeleteQuestionIntegration:
    """Integration tests for delete_question tool."""

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
        """Test deleting nonexistent raises error."""
        from mcp_test_questions.storage.question_store import NotFoundError

        with pytest.raises(NotFoundError):
            question_store.delete("nonexistent-id")


class TestResourceIntegration:
    """Integration tests for question resources."""

    def test_question_to_json(self, question_store: QuestionStore) -> None:
        """Test question JSON serialization."""
        question = question_store.create(
            question_text="Test?",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        data = question.model_dump(mode="json")
        assert isinstance(data, dict)
        assert "id" in data

    def test_question_to_markdown(self, question_store: QuestionStore) -> None:
        """Test question Markdown conversion."""
        question = question_store.create(
            question_text="What is 2+2?",
            answer_options=["3", "4", "5", "6"],
            correct_answer="4",
        )
        markdown = question.to_markdown()
        assert "What is 2+2?" in markdown
        assert "## Answer Options" in markdown
        assert "4" in markdown

    def test_full_crud_workflow(self, question_store: QuestionStore) -> None:
        """Test complete CRUD workflow."""
        question = question_store.create(
            question_text="Original question",
            answer_options=["A", "B", "C"],
            correct_answer="A",
        )

        retrieved = question_store.get(question.id)
        assert retrieved is not None
        assert retrieved.question_text == "Original question"

        updated = question_store.update(question.id, question_text="Updated question")
        assert updated.question_text == "Updated question"

        all_questions = question_store.get_all()
        assert any(q.id == question.id for q in all_questions)

        question_store.delete(question.id)
        assert question_store.get(question.id) is None