"""Main application window."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp_gui_client.main import Application


class MainWindow(ttk.Frame):
    """Main application window containing all UI components."""

    def __init__(self, parent: tk.Tk, app: Application) -> None:
        """Initialize the main window.

        Args:
            parent: The parent Tkinter widget.
            app: The application controller.
        """
        super().__init__(parent)
        self.app = app
        self._create_ui()

    def _create_ui(self) -> None:
        """Create the main UI components."""
        self._create_menu()
        self._create_toolbar()
        self._create_main_area()
        self._create_status_bar()

    def _create_menu(self) -> None:
        """Create the menu bar."""
        menubar = tk.Menu(self)
        self.winfo_toplevel().config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Question", command=self._on_new_question)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.winfo_toplevel().destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._on_about)
        menubar.add_cascade(label="Help", menu=help_menu)

    def _create_toolbar(self) -> None:
        """Create the toolbar."""
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            toolbar, text="New", command=self._on_new_question
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            toolbar, text="Refresh", command=self._on_refresh
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            toolbar, text="Random", command=self._on_random_question
        ).pack(side=tk.LEFT, padx=2)

    def _create_main_area(self) -> None:
        """Create the main content area with paned window."""
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left_frame = ttk.LabelFrame(paned, text="Questions")
        paned.add(left_frame, weight=1)

        list_label = ttk.Label(left_frame, text="Question list will appear here")
        list_label.pack(padx=10, pady=10)

        right_frame = ttk.LabelFrame(paned, text="Details")
        paned.add(right_frame, weight=2)

        detail_label = ttk.Label(right_frame, text="Select a question to view details")
        detail_label.pack(padx=10, pady=10)

    def _create_status_bar(self) -> None:
        """Create the status bar."""
        statusbar = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def _on_new_question(self) -> None:
        """Handle new question button."""
        pass

    def _on_refresh(self) -> None:
        """Handle refresh button."""
        pass

    def _on_random_question(self) -> None:
        """Handle random question button."""
        pass

    def _on_about(self) -> None:
        """Show about dialog."""
        pass
