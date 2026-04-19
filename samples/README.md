# Samples MCP

Coleccion de 10 ejemplos funcionales para demostrar capacidades MCP.

## FastMCP (ejemplos 01-04)

| # | Ejemplo | Demuestra |
|---|---------|-----------|
| 01 | `01_fastmcp_tools_basico` | Tools con `@mcp.tool()` + cliente stdio + Ollama planner |
| 02 | `02_fastmcp_resources_basico` | Resources estaticos/dinamicos con `@mcp.resource()` |
| 03 | `03_fastmcp_prompts_ollama` | Prompts con `@mcp.prompt()` + ejecucion Ollama |
| 04 | `04_fastmcp_http_progress` | Streamable HTTP + progreso con `Context` |

## SDK Oficial Low-Level (ejemplos 05-10)

| # | Ejemplo | Demuestra |
|---|---------|-----------|
| 05 | `05_sdk_tools_rbac` | Tools con RBAC (viewer/operator/admin) |
| 06 | `06_sdk_sqlite_memory_crud` | CRUD con SQLite `:memory:` + resources |
| 07 | `07_sdk_prompts_resources_lowlevel` | Tools + resources + prompts low-level |
| 08 | `08_sdk_rag_memory_langchain_ollama` | RAG local con embeddings Ollama en memoria |
| 09 | `09_sdk_multiagent_crewai` | Orquestacion multiagente con Ollama (planner/executor/verifier) |
| 10 | `10_sdk_webmcp_hibrido_typescript` | WebMCP (TS) + backend MCP low-level |

## Convenciones

- Cada carpeta tiene `README.md` + `requirements.txt`.
- Proveedor de inferencia: Ollama local (`OLLAMA_MODEL` configurable).
- Sin contenedores, sin BD externa, almacenamiento en memoria.
