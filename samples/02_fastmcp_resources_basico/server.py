from __future__ import annotations

import json
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("fastmcp-resources-demo")

PRODUCTS = {
    "mcp-101": {
        "sku": "mcp-101",
        "name": "Curso MCP Fundamentos",
        "price": 49,
        "level": "beginner",
    },
    "mcp-301": {
        "sku": "mcp-301",
        "name": "Curso MCP Produccion",
        "price": 129,
        "level": "advanced",
    },
}

KB = {
    "tools": "Las tools permiten ejecutar acciones con parametros.",
    "resources": "Los resources exponen datos de solo lectura para el modelo.",
    "prompts": "Los prompts son plantillas reutilizables para tareas frecuentes.",
}


@mcp.resource("config://app")
def app_config() -> str:
    """Configuracion de la aplicacion demo."""
    return json.dumps(
        {
            "app": "resources-demo",
            "env": "local",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        indent=2,
    )


@mcp.resource("product://{sku}")
def get_product(sku: str) -> str:
    """Producto por SKU."""
    product = PRODUCTS.get(sku)
    if not product:
        return json.dumps({"error": f"SKU no encontrado: {sku}"}, indent=2)
    return json.dumps(product, indent=2)


@mcp.resource("kb://{topic}")
def get_kb(topic: str) -> str:
    """Nota de knowledge base por topico."""
    text = KB.get(topic.lower())
    if not text:
        return f"No existe topic '{topic}'. Disponibles: {', '.join(sorted(KB))}"
    return text


if __name__ == "__main__":
    mcp.run(transport="stdio")
