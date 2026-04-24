"""Create question MCP tool."""

from mcp_test_questions.models.question import Question
from mcp_test_questions.storage.question_store import QuestionStore


def register_create_question(mcp: "FastMCP", store: QuestionStore) -> None:  # type: ignore[name-defined]
    """Register create_question tool with MCP server."""

    @mcp.tool()
    def create_question(
        question_text: str,
        answer_options: list[str],
        correct_answer: str,
    ) -> dict:
        """Create a new multiple-choice question.

        Args:
            question_text: The text of the question.
            answer_options: List of answer options (2-10 items).
            correct_answer: The correct answer (must be in answer_options).

        Returns:
            The created question with id and timestamps.

        Raises:
            Error: If validation fails.
        """
        question = store.create(
            question_text=question_text,
            answer_options=answer_options,
            correct_answer=correct_answer,
        )
        return question.model_dump(mode="json")