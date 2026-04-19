from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone

import mcp.types as types
from mcp.server import Server
from mcp.server.lowlevel.helper_types import ReadResourceContents
from mcp.server.stdio import stdio_server

server = Server("sdk-prompts-resources-lowlevel")

CATALOG = {
    "widgets": {"name": "Widgets A", "stock": 150, "price": 9.99},
    "gadgets": {"name": "Gadgets B", "stock": 42, "price": 24.50},
}

NOTES = {
    "arq-microservicios": "Los microservicios dividen monolitos en servicios independientes con API propia.",
    "arq-monolito": "Un monolito une toda la logica en una sola unidad de despliegue.",
    "dev-container": "Los contenedores aislan dependencias y garantizan reproducibilidad.",
}

SYSTEM_STATUS = {
    "version": "1.0.0",
    "uptime": "42d",
    "last_check": datetime.now(timezone.utc).isoformat(),
}


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_catalog",
            description="Busca en el catalogo de productos",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        ),
        types.Tool(
            name="add_to_cart",
            description="Anade un producto al carrito",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "string"},
                    "qty": {"type": "integer"},
                },
                "required": ["product_id", "qty"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "search_catalog":
        query = arguments["query"].lower()
        results = {
            k: v for k, v in CATALOG.items() if query in k or query in v["name"].lower()
        }
        return [
            types.TextContent(
                type="text",
                text=json.dumps(results, indent=2) if results else "Sin resultados",
            )
        ]

    if name == "add_to_cart":
        pid = arguments["product_id"]
        if pid not in CATALOG:
            return [
                types.TextContent(type="text", text=f"Producto '{pid}' no encontrado")
            ]
        return [
            types.TextContent(
                type="text",
                text=f"Anadido al carrito: {CATALOG[pid]['name']} x{arguments['qty']}",
            )
        ]

    return [types.TextContent(type="text", text=f"Tool desconocida: {name}")]


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri="system://status", name="system-status", mimeType="application/json"
        ),
    ]


@server.list_resource_templates()
async def handle_list_resource_templates() -> list[types.ResourceTemplate]:
    return [
        types.ResourceTemplate(
            uriTemplate="catalog://{product_id}",
            name="catalog-product",
            mimeType="application/json",
        ),
        types.ResourceTemplate(
            uriTemplate="notes://{topic}", name="dev-notes", mimeType="text/plain"
        ),
    ]


@server.read_resource()
async def handle_read_resource(uri) -> object:
    uri_str = str(uri)
    if uri_str == "system://status":
        return [
            ReadResourceContents(
                content=json.dumps(SYSTEM_STATUS, indent=2),
                mime_type="application/json",
            )
        ]
    if uri_str.startswith("catalog://"):
        pid = uri_str[len("catalog://") :]
        if pid in CATALOG:
            return [
                ReadResourceContents(
                    content=json.dumps(CATALOG[pid], indent=2),
                    mime_type="application/json",
                )
            ]
        return [
            ReadResourceContents(
                content=json.dumps({"error": f"Producto '{pid}' no encontrado"}),
                mime_type="application/json",
            )
        ]
    if uri_str.startswith("notes://"):
        topic = uri_str[len("notes://") :]
        if topic in NOTES:
            return [ReadResourceContents(content=NOTES[topic], mime_type="text/plain")]
        return [
            ReadResourceContents(
                content=f"Nota '{topic}' no encontrada. Topics: {', '.join(sorted(NOTES))}",
                mime_type="text/plain",
            )
        ]
    return [
        ReadResourceContents(
            content=f"Recurso no encontrado: {uri}", mime_type="text/plain"
        )
    ]


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="technical-review",
            description="Genera un prompt para revision tecnica",
            arguments=[
                types.PromptArgument(
                    name="topic", description="Topic a revisar", required=True
                ),
                types.PromptArgument(
                    name="depth",
                    description="Nivel de detalle (basic/advanced)",
                    required=False,
                ),
            ],
        ),
        types.Prompt(
            name="product-summary",
            description="Genera un prompt para resumen de producto",
            arguments=[
                types.PromptArgument(
                    name="product_id", description="ID del producto", required=True
                ),
            ],
        ),
    ]


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    args = arguments or {}
    if name == "technical-review":
        topic = args.get("topic", "general")
        depth = args.get("depth", "basic")
        return types.GetPromptResult(
            description=f"Revision tecnica de {topic}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=(
                            f"Haz una revision tecnica (nivel: {depth}) sobre '{topic}'.\n"
                            "Incluye: pros, contras, cuando usar, cuando evitar.\n"
                            "Si existe, consulta la nota: notes://{topic}"
                        ),
                    ),
                )
            ],
        )
    if name == "product-summary":
        pid = args.get("product_id", "")
        return types.GetPromptResult(
            description=f"Resumen de producto {pid}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=(
                            f"Genera un resumen del producto '{pid}'.\n"
                            f"Consulta catalog://{pid} para los datos completos.\n"
                            "Incluye recomendacion de compra segun stock y precio."
                        ),
                    ),
                )
            ],
        )
    raise ValueError(f"Prompt desconocido: {name}")


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
