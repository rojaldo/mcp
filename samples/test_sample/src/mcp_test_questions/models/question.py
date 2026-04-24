"""Question model for MCP Test Questions Server."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator


class Question(BaseModel):
    """Represents a multiple-choice test question."""

    id: str = Field(description="Unique identifier (UUID format)")
    question_text: str = Field(
        min_length=1,
        max_length=2000,
        description="The question prompt text",
    )
    answer_options: list[str] = Field(
        min_length=2,
        max_length=10,
        description="List of possible answer options",
    )
    correct_answer: str = Field(description="The correct answer")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last modification timestamp")

    @field_validator("id")
    @classmethod
    def validate_id_format(cls, v: str) -> str:
        """Validate that id is a valid UUID format."""
        UUID(v)
        return v

    @field_validator("answer_options")
    @classmethod
    def validate_option_length(cls, v: list[str]) -> list[str]:
        """Validate that each option is within length limits."""
        for option in v:
            if len(option) < 1 or len(option) > 500:
                raise ValueError("Each answer option must be between 1 and 500 characters")
        return v

    @field_validator("answer_options")
    @classmethod
    def validate_no_duplicates(cls, v: list[str]) -> list[str]:
        """Validate that there are no duplicate options."""
        if len(v) != len(set(v)):
            raise ValueError("Answer options must not contain duplicates")
        return v

    @model_validator(mode="after")
    def validate_correct_answer_in_options(self) -> "Question":
        """Validate that correct_answer exists in answer_options."""
        if self.correct_answer not in self.answer_options:
            raise ValueError("correct_answer must be in answer_options")
        return self

    def to_markdown(self) -> str:
        """Convert question to Markdown format."""
        lines = [
            f"# Question: {self.id}",
            "",
            "## Question",
            "",
            self.question_text,
            "",
            "## Answer Options",
            "",
        ]
        for i, option in enumerate(self.answer_options, 1):
            marker = " \u2713" if option == self.correct_answer else ""
            lines.append(f"{i}. {option}{marker}")
        lines.extend(
            [
                "",
                "## Metadata",
                "",
                f"- **Created**: {self.created_at.isoformat()}Z",
                f"- **Last Updated**: {self.updated_at.isoformat()}Z",
            ]
        )
        return "\n".join(lines)