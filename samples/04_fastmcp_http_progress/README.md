# 04 - FastMCP Streamable HTTP + Progreso

Servidor FastMCP con transporte HTTP stateless + tools con reporte de progreso via `Context`.

## Requisitos

- Python 3.10+

## Preparacion

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

1. Arranca el servidor en una terminal:

```bash
python server.py
```

2. En otra terminal, ejecuta el cliente:

```bash
source .venv/bin/activate
python client.py
```

## Como funciona

- `server.py` usa `stateless_http=True` y `json_response=True` para transporte HTTP.
- Las tools usan `Context.report_progress()` para enviar notificaciones de progreso.
- `client.py` se conecta via `streamablehttp_client` al endpoint `/mcp`.

## Tools disponibles

| Tool | Descripcion |
|------|-------------|
| `tarea_larga(pasos)` | Tarea con progreso paso a paso |
| `analisis_datos(filas)` | Simula analisis con progreso porcentual |