# 02 - FastMCP Resources Basico

Servidor FastMCP con resources estaticos y dinamicos + cliente Python por stdio.

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

- `server.py` declara resources con `@mcp.resource(...)`.
- Los resources dinamcos (`product://{sku}`, `kb://{topic}`) se leen por URI directa.
- Los resources estaticos (`config://app`) tambien aparecen en `list_resources`.

## Resources disponibles

| URI | Descripcion |
|-----|-------------|
| `config://app` | Configuracion de la app |
| `product://{sku}` | Producto por SKU |
| `kb://{topic}` | Nota de knowledge base |