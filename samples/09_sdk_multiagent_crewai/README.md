# 09 - SDK Multiagente con Ollama

Servidor MCP low-level de gestion de tareas + orquestacion multiagente con 3 roles (planificador, ejecutor, verificador) usando Ollama local.

## Requisitos

- Python 3.10+
- Ollama local corriendo con un modelo de chat descargado

## Preparacion

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.2
```

## Ejecucion

```bash
python client.py
OLLAMA_MODEL=qwen3.5 python client.py
```

## Como funciona

- `server.py`: servidor MCP low-level con CRUD de tareas y `lifespan` para compartir estado.
- `client.py`: implementa 3 agentes secuenciales:
  1. **Planificador**: usa Ollama para analizar el estado y decidir la siguiente accion.
  2. **Ejecutor**: invoca la tool MCP correspondiente al plan.
  3. **Verificador**: usa Ollama para validar coherencia del estado final.

## Tools disponibles

| Tool | Descripcion |
|------|-------------|
| `list_tasks` | Lista todas las tareas |
| `get_task(id)` | Detalle de una tarea |
| `update_task(id, status)` | Cambia estado (pending/in_progress/done) |
| `create_task(title)` | Crea nueva tarea |