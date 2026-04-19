# 05 - SDK Tools RBAC

Servidor MCP low-level con control de acceso por rol. Usa el SDK oficial (`mcp.server.Server`), no FastMCP.

## Requisitos

- Python 3.10+

## Preparacion

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

```bash
python client.py --role viewer
python client.py --role operator
python client.py --role admin
```

## Como funciona

- El servidor usa `@server.list_tools()` y `@server.call_tool()` del SDK low-level.
- La variable de entorno `MCP_ROLE` controla que tools estan permitidas.
- El cliente pasa el rol como argumento y lo inyecta en el entorno del servidor.

## Permisos por rol

| Tool | viewer | operator | admin |
|------|--------|----------|-------|
| `list_users` | si | si | si |
| `get_config` | si | si | si |
| `create_user` | no | si | si |
| `reset_password` | no | si | si |
| `delete_user` | no | no | si |
| `update_config` | no | no | si |