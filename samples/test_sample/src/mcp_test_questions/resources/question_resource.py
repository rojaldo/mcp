"""Question MCP resource."""

from mcp_test_questions.storage.question_store import QuestionStore


def register_question_resource(mcp: "FastMCP", store: QuestionStore) -> None:  # type: ignore[name-defined]
    """Register question resource with MCP server."""

    @mcp.resource("question://{question_id}")
    def get_question_resource(question_id: str, mime_type: str = "application/json") -> str:
        """Get a question as a resource.

        Args:
            question_id: The question ID.
            mime_type: Desired format (application/json or text/markdown).

        Returns:
            Question data in requested format.
        """
        question = store.get(question_id)
        if question is None:
            return '{"error": {"code": "NotFound", "message": "Question not found"}}'

        if mime_type == "text/markdown":
            return question.to_markdown()
        import json

        return json.dumps(question.model_dump(mode="json"), default=str)