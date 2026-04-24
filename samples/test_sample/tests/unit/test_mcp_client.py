"""Unit tests for MCP client."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_gui_client.mcp_client.connection import MCPConnection, MCPConnectionError
from mcp_gui_client.mcp_client.tools import MCPTools


class TestMCPConnection:
    """Tests for MCP connection management."""

    def test_connection_creation(self) -> None:
        """Should create connection with server config."""
        connection = MCPConnection(server_command="python -m mcp_test_questions.server")
        assert connection.server_command == "python -m mcp_test_questions.server"

    def test_connection_default_state(self) -> None:
        """New connection should not be connected."""
        connection = MCPConnection(server_command="python -m mcp_test_questions.server")
        assert not connection.is_connected

    @pytest.mark.asyncio
    async def test_connect_starts_server(self) -> None:
        """Connect should start the MCP server process."""
        connection = MCPConnection(server_command="python -m mcp_test_questions.server")
        with patch("asyncio.create_subprocess_exec") as mock_subprocess:
            mock_proc = AsyncMock()
            mock_proc.stdin = MagicMock()
            mock_proc.stdin.drain = AsyncMock()
            mock_proc.stdin.write = MagicMock()
            mock_proc.stdout = MagicMock()
            mock_proc.stdout.readline = AsyncMock(return_value=b'{"result":{"protocolVersion":"2024-11-05"}}\n')
            mock_proc.stderr = MagicMock()
            mock_proc.pid = 12345
            mock_subprocess.return_value = mock_proc

            await connection.connect()

            mock_subprocess.assert_called_once()
            assert connection.is_connected

    @pytest.mark.asyncio
    async def test_disconnect_stops_server(self) -> None:
        """Disconnect should stop the MCP server process."""
        connection = MCPConnection(server_command="python -m mcp_test_questions.server")
        with patch("asyncio.create_subprocess_exec") as mock_subprocess:
            mock_proc = AsyncMock()
            mock_proc.stdin = MagicMock()
            mock_proc.stdin.drain = AsyncMock()
            mock_proc.stdin.write = MagicMock()
            mock_proc.stdout = MagicMock()
            mock_proc.stdout.readline = AsyncMock(return_value=b'{"result":{"protocolVersion":"2024-11-05"}}\n')
            mock_proc.stderr = MagicMock()
            mock_proc.pid = 12345
            mock_proc.terminate = MagicMock()
            mock_proc.wait = AsyncMock()
            mock_subprocess.return_value = mock_proc

            await connection.connect()
            await connection.disconnect()

            mock_proc.terminate.assert_called_once()
            assert not connection.is_connected

    @pytest.mark.asyncio
    async def test_connect_already_connected_raises_error(self) -> None:
        """Connecting when already connected should raise error."""
        connection = MCPConnection(server_command="python -m mcp_test_questions.server")
        with patch("asyncio.create_subprocess_exec") as mock_subprocess:
            mock_proc = AsyncMock()
            mock_proc.stdin = MagicMock()
            mock_proc.stdin.drain = AsyncMock()
            mock_proc.stdin.write = MagicMock()
            mock_proc.stdout = MagicMock()
            mock_proc.stdout.readline = AsyncMock(return_value=b'{"result":{"protocolVersion":"2024-11-05"}}\n')
            mock_proc.stderr = MagicMock()
            mock_proc.pid = 12345
            mock_subprocess.return_value = mock_proc

            await connection.connect()

            with pytest.raises(MCPConnectionError, match="Already connected"):
                await connection.connect()

    @pytest.mark.asyncio
    async def test_disconnect_when_not_connected(self) -> None:
        """Disconnect when not connected should be a no-op."""
        connection = MCPConnection(server_command="python -m mcp_test_questions.server")
        await connection.disconnect()
        assert not connection.is_connected


class TestMCPTools:
    """Tests for MCP tool invocations."""

    @pytest.fixture
    def mock_connection(self) -> MCPConnection:
        """Create a mocked MCP connection."""
        connection = MCPConnection(server_command="test")
        connection._process = AsyncMock()
        connection._process.stdin = MagicMock()
        connection._process.stdout = MagicMock()
        connection._connected = True
        connection.call_tool = AsyncMock()
        return connection

    @pytest.fixture
    def mcp_tools(self, mock_connection: MCPConnection) -> MCPTools:
        """Create MCPTools with mocked connection."""
        return MCPTools(connection=mock_connection)

    @pytest.mark.asyncio
    async def test_create_question(self, mcp_tools: MCPTools) -> None:
        """Create question should invoke MCP tool and return ID."""
        response = {"content": [{"type": "text", "text": "Created question with ID: test-id-123"}]}

        with patch.object(mcp_tools, "_invoke_tool", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = response

            result = await mcp_tools.create_question(
                question_text="What is 2+2?",
                answer_options=["3", "4", "5", "6"],
                correct_answer="4",
            )

            mock_invoke.assert_called_once_with(
                "create_question",
                {
                    "question_text": "What is 2+2?",
                    "answer_options": ["3", "4", "5", "6"],
                    "correct_answer": "4",
                },
            )
            assert result == "test-id-123"

    @pytest.mark.asyncio
    async def test_get_question(self, mcp_tools: MCPTools, sample_question_dict: dict[str, object]) -> None:
        """Get question should invoke MCP tool and return question dict."""
        response = {"content": [{"type": "text", "text": json.dumps(sample_question_dict)}]}

        with patch.object(mcp_tools, "_invoke_tool", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = response

            result = await mcp_tools.get_question(question_id="test-id-123")

            mock_invoke.assert_called_once_with("get_question", {"question_id": "test-id-123"})
            assert result == sample_question_dict

    @pytest.mark.asyncio
    async def test_update_question(self, mcp_tools: MCPTools, sample_question_dict: dict[str, object]) -> None:
        """Update question should invoke MCP tool and return updated question."""
        sample_question_dict["question_text"] = "Updated question"
        response = {"content": [{"type": "text", "text": json.dumps(sample_question_dict)}]}

        with patch.object(mcp_tools, "_invoke_tool", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = response

            result = await mcp_tools.update_question(
                question_id="test-id-123",
                question_text="Updated question",
            )

            mock_invoke.assert_called_once_with(
                "update_question",
                {"question_id": "test-id-123", "question_text": "Updated question"},
            )
            assert result["question_text"] == "Updated question"

    @pytest.mark.asyncio
    async def test_delete_question(self, mcp_tools: MCPTools) -> None:
        """Delete question should invoke MCP tool and return success."""
        response = {"content": [{"type": "text", "text": "Question deleted successfully"}]}

        with patch.object(mcp_tools, "_invoke_tool", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = response

            result = await mcp_tools.delete_question(question_id="test-id-123")

            mock_invoke.assert_called_once_with("delete_question", {"question_id": "test-id-123"})
            assert result is True

    @pytest.mark.asyncio
    async def test_list_questions(self, mcp_tools: MCPTools, sample_questions_list: list[dict[str, object]]) -> None:
        """List questions should invoke MCP tool and return questions list."""
        response = {"content": [{"type": "text", "text": json.dumps(sample_questions_list)}]}

        with patch.object(mcp_tools, "_invoke_tool", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = response

            result = await mcp_tools.list_questions()

            mock_invoke.assert_called_once_with("list_questions", {})
            assert result == sample_questions_list

    @pytest.mark.asyncio
    async def test_get_random_question(self, mcp_tools: MCPTools, sample_question_dict: dict[str, object]) -> None:
        """Get random question should invoke MCP tool and return a question."""
        response = {"content": [{"type": "text", "text": json.dumps(sample_question_dict)}]}

        with patch.object(mcp_tools, "_invoke_tool", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = response

            result = await mcp_tools.get_random_question()

            mock_invoke.assert_called_once_with("get_random_question", {})
            assert result == sample_question_dict

    @pytest.mark.asyncio
    async def test_tool_error_handling(self, mcp_tools: MCPTools) -> None:
        """Tool invocation error should raise appropriate exception."""
        error_response = {
            "content": [{"type": "text", "text": "Error: Question not found"}],
            "isError": True,
        }

        with patch.object(mcp_tools._connection, "call_tool", new_callable=AsyncMock) as mock_call:
            mock_call.return_value = error_response

            with pytest.raises(Exception, match="Question not found"):
                await mcp_tools.get_question(question_id="non-existent-id")


class TestMCPConnectionError:
    """Tests for MCPConnectionError."""

    def test_error_message(self) -> None:
        """MCPConnectionError should contain message."""
        error = MCPConnectionError("Test connection error")
        assert str(error) == "Test connection error"

    def test_error_inheritance(self) -> None:
        """MCPConnectionError should inherit from Exception."""
        error = MCPConnectionError("Test error")
        assert isinstance(error, Exception)