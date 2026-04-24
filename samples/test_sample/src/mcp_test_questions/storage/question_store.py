"""Question storage with in-memory and file persistence."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from mcp_test_questions.models.question import Question


class NotFoundError(Exception):
    """Raised when a question is not found."""

    def __init__(self, question_id: str) -> None:
        self.question_id = question_id
        super().__init__(f"Question with id '{question_id}' not found")


class StoreEmptyError(Exception):
    """Raised when store is empty but operation requires questions."""

    def __init__(self) -> None:
        super().__init__("No questions available in store")


class QuestionStore:
    """In-memory question storage with JSON file persistence."""

    def __init__(self, file_path: Path | None = None) -> None:
        """Initialize store, optionally loading from file.

        Args:
            file_path: Path to JSON file for persistence. Defaults to
                'questions.json' in current directory or QUESTIONS_FILE env var.
        """
        self._questions: dict[str, Question] = {}
        self._file_path = file_path or Path(
            os.environ.get("QUESTIONS_FILE", "questions.json")
        )
        self._load()

    def create(
        self,
        question_text: str,
        answer_options: list[str],
        correct_answer: str,
    ) -> Question:
        """Create a new question.

        Args:
            question_text: The question prompt text.
            answer_options: List of answer options.
            correct_answer: The correct answer.

        Returns:
            The created Question instance.
        """
        question_id = str(uuid4())
        now = datetime.utcnow()
        question = Question(
            id=question_id,
            question_text=question_text,
            answer_options=answer_options,
            correct_answer=correct_answer,
            created_at=now,
            updated_at=now,
        )
        self._questions[question_id] = question
        self._save()
        return question

    def get(self, question_id: str) -> Question | None:
        """Get a question by ID.

        Args:
            question_id: The question ID.

        Returns:
            The Question if found, None otherwise.
        """
        return self._questions.get(question_id)

    def get_random(self) -> Question:
        """Get a random question.

        Returns:
            A random Question from the store.

        Raises:
            StoreEmptyError: If store has no questions.
        """
        import random

        if not self._questions:
            raise StoreEmptyError()
        return random.choice(list(self._questions.values()))

    def get_all(self) -> list[Question]:
        """Get all questions.

        Returns:
            List of all questions in the store.
        """
        return list(self._questions.values())

    def update(
        self,
        question_id: str,
        question_text: str | None = None,
        answer_options: list[str] | None = None,
        correct_answer: str | None = None,
    ) -> Question:
        """Update a question.

        Args:
            question_id: The question ID to update.
            question_text: New question text (optional).
            answer_options: New answer options (optional).
            correct_answer: New correct answer (optional).

        Returns:
            The updated Question.

        Raises:
            NotFoundError: If question doesn't exist.
            ValueError: If update would result in invalid state.
        """
        if question_id not in self._questions:
            raise NotFoundError(question_id)

        existing = self._questions[question_id]

        new_text = question_text if question_text is not None else existing.question_text
        new_options = (
            answer_options if answer_options is not None else existing.answer_options
        )
        new_correct = (
            correct_answer if correct_answer is not None else existing.correct_answer
        )

        if new_correct not in new_options:
            raise ValueError("correct_answer must be in answer_options")

        updated = Question(
            id=existing.id,
            question_text=new_text,
            answer_options=new_options,
            correct_answer=new_correct,
            created_at=existing.created_at,
            updated_at=datetime.utcnow(),
        )
        self._questions[question_id] = updated
        self._save()
        return updated

    def delete(self, question_id: str) -> None:
        """Delete a question.

        Args:
            question_id: The question ID to delete.

        Raises:
            NotFoundError: If question doesn't exist.
        """
        if question_id not in self._questions:
            raise NotFoundError(question_id)
        del self._questions[question_id]
        self._save()

    def count(self) -> int:
        """Count total questions.

        Returns:
            Number of questions in store.
        """
        return len(self._questions)

    def _load(self) -> None:
        """Load questions from JSON file if exists."""
        if not self._file_path.exists():
            return

        try:
            with open(self._file_path, encoding="utf-8") as f:
                data = json.load(f)
                for question_data in data.get("questions", {}).values():
                    question = Question.model_validate(question_data)
                    self._questions[question.id] = question
        except (json.JSONDecodeError, KeyError, ValueError):
            pass

    def _save(self) -> None:
        """Save questions to JSON file."""
        data: dict[str, Any] = {
            "version": "1.0",
            "questions": {
                qid: q.model_dump(mode="json") for qid, q in self._questions.items()
            },
        }
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)