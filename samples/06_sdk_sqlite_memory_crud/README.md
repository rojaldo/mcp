# 06 - SDK SQLite In-Memory CRUD

Servidor MCP low-level con CRUD usando `sqlite3 :memory:` + resources de consulta.

## Requisitos

- Python 3.10+

## Preparacion

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

```bash
python client.py
```

## Como funciona

- Usa `mcp.server.Server` (SDK low-level), no FastMCP.
- Base de datos SQLite en `:memory:` — se recreate en cada ejecucion.
- Tools: CRUD de tareas; Resources: consulta por estado.
- Los resources `tasks://all` y `tasks://{status}` devuelven JSON.

## Tools

| Tool | Descripcion |
|------|-------------|
| `create_task(title)` | Crea tarea |
| `list_tasks()` | Lista todas |
| `complete_task(id)` | Marca completada |
| `delete_task(id)` | Elimina |

## Resources

| URI | Descripcion |
|-----|-------------|
| `tasks://all` | Todas las tareas (JSON) |
| `tasks://todo` | Tareas pendientes |
| `tasks://done` | Tareas completadas |