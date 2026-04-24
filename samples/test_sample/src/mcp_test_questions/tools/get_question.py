"""Get question MCP tool."""

from mcp_test_questions.storage.question_store import (
    NotFoundError,
    QuestionStore,
    StoreEmptyError,
)


def register_get_question(mcp: "FastMCP", store: QuestionStore) -> None:  # type: ignore[name-defined]
    """Register get_question tool with MCP server."""

    @mcp.tool()
    def get_question(question_id: str | None = None) -> dict:
        """Retrieve a question by ID or get a random question.

        Args:
            question_id: The question ID to retrieve. If omitted, returns a random question.

        Returns:
            The question data if found.

        Raises:
            Error: If question not found or store is empty for random query.
        """
        if question_id is None:
            try:
                question = store.get_random()
            except StoreEmptyError:
                return {"error": {"code": "Internal", "message": "No questions available"}}
        else:
            question = store.get(question_id)
            if question is None:
                return {
                    "error": {
                        "code": "NotFound",
                        "message": f"Question with id '{question_id}' not found",
                    }
                }
        return question.model_dump(mode="json")