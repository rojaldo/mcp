"""Update question MCP tool."""

from mcp_test_questions.storage.question_store import NotFoundError, QuestionStore


def register_update_question(mcp: "FastMCP", store: QuestionStore) -> None:  # type: ignore[name-defined]
    """Register update_question tool with MCP server."""

    @mcp.tool()
    def update_question(
        question_id: str,
        question_text: str | None = None,
        answer_options: list[str] | None = None,
        correct_answer: str | None = None,
    ) -> dict:
        """Update an existing question.

        All fields are optional - only provided fields are updated.

        Args:
            question_id: The question ID to update.
            question_text: New question text (optional).
            answer_options: New answer options (optional).
            correct_answer: New correct answer (optional).

        Returns:
            The updated question.

        Raises:
            Error: If question not found or update invalid.
        """
        try:
            question = store.update(
                question_id=question_id,
                question_text=question_text,
                answer_options=answer_options,
                correct_answer=correct_answer,
            )
        except NotFoundError:
            return {
                "error": {
                    "code": "NotFound",
                    "message": f"Question with id '{question_id}' not found",
                }
            }
        except ValueError as e:
            return {"error": {"code": "InvalidParams", "message": str(e)}}
        return question.model_dump(mode="json")