"""MCP connection management."""

import asyncio
import json
from typing import Any


class MCPConnectionError(Exception):
    """Exception raised when MCP connection fails."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class MCPConnection:
    """Manages connection to an MCP server via stdio transport."""

    def __init__(self, server_command: str) -> None:
        """Initialize MCP connection.

        Args:
            server_command: Command to start the MCP server.
        """
        self.server_command = server_command
        self._process: asyncio.subprocess.Process | None = None
        self._connected = False
        self._request_id = 0

    @property
    def is_connected(self) -> bool:
        """Check if connection is active."""
        return self._connected and self._process is not None

    async def connect(self) -> None:
        """Start the MCP server process and establish connection.

        Raises:
            MCPConnectionError: If connection fails or already connected.
        """
        if self._connected:
            raise MCPConnectionError("Already connected to MCP server")

        parts = self.server_command.split()
        self._process = await asyncio.create_subprocess_exec(
            *parts,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        self._connected = True

        await self._initialize()

    async def _initialize(self) -> None:
        """Send initialize request to MCP server."""
        _result = await self.send_request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "mcp-gui-client", "version": "0.1.0"},
            },
        )
        await self.send_notification("notifications/initialized", {})

    async def disconnect(self) -> None:
        """Stop the MCP server process and close connection."""
        if self._process is not None:
            self._process.terminate()
            await self._process.wait()
            self._process = None
        self._connected = False

    async def send_request(
        self, method: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Send a JSON-RPC request to the MCP server.

        Args:
            method: The RPC method name.
            params: Optional parameters for the request.

        Returns:
            The result from the server.

        Raises:
            MCPConnectionError: If not connected or request fails.
        """
        if (
            not self.is_connected
            or self._process is None
            or self._process.stdin is None
        ):
            raise MCPConnectionError("Not connected to MCP server")

        self._request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
            "params": params or {},
        }

        self._process.stdin.write((json.dumps(request) + "\n").encode())
        await self._process.stdin.drain()

        return await self._read_response()

    async def send_notification(self, method: str, params: dict[str, Any] | None = None) -> None:
        """Send a JSON-RPC notification to the MCP server.

        Args:
            method: The RPC method name.
            params: Optional parameters for the notification.
        """
        if not self.is_connected or self._process is None or self._process.stdin is None:
            return

        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
        }

        self._process.stdin.write((json.dumps(notification) + "\n").encode())
        await self._process.stdin.drain()

    async def _read_response(self) -> dict[str, Any]:
        """Read a JSON-RPC response from the MCP server.

        Returns:
            The parsed response.

        Raises:
            MCPConnectionError: If response cannot be read.
        """
        if self._process is None or self._process.stdout is None:
            raise MCPConnectionError("Cannot read from server")

        response_line = await self._process.stdout.readline()
        if not response_line:
            raise MCPConnectionError("Empty response from server")

        try:
            response = json.loads(response_line.decode().strip())
        except json.JSONDecodeError as e:
            raise MCPConnectionError(f"Invalid JSON response: {e}") from None

        if "error" in response:
            raise MCPConnectionError(response["error"].get("message", "Unknown error"))

        return response.get("result", {})

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Call an MCP tool by name.

        Args:
            tool_name: Name of the tool to call.
            arguments: Arguments for the tool.

        Returns:
            The tool result.
        """
        return await self.send_request(
            "tools/call",
            {"name": tool_name, "arguments": arguments},
        )
