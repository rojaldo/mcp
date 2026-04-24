"""Delete question MCP tool."""

from mcp_test_questions.storage.question_store import NotFoundError, QuestionStore


def register_delete_question(mcp: "FastMCP", store: QuestionStore) -> None:  # type: ignore[name-defined]
    """Register delete_question tool with MCP server."""

    @mcp.tool()
    def delete_question(question_id: str) -> dict:
        """Delete a question by ID.

        Args:
            question_id: The question ID to delete.

        Returns:
            Success confirmation with deleted ID.

        Raises:
            Error: If question not found.
        """
        try:
            store.delete(question_id)
        except NotFoundError:
            return {
                "error": {
                    "code": "NotFound",
                    "message": f"Question with id '{question_id}' not found",
                }
            }
        return {"success": True, "deleted_id": question_id}