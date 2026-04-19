# Curso MCP - Model Context Protocol

Repositorio del curso sobre MCP (Model Context Protocol), WebMCP y FastMCP.

## Estructura

```
mcp/
├── docs/          # Documentacion del curso (slides, guias, ejercicios)
├── samples/       # 10 ejemplos funcionales de MCP
└── .gitignore
```

## Documentacion (`docs/`)

| Archivo | Descripcion |
|---------|-------------|
| `slides_v6.md` / `.html` | Slides principales del curso (MCP + WebMCP) |
| `mcp_python.md` / `.html` | Guia completa del SDK Python |
| `fast_mcp_slides.md` / `.html` | Slides especificos de FastMCP |
| `mcp_typescript.md` / `.html` | Guia del SDK TypeScript |
| `buenas_practicas.md` / `.html` | Buenas practicas MCP |
| `awesome.md` / `.html` | Recursos y enlaces destacados |
| `mcp_python_exercises.*` | Ejercicios practicos del SDK Python |
| `temario.adoc` | Temario del curso |

Los archivos `.adoc` son fuentes AsciiDoc; los `.md` y `.html` son versiones generadas.

## Ejemplos (`samples/`)

10 ejemplos funcionales, autocontenidos, con `README.md` y `requirements.txt` propios.

### FastMCP (01-04)

| # | Carpeta | Demuestra |
|---|---------|-----------|
| 01 | `01_fastmcp_tools_basico` | Tools con `@mcp.tool()` + cliente stdio + Ollama planner |
| 02 | `02_fastmcp_resources_basico` | Resources estaticos/dinamicos con `@mcp.resource()` |
| 03 | `03_fastmcp_prompts_ollama` | Prompts con `@mcp.prompt()` + ejecucion Ollama |
| 04 | `04_fastmcp_http_progress` | Streamable HTTP + progreso con `Context` |

### SDK Oficial Low-Level (05-10)

| # | Carpeta | Demuestra |
|---|---------|-----------|
| 05 | `05_sdk_tools_rbac` | Tools con RBAC (viewer/operator/admin) |
| 06 | `06_sdk_sqlite_memory_crud` | CRUD con SQLite `:memory:` + resources |
| 07 | `07_sdk_prompts_resources_lowlevel` | Tools + resources + prompts low-level |
| 08 | `08_sdk_rag_memory_langchain_ollama` | RAG local con embeddings Ollama en memoria |
| 09 | `09_sdk_multiagent_crewai` | Orquestacion multiagente con Ollama (planner/executor/verifier) |
| 10 | `10_sdk_webmcp_hibrido_typescript` | WebMCP (TypeScript) + backend MCP low-level |

## Requisitos generales

- **Python 3.10+**
- **Ollama local** para ejemplos que usan LLM (03, 08, 09)
- **Node.js 18+** para compilar TypeScript (ejemplo 10)
- **Navegador con WebMCP experimental** (ejemplo 10)

## Convenciones

- Cada ejemplo tiene su propio `requirements.txt` y venv aislado.
- Proveedor de inferencia: Ollama local (`OLLAMA_MODEL` configurable).
- Sin contenedores, sin bases de datos externas, almacenamiento en memoria.

## Inicio rapido

```bash
cd samples/01_fastmcp_tools_basico
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python client.py
```

Ver el `README.md` de cada ejemplo para instrucciones especificas.