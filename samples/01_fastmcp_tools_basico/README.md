# 01 - FastMCP Tools Basico

Servidor FastMCP con tools + cliente Python por stdio. Opcionalmente usa Ollama para elegir la tool desde lenguaje natural.

## Requisitos

- Python 3.10+
- Ollama local (opcional, para `--question`)

## Preparacion

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

```bash
python client.py
```

Con Ollama planner:

```bash
python client.py --question "Cuanto es 17 + 25"
OLLAMA_MODEL=qwen3.5 python client.py --question "Palabras clave de: MCP conecta LLMs con herramientas"
```

## Como funciona

- `server.py` declara tools con `@mcp.tool()`.
- `client.py` arranca el servidor por stdio, lista tools y las ejecuta.
- Con `--question`, Ollama genera un JSON con tool + argumentos.

## Tools disponibles

| Tool | Descripcion |
|------|-------------|
| `sumar(a, b)` | Suma dos numeros |
| `normalizar_texto(texto)` | Trim + lowercase + espacios simples |
| `extraer_keywords(texto, max_keywords)` | Keywords por frecuencia |