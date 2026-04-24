"""MCP tool invocations for test questions."""

import json
import re
from typing import Any

from mcp_gui_client.mcp_client.connection import MCPConnection


class MCPTools:
    """High-level interface for calling MCP server tools."""

    def __init__(self, connection: MCPConnection) -> None:
        """Initialize MCPTools with a connection.

        Args:
            connection: An established MCP connection.
        """
        self._connection = connection

    async def _invoke_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Invoke a tool and return the raw response.

        Args:
            tool_name: Name of the tool to call.
            arguments: Arguments for the tool.

        Returns:
            The raw tool response.

        Raises:
            Exception: If the tool returns an error.
        """
        response = await self._connection.call_tool(tool_name, arguments)

        if response.get("isError"):
            error_text = ""
            for content in response.get("content", []):
                if content.get("type") == "text":
                    error_text = content.get("text", "")
                    break
            raise Exception(error_text)

        return response

    def _extract_text(self, response: dict[str, Any]) -> str:
        """Extract text content from a tool response.

        Args:
            response: The tool response.

        Returns:
            The text content.
        """
        for content in response.get("content", []):
            if content.get("type") == "text":
                return content.get("text", "")
        return ""

    async def create_question(
        self,
        question_text: str,
        answer_options: list[str],
        correct_answer: str,
    ) -> str:
        """Create a new question.

        Args:
            question_text: The question text.
            answer_options: List of answer options.
            correct_answer: The correct answer.

        Returns:
            The ID of the created question.
        """
        response = await self._invoke_tool(
            "create_question",
            {
                "question_text": question_text,
                "answer_options": answer_options,
                "correct_answer": correct_answer,
            },
        )

        text = self._extract_text(response)
        match = re.search(r"ID:\s*([\w-]+)", text)
        if match:
            return match.group(1)
        return text

    async def get_question(self, question_id: str) -> dict[str, Any]:
        """Get a question by ID.

        Args:
            question_id: The question ID.

        Returns:
            The question as a dictionary.
        """
        response = await self._invoke_tool("get_question", {"question_id": question_id})
        return json.loads(self._extract_text(response))

    async def update_question(
        self,
        question_id: str,
        question_text: str | None = None,
        answer_options: list[str] | None = None,
        correct_answer: str | None = None,
    ) -> dict[str, Any]:
        """Update an existing question.

        Args:
            question_id: The question ID.
            question_text: Optional new question text.
            answer_options: Optional new answer options.
            correct_answer: Optional new correct answer.

        Returns:
            The updated question as a dictionary.
        """
        arguments: dict[str, Any] = {"question_id": question_id}
        if question_text is not None:
            arguments["question_text"] = question_text
        if answer_options is not None:
            arguments["answer_options"] = answer_options
        if correct_answer is not None:
            arguments["correct_answer"] = correct_answer

        response = await self._invoke_tool("update_question", arguments)
        return json.loads(self._extract_text(response))

    async def delete_question(self, question_id: str) -> bool:
        """Delete a question by ID.

        Args:
            question_id: The question ID.

        Returns:
            True if deletion was successful.
        """
        await self._invoke_tool("delete_question", {"question_id": question_id})
        return True

    async def list_questions(self) -> list[dict[str, Any]]:
        """List all questions.

        Returns:
            List of questions as dictionaries.
        """
        response = await self._invoke_tool("list_questions", {})
        return json.loads(self._extract_text(response))

    async def get_random_question(self) -> dict[str, Any]:
        """Get a random question.

        Returns:
            A random question as a dictionary.
        """
        response = await self._invoke_tool("get_random_question", {})
        return json.loads(self._extract_text(response))
