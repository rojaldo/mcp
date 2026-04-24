"""Input validation utilities for GUI forms."""

import uuid


class ValidationError(ValueError):
    """Validation error with message."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def validate_question_text(text: str) -> str:
    """Validate question text.

    Args:
        text: The question text to validate.

    Returns:
        Stripped and validated question text.

    Raises:
        ValidationError: If text is empty, too short, or too long.
    """
    stripped = text.strip()
    if not stripped:
        raise ValidationError("Question text cannot be empty")

    if len(stripped) < 3:
        raise ValidationError("Question text must be at least 3 characters")

    if len(stripped) > 1000:
        raise ValidationError("Question text cannot exceed 1000 characters")

    return stripped


def validate_answer_options(options: list[str]) -> list[str]:
    """Validate answer options list.

    Args:
        options: List of answer options to validate.

    Returns:
        List of stripped and validated options.

    Raises:
        ValidationError: If options list is invalid.
    """
    if len(options) < 2:
        raise ValidationError("Answer options must have at least 2 options")

    if len(options) > 8:
        raise ValidationError("Answer options cannot exceed 8 options")

    stripped_options = [opt.strip() for opt in options]

    for i, opt in enumerate(stripped_options):
        if not opt:
            raise ValidationError(f"Answer option {i + 1} cannot be empty")

    if len(set(stripped_options)) != len(stripped_options):
        raise ValidationError("Answer options must be unique")

    return stripped_options


def validate_correct_answer(answer: str, options: list[str]) -> str:
    """Validate correct answer against options.

    Args:
        answer: The correct answer to validate.
        options: List of valid answer options.

    Returns:
        Stripped and validated answer.

    Raises:
        ValidationError: If answer is invalid or doesn't match options.
    """
    stripped_answer = answer.strip()
    stripped_options = [opt.strip() for opt in options]

    if not stripped_answer:
        raise ValidationError("Correct answer cannot be empty")

    if stripped_answer not in stripped_options:
        raise ValidationError("Correct answer must match one of the options")

    return stripped_answer


def validate_question_id(question_id: str) -> str:
    """Validate question ID as UUID.

    Args:
        question_id: The question ID to validate.

    Returns:
        Stripped and validated question ID.

    Raises:
        ValidationError: If ID is not a valid UUID.
    """
    stripped = question_id.strip()

    if not stripped:
        raise ValidationError("Question ID cannot be empty")

    try:
        uuid.UUID(stripped)
    except ValueError:
        raise ValidationError(f"Invalid UUID format: {stripped}") from None

    return stripped
