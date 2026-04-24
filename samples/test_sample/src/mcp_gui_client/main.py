"""Application entry point for MCP GUI Client."""

from __future__ import annotations

import asyncio
import tkinter as tk
from tkinter import messagebox

from mcp_gui_client.config import Config
from mcp_gui_client.mcp_client.connection import MCPConnection, MCPConnectionError
from mcp_gui_client.views.main_window import MainWindow


def main() -> None:
    """Main entry point for the application."""
    config = Config()
    root = tk.Tk()
    Application(root, config)
    root.mainloop()


class Application:
    """Main application controller."""

    def __init__(self, root: tk.Tk, config: Config) -> None:
        """Initialize the application.

        Args:
            root: The Tkinter root window.
            config: Application configuration.
        """
        self.root = root
        self.config = config
        self.connection: MCPConnection | None = None
        self._setup_root()
        self._create_ui()

    def _setup_root(self) -> None:
        """Configure the root window."""
        self.root.title(self.config.window_title)
        self.root.geometry(
            f"{self.config.window_width}x{self.config.window_height}"
        )
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_ui(self) -> None:
        """Create the main UI."""
        self.main_window = MainWindow(self.root, self)
        self.main_window.pack(fill=tk.BOTH, expand=True)

    async def connect_to_server(self) -> None:
        """Connect to the MCP server."""
        if self.connection is None:
            self.connection = MCPConnection(
                server_command=self.config.server_command
            )

        try:
            await self.connection.connect()
        except MCPConnectionError as e:
            messagebox.showerror(
                "Connection Error", f"Failed to connect: {e.message}"
            )
            raise

    async def disconnect_from_server(self) -> None:
        """Disconnect from the MCP server."""
        if self.connection is not None:
            await self.connection.disconnect()

    def _on_close(self) -> None:
        """Handle window close event."""
        if self.connection is not None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.disconnect_from_server())
            finally:
                loop.close()
        self.root.destroy()


if __name__ == "__main__":
    main()
