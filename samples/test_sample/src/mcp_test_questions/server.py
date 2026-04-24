"""Main MCP server entry point."""

from pathlib import Path

from mcp_test_questions.storage.question_store import QuestionStore

_store: QuestionStore | None = None


def get_store() -> QuestionStore:
    """Get the global QuestionStore instance."""
    global _store
    if _store is None:
        _store = QuestionStore()
    return _store


def main() -> None:
    """Main entry point for MCP server."""
    from fastmcp import FastMCP

    mcp = FastMCP("Test Questions Server")

    store = get_store()

    from mcp_test_questions.tools.create_question import register_create_question
    from mcp_test_questions.tools.delete_question import register_delete_question
    from mcp_test_questions.tools.get_question import register_get_question
    from mcp_test_questions.tools.update_question import register_update_question

    register_create_question(mcp, store)
    register_get_question(mcp, store)
    register_update_question(mcp, store)
    register_delete_question(mcp, store)

    from mcp_test_questions.resources.question_resource import register_question_resource

    register_question_resource(mcp, store)

    mcp.run()


if __name__ == "__main__":
    main()