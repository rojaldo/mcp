"""Unit tests for question resource formatting."""

import uuid
from datetime import datetime

from mcp_test_questions.models.question import Question


class TestQuestionResourceFormatting:
    """Test question resource formatting to JSON and Markdown."""

    def test_question_to_markdown_includes_question_text(self) -> None:
        """Test Markdown output includes question text."""
        question = Question(
            id=str(uuid.uuid4()),
            question_text="What is 2+2?",
            answer_options=["3", "4", "5", "6"],
            correct_answer="4",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        markdown = question.to_markdown()
        assert "What is 2+2?" in markdown

    def test_question_to_markdown_has_header(self) -> None:
        """Test Markdown output has proper header with ID."""
        question = Question(
            id=str(uuid.uuid4()),
            question_text="Test?",
            answer_options=["A", "B"],
            correct_answer="A",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        markdown = question.to_markdown()
        assert "# Question:" in markdown
        assert question.id in markdown

    def test_question_to_markdown_lists_options(self) -> None:
        """Test Markdown output lists all answer options."""
        question = Question(
            id=str(uuid.uuid4()),
            question_text="What is the capital of France?",
            answer_options=["London", "Paris", "Berlin", "Madrid"],
            correct_answer="Paris",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        markdown = question.to_markdown()
        assert "London" in markdown
        assert "Paris" in markdown
        assert "Berlin" in markdown
        assert "Madrid" in markdown

    def test_question_to_markdown_marks_correct_answer(self) -> None:
        """Test Markdown output marks correct answer with checkmark."""
        question = Question(
            id=str(uuid.uuid4()),
            question_text="Test?",
            answer_options=["Wrong", "Correct"],
            correct_answer="Correct",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        markdown = question.to_markdown()
        lines = markdown.split("\n")
        correct_line = next(line for line in lines if "Correct" in line)
        assert "\u2713" in correct_line

    def test_question_to_markdown_includes_metadata(self) -> None:
        """Test Markdown output includes creation and update timestamps."""
        question = Question(
            id=str(uuid.uuid4()),
            question_text="Test?",
            answer_options=["A", "B"],
            correct_answer="A",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        markdown = question.to_markdown()
        assert "## Metadata" in markdown
        assert "**Created**:" in markdown
        assert "**Last Updated**:" in markdown

    def test_question_model_dump_json(self) -> None:
        """Test question can be serialized to JSON dict."""
        question = Question(
            id=str(uuid.uuid4()),
            question_text="Test?",
            answer_options=["A", "B"],
            correct_answer="A",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        data = question.model_dump(mode="json")
        assert isinstance(data, dict)
        assert "id" in data
        assert "question_text" in data
        assert data["question_text"] == "Test?"