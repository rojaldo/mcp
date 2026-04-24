"""Unit tests for input validators."""

import pytest

from mcp_gui_client.utils.validators import (
    validate_question_text,
    validate_answer_options,
    validate_correct_answer,
    validate_question_id,
    ValidationError,
)


class TestValidateQuestionText:
    """Tests for question text validation."""

    def test_valid_question_text(self) -> None:
        """Valid question text should return without error."""
        result = validate_question_text("What is 2+2?")
        assert result == "What is 2+2?"

    def test_strips_whitespace(self) -> None:
        """Should strip leading/trailing whitespace."""
        result = validate_question_text("  What is 2+2?  ")
        assert result == "What is 2+2?"

    def test_empty_text_raises_error(self) -> None:
        """Empty text should raise ValidationError."""
        with pytest.raises(ValidationError, match="Question text cannot be empty"):
            validate_question_text("")

    def test_whitespace_only_raises_error(self) -> None:
        """Whitespace-only text should raise ValidationError."""
        with pytest.raises(ValidationError, match="Question text cannot be empty"):
            validate_question_text("   ")

    def test_minimum_length(self) -> None:
        """Minimum length (3 chars) should be valid."""
        result = validate_question_text("ABC")
        assert result == "ABC"

    def test_too_short_raises_error(self) -> None:
        """Text shorter than 3 chars should raise error."""
        with pytest.raises(ValidationError, match="at least 3 characters"):
            validate_question_text("AB")

    def test_maximum_length(self) -> None:
        """Maximum length (1000 chars) should be valid."""
        long_text = "A" * 1000
        result = validate_question_text(long_text)
        assert len(result) == 1000

    def test_too_long_raises_error(self) -> None:
        """Text longer than 1000 chars should raise error."""
        long_text = "A" * 1001
        with pytest.raises(ValidationError, match="cannot exceed 1000 characters"):
            validate_question_text(long_text)


class TestValidateAnswerOptions:
    """Tests for answer options validation."""

    def test_valid_options_list(self) -> None:
        """Valid options list should return without error."""
        options = ["3", "4", "5", "6"]
        result = validate_answer_options(options)
        assert result == ["3", "4", "5", "6"]

    def test_minimum_two_options(self) -> None:
        """Minimum 2 options should be valid."""
        options = ["Yes", "No"]
        result = validate_answer_options(options)
        assert result == ["Yes", "No"]

    def test_single_option_raises_error(self) -> None:
        """Single option should raise ValidationError."""
        with pytest.raises(ValidationError, match="at least 2 options"):
            validate_answer_options(["Only one"])

    def test_empty_list_raises_error(self) -> None:
        """Empty list should raise ValidationError."""
        with pytest.raises(ValidationError, match="at least 2 options"):
            validate_answer_options([])

    def test_maximum_eight_options(self) -> None:
        """Maximum 8 options should be valid."""
        options = [str(i) for i in range(8)]
        result = validate_answer_options(options)
        assert len(result) == 8

    def test_too_many_options_raises_error(self) -> None:
        """More than 8 options should raise error."""
        options = [str(i) for i in range(9)]
        with pytest.raises(ValidationError, match="cannot exceed 8 options"):
            validate_answer_options(options)

    def test_strips_whitespace_from_options(self) -> None:
        """Should strip whitespace from each option."""
        options = ["  A  ", "  B  "]
        result = validate_answer_options(options)
        assert result == ["A", "B"]

    def test_empty_option_raises_error(self) -> None:
        """Empty option string should raise error."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_answer_options(["A", ""])

    def test_duplicate_options_raises_error(self) -> None:
        """Duplicate options should raise error."""
        with pytest.raises(ValidationError, match="must be unique"):
            validate_answer_options(["A", "B", "A"])

    def test_accepts_valid_type(self) -> None:
        """Should accept string input and convert to list."""
        result = validate_answer_options(["A", "B"])
        assert result == ["A", "B"]


class TestValidateCorrectAnswer:
    """Tests for correct answer validation."""

    def test_valid_answer(self) -> None:
        """Valid answer matching an option should return without error."""
        options = ["3", "4", "5", "6"]
        result = validate_correct_answer("4", options)
        assert result == "4"

    def test_answer_with_whitespace(self) -> None:
        """Should strip whitespace from answer."""
        options = ["3", "4", "5", "6"]
        result = validate_correct_answer("  4  ", options)
        assert result == "4"

    def test_answer_not_in_options_raises_error(self) -> None:
        """Answer not in options should raise ValidationError."""
        options = ["3", "4", "5", "6"]
        with pytest.raises(ValidationError, match="must match one of the options"):
            validate_correct_answer("7", options)

    def test_empty_answer_raises_error(self) -> None:
        """Empty answer should raise ValidationError."""
        options = ["3", "4", "5", "6"]
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_correct_answer("", options)


class TestValidateQuestionId:
    """Tests for question ID validation."""

    def test_valid_uuid(self) -> None:
        """Valid UUID should return without error."""
        test_id = "123e4567-e89b-12d3-a456-426614174000"
        result = validate_question_id(test_id)
        assert result == test_id

    def test_id_with_whitespace(self) -> None:
        """Should strip whitespace from ID."""
        test_id = "  123e4567-e89b-12d3-a456-426614174000  "
        result = validate_question_id(test_id)
        assert result == "123e4567-e89b-12d3-a456-426614174000"

    def test_invalid_uuid_raises_error(self) -> None:
        """Invalid UUID should raise ValidationError."""
        with pytest.raises(ValidationError, match="Invalid UUID"):
            validate_question_id("not-a-uuid")

    def test_empty_id_raises_error(self) -> None:
        """Empty ID should raise ValidationError."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_question_id("")


class TestValidationError:
    """Tests for ValidationError class."""

    def test_error_message(self) -> None:
        """ValidationError should contain message."""
        error = ValidationError("Test error message")
        assert str(error) == "Test error message"
        assert error.message == "Test error message"

    def test_error_inheritance(self) -> None:
        """ValidationError should inherit from ValueError."""
        error = ValidationError("Test error")
        assert isinstance(error, ValueError)