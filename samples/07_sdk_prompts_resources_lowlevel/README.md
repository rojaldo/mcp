# 07 - SDK Prompts + Resources Low-Level

Servidor MCP low-level que implementa las tres primitivas (tools, resources, prompts) usando el SDK oficial.

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

- Usa `mcp.server.Server` con decoradores low-level para las 3 primitivas.
- Compara directamente con los ejemplos FastMCP (01-03) para ver la diferencia de API.
- Muestra como resources y prompts pueden referenciarse mutuamente en las plantillas.

## Comparacion con FastMCP

| Aspecto | FastMCP | SDK Low-Level |
|---------|---------|---------------|
| Decorador tools | `@mcp.tool()` | `@server.list_tools()` + `@server.call_tool()` |
| Decorador resources | `@mcp.resource("uri")` | `@server.list_resources()` + `@server.read_resource()` |
| Decorador prompts | `@mcp.prompt()` | `@server.list_prompts()` + `@server.get_prompt()` |
| Schema | Auto (type hints) | Manual (JSON Schema dict) |
| Transporte | `mcp.run()` | `server.run()` + `stdio_server()` |

## APIs expuestas

- **Tools**: `search_catalog`, `add_to_cart`
- **Resources**: `system://status`, `catalog://{product_id}`, `notes://{topic}`
- **Prompts**: `technical-review`, `product-summary`