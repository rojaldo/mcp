"""Contract tests for MCP tools and resources."""

import pytest

from mcp_test_questions.models.question import Question
from mcp_test_questions.storage.question_store import QuestionStore


class TestCreateQuestionContract:
    """Contract tests for create_question tool."""

    def test_create_question_returns_valid_question(self, question_store: QuestionStore) -> None:
        """Create question returns a valid Question with all fields."""
        result = question_store.create(
            question_text="What is 2+2?",
            answer_options=["3", "4", "5", "6"],
            correct_answer="4",
        )
        assert isinstance(result, Question)
        assert result.id
        assert result.question_text == "What is 2+2?"
        assert result.answer_options == ["3", "4", "5", "6"]
        assert result.correct_answer == "4"
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_create_question_rejects_empty_text(self, question_store: QuestionStore) -> None:
        """Create question rejects empty question_text."""
        with pytest.raises(Exception):
            question_store.create(
                question_text="",
                answer_options=["A", "B"],
                correct_answer="A",
            )

    def test_create_question_rejects_too_few_options(self, question_store: QuestionStore) -> None:
        """Create question rejects fewer than 2 answer_options."""
        with pytest.raises(Exception):
            question_store.create(
                question_text="Test?",
                answer_options=["A"],
                correct_answer="A",
            )

    def test_create_question_rejects_invalid_correct_answer(
        self, question_store: QuestionStore
    ) -> None:
        """Create question rejects correct_answer not in options."""
        with pytest.raises(Exception):
            question_store.create(
                question_text="Test?",
                answer_options=["A", "B"],
                correct_answer="C",
            )

    def test_create_question_rejects_duplicate_options(
        self, question_store: QuestionStore
    ) -> None:
        """Create question rejects duplicate answer options."""
        with pytest.raises(Exception):
            question_store.create(
                question_text="Test?",
                answer_options=["A", "A", "B"],
                correct_answer="A",
            )


class TestGetQuestionContract:
    """Contract tests for get_question tool."""

    def test_get_question_by_id_returns_exact_match(
        self, populated_store: QuestionStore
    ) -> None:
        """Get question by ID returns exact match."""
        all_questions = populated_store.get_all()
        first = all_questions[0]
        result = populated_store.get(first.id)
        assert result is not None
        assert result.id == first.id
        assert result.question_text == first.question_text

    def test_get_question_nonexistent_returns_none(
        self, question_store: QuestionStore
    ) -> None:
        """Get nonexistent ID returns None."""
        result = question_store.get("nonexistent-uuid")
        assert result is None

    def test_get_random_question(self, populated_store: QuestionStore) -> None:
        """Get random returns a valid question."""
        result = populated_store.get_random()
        assert isinstance(result, Question)
        assert result.id in [q.id for q in populated_store.get_all()]


class TestUpdateQuestionContract:
    """Contract tests for update_question tool."""

    def test_update_question_text_only(self, populated_store: QuestionStore) -> None:
        """Update can modify only question_text."""
        question = populated_store.create(
            question_text="Original",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        result = populated_store.update(question.id, question_text="Updated")
        assert result.question_text == "Updated"
        assert result.answer_options == ["A", "B"]
        assert result.correct_answer == "A"

    def test_update_options_requires_valid_correct_answer(
        self, populated_store: QuestionStore
    ) -> None:
        """Update options validates correct_answer is in new options."""
        question = populated_store.create(
            question_text="Test?",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        with pytest.raises(Exception):
            populated_store.update(question.id, answer_options=["C", "D"])

    def test_update_nonexistent_raises(self, question_store: QuestionStore) -> None:
        """Update nonexistent ID raises error."""
        with pytest.raises(Exception):
            question_store.update("nonexistent-id", question_text="New")


class TestDeleteQuestionContract:
    """Contract tests for delete_question tool."""

    def test_delete_question_removes_from_store(self, populated_store: QuestionStore) -> None:
        """Delete removes question from store."""
        question = populated_store.create(
            question_text="To delete",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        populated_store.delete(question.id)
        assert populated_store.get(question.id) is None

    def test_delete_nonexistent_raises(self, question_store: QuestionStore) -> None:
        """Delete nonexistent ID raises error."""
        with pytest.raises(Exception):
            question_store.delete("nonexistent-id")


class TestQuestionResourceContract:
    """Contract tests for question resource."""

    def test_question_to_json(self, question_store: QuestionStore) -> None:
        """Question serializes to JSON correctly."""
        question = question_store.create(
            question_text="Test?",
            answer_options=["A", "B"],
            correct_answer="A",
        )
        data = question.model_dump(mode="json")
        assert "id" in data
        assert "question_text" in data
        assert data["correct_answer"] == "A"

    def test_question_to_markdown(self, question_store: QuestionStore) -> None:
        """Question converts to Markdown format."""
        question = question_store.create(
            question_text="What is 2+2?",
            answer_options=["3", "4", "5", "6"],
            correct_answer="4",
        )
        markdown = question.to_markdown()
        assert "What is 2+2?" in markdown
        assert "4" in markdown
        assert "\u2713" in markdown