# Research: MCP GUI Client

**Feature**: 002-mcp-gui-client
**Date**: 2026-04-22

## Technology Decisions

### GUI Framework

**Decision**: Use Tkinter with ttk (themed widgets)

**Rationale**:
- Built into Python standard library - no external dependencies
- Cross-platform support (Windows, macOS, Linux)
- Sufficient for CRUD-style data management UI
- Easy to test with pytest-qt patterns
- Fast startup and low memory footprint
- ttk widgets provide modern appearance

**Alternatives Considered**:
- PyQt/PySide: More features but heavy dependency, licensing considerations
- wxPython: Cross-platform but larger learning curve
- Web-based (Flask + HTML): Requires browser, more complex architecture
- Dear PyGui: Modern but less mature ecosystem

### MCP Client Connection

**Decision**: Use mcp Python SDK with stdio transport

**Rationale**:
- Official MCP client library for Python
- Supports stdio transport (same as server)
- Async/await compatible
- Well-documented client patterns
- Direct process spawning for local server connection

**Alternatives Considered**:
- HTTP transport: Server uses stdio, would require wrapper
- Custom JSON-RPC: Reinventing MCP client, more maintenance

### Configuration Management

**Decision**: JSON file for persistent settings

**Rationale**:
- Human-readable and editable
- Python json module is built-in
- Cross-platform file locations (user home directory)
- Easy to backup and version
- Simple schema for connection settings

**Alternatives Considered**:
- TOML: Would require tomli dependency
- SQLite: Overkill for simple key-value config
- INI files: Less structured, no nested data

### UI Testing Strategy

**Decision**: pytest with tkinter-specific mocking patterns

**Rationale**:
- Standard testing framework consistent with project
- Mock MCP client for isolated UI testing
- pytest fixtures for common test setup
- 60% coverage target realistic for GUI complexity

**Alternatives Considered**:
- pytest-qt: Designed for Qt, not Tkinter
- unittest.mock: Less flexible than pytest fixtures
- Robot Framework: Too heavy for this project scope

### Async Operations

**Decision**: threading for background MCP operations

**Rationale**:
- Tkinter main loop runs in main thread
- Background operations prevent UI freezing
- Simple threading patterns for async I/O
- Queue-based communication to UI thread

**Alternatives Considered**:
- asyncio: Requires more complex Tkinter integration
- multiprocessing: Overkill for simple client operations
- Blocking calls: Would freeze UI (unacceptable)

## MCP Integration Patterns

### Tool Invocation Pattern

Each MCP tool follows this pattern:
1. User action triggers GUI event
2. Event handler invokes MCP tool via client
3. Response received and parsed
4. UI updated on main thread via queue
5. Error handling displays user-friendly messages

### Resource Access Pattern

Resources accessed via URI template:
1. Format switcher sets desired MIME type
2. Resource request with accept header
3. Content rendered based on format
4. Fallback to JSON if format unavailable

### Connection Management

Pattern for server connection:
1. On startup: Check config for saved server path
2. Display connection dialog if not configured
3. Test connection with ping/status command
4. Store valid connection in config
5. Reconnect on application restart

## Best Practices Identified

1. **Separation of Concerns**: MCP client layer separate from GUI views
2. **Thread Safety**: Use queues for cross-thread communication
3. **Error Propagation**: User-friendly error messages, not raw exceptions
4. **Validation**: Client-side validation before server calls
5. **Responsiveness**: Non-blocking UI with progress indicators
6. **Accessibility**: Standard ttk widgets support keyboard navigation

## Open Questions (Resolved)

All technical questions resolved. The spec clearly defines all MCP tools that need GUI access.