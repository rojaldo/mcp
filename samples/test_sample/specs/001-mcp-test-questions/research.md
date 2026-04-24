# Research: MCP Test Questions Server

**Feature**: 001-mcp-test-questions
**Date**: 2026-04-22

## Technology Decisions

### FastMCP Framework

**Decision**: Use FastMCP as the primary MCP framework

**Rationale**:
- Simplified decorator-based API for defining tools and resources
- Built-in Pydantic integration for automatic schema generation
- Native support for stdio transport
- Active development and good documentation
- Reduces boilerplate compared to raw MCP SDK

**Alternatives Considered**:
- Raw MCP Python SDK: More verbose, requires manual schema definition
- Custom implementation: Reinventing the wheel, more maintenance burden

### Pydantic for Validation

**Decision**: Use Pydantic v2 for data validation and serialization

**Rationale**:
- Native FastMCP integration
- Automatic JSON schema generation for MCP tool parameters
- Type-safe models with runtime validation
- Clean serialization to JSON for file persistence

**Alternatives Considered**:
- attrs: Less ecosystem support for MCP integration
- dataclasses: No built-in validation or schema generation
- marshmallow: More verbose, older API

### Storage Strategy

**Decision**: In-memory storage with JSON file persistence

**Rationale**:
- No external database dependency for initial implementation
- Fast access for <1000 questions (meets performance goals)
- JSON files are human-readable and version-controllable
- Simple backup/restore via file copy
- Easy to migrate to database later if needed

**Alternatives Considered**:
- SQLite: Adds complexity, overkill for current scope
- Redis: Requires external service, not needed for single-user context
- In-memory only: Data lost on restart, poor user experience

### Testing Strategy

**Decision**: pytest with pytest-asyncio

**Rationale**:
- Standard Python testing framework
- Native async support for testing MCP tools
- Rich plugin ecosystem (cov, fixtures, parametrize)
- Clear assertion syntax
- Works with TDD workflow

**Alternatives Considered**:
- unittest: More verbose, less flexible fixtures
- nose2: Less actively maintained

### Linting and Type Checking

**Decision**: ruff (linting) + mypy (type checking)

**Rationale**:
- ruff is fast and comprehensive (replaces flake8, isort, black)
- mypy is the de facto standard for Python type checking
- Both integrate well with CI/CD pipelines
- Aligns with constitution static analysis requirements

**Alternatives Considered**:
- flake8 + isort + black: Multiple tools, slower
- pyright: Good but mypy has wider adoption

## MCP Integration Patterns

### Tool Definitions

Each MCP tool follows this pattern:
1. Decorator `@mcp.tool()` registers the function
2. Pydantic models define parameter schemas (auto-generated)
3. Return type hints define response schema
4. Errors returned as structured error responses

### Resource URIs

Pattern: `question://{id}`
- Dynamic resources registered via `@mcp.resource()`
- URI templates support pattern matching
- Content negotiation for JSON vs Markdown formats

### Error Handling

Standard MCP error codes:
- Invalid params: Tool called with wrong arguments
- Internal error: Unexpected server error
- Not found: Resource/tool target doesn't exist

## Best Practices Identified

1. **Tool Granularity**: One tool per operation (CRUD pattern)
2. **Model Isolation**: Separate Pydantic models from storage logic
3. **Resource Templates**: Use URI templates for dynamic resources
4. **Validation Layer**: Validate at model boundaries, trust internally
5. **Testing Layers**: Unit tests for models/store, integration tests for tools, contract tests for MCP interface

## Open Questions (Resolved)

All technical questions resolved from spec. No NEEDS CLARIFICATION items remain.