"""Configuration management for MCP GUI Client."""

import json
from pathlib import Path
from typing import Any


class Config:
    """Manages application configuration."""

    DEFAULT_CONFIG: dict[str, Any] = {
        "server_command": "python -m mcp_test_questions.server",
        "window": {
            "width": 1024,
            "height": 768,
            "title": "MCP Test Questions Client",
        },
        "view_format": "formatted",
    }

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize configuration.

        Args:
            config_path: Path to config file. Defaults to user home directory.
        """
        if config_path is None:
            config_dir = Path.home() / ".mcp_gui_client"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_path = config_dir / "config.json"

        self.config_path = config_path
        self._config: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    self._config = json.load(f)
            except (json.JSONDecodeError, OSError):
                self._config = self.DEFAULT_CONFIG.copy()
        else:
            self._config = self.DEFAULT_CONFIG.copy()
            self.save()

    def save(self) -> None:
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(self._config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key (supports dot notation).
            default: Default value if key not found.

        Returns:
            The configuration value.
        """
        keys = key.split(".")
        value: Any = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: Configuration key (supports dot notation).
            value: Value to set.
        """
        keys = key.split(".")
        config: dict[str, Any] = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    @property
    def server_command(self) -> str:
        """Get the MCP server command."""
        return self.get("server_command", self.DEFAULT_CONFIG["server_command"])

    @server_command.setter
    def server_command(self, value: str) -> None:
        """Set the MCP server command."""
        self.set("server_command", value)
        self.save()

    @property
    def window_width(self) -> int:
        """Get the window width."""
        return self.get("window.width", self.DEFAULT_CONFIG["window"]["width"])

    @property
    def window_height(self) -> int:
        """Get the window height."""
        return self.get("window.height", self.DEFAULT_CONFIG["window"]["height"])

    @property
    def window_title(self) -> str:
        """Get the window title."""
        return self.get("window.title", self.DEFAULT_CONFIG["window"]["title"])

    @property
    def view_format(self) -> str:
        """Get the default view format."""
        return self.get("view_format", self.DEFAULT_CONFIG["view_format"])

    @view_format.setter
    def view_format(self, value: str) -> None:
        """Set the default view format."""
        self.set("view_format", value)
        self.save()
