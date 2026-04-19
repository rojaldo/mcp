# 03 - FastMCP Prompts + Ollama

Servidor FastMCP con prompts parametrizables + cliente que renderiza y opcionalmente ejecuta en Ollama local.

## Requisitos

- Python 3.10+
- Ollama local (opcional, para `--run-llm`)

## Preparacion

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

Solo generar prompt renderizado:

```bash
python client.py
```

Generar y ejecutar en Ollama:

```bash
python client.py --run-llm
OLLAMA_MODEL=qwen3.5 python client.py --run-llm
```

## Prompts disponibles

| Prompt | Parametros |
|--------|------------|
| `resumen_tecnico` | `tema`, `audiencia` (opcional) |
| `plan_migracion` | `sistema_actual`, `objetivo` |