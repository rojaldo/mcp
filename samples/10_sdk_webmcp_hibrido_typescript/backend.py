from __future__ import annotations

import asyncio
import json

import mcp.types as types
from mcp.server import Server
from mcp.server.lowlevel.helper_types import ReadResourceContents
from mcp.server.stdio import stdio_server

server = Server("sdk-webmcp-backend")

CART: list[dict[str, str | int]] = []
PRODUCTS_BACKEND = {
    "widget-a": {"name": "Widget A", "price": 9.99, "stock": 100},
    "gadget-b": {"name": "Gadget B", "price": 24.50, "stock": 42},
    "tool-c": {"name": "Tool C", "price": 15.00, "stock": 75},
}
AUDIT_LOG: list[dict[str, str]] = []


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="sync_cart",
            description="Sincroniza carrito del frontend con el backend",
            inputSchema={
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "qty": {"type": "integer"},
                            },
                        },
                    }
                },
                "required": ["items"],
            },
        ),
        types.Tool(
            name="checkout",
            description="Procesa el checkout del carrito actual",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="check_stock",
            description="Consulta stock de un producto",
            inputSchema={
                "type": "object",
                "properties": {"product_id": {"type": "string"}},
                "required": ["product_id"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "sync_cart":
        CART.clear()
        for item in arguments["items"]:
            CART.append({"name": item["name"], "qty": item["qty"]})
        AUDIT_LOG.append({"action": "sync_cart", "count": str(len(CART))})
        return [
            types.TextContent(
                type="text", text=f"Carrito sincronizado: {len(CART)} items"
            )
        ]

    if name == "checkout":
        if not CART:
            return [types.TextContent(type="text", text="Carrito vacio")]
        total = 0.0
        for item in CART:
            pid = item["name"].lower().replace(" ", "-")
            product = PRODUCTS_BACKEND.get(pid, {"price": 0})
            total += product["price"] * item["qty"]
        AUDIT_LOG.append({"action": "checkout", "total": f"{total:.2f}"})
        CART.clear()
        return [
            types.TextContent(
                type="text", text=f"Checkout completado. Total: ${total:.2f}"
            )
        ]

    if name == "check_stock":
        pid = arguments["product_id"]
        product = PRODUCTS_BACKEND.get(pid)
        if not product:
            return [
                types.TextContent(type="text", text=f"Producto '{pid}' no encontrado")
            ]
        return [
            types.TextContent(
                type="text",
                text=f"{product['name']}: stock={product['stock']}, precio=${product['price']}",
            )
        ]

    return [types.TextContent(type="text", text=f"Tool desconocida: {name}")]


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri="catalog://all", name="full-catalog", mimeType="application/json"
        ),
        types.Resource(
            uri="audit://log", name="audit-log", mimeType="application/json"
        ),
    ]


@server.read_resource()
async def handle_read_resource(uri) -> object:
    uri_str = str(uri)
    if uri_str == "catalog://all":
        return [
            ReadResourceContents(
                content=json.dumps(PRODUCTS_BACKEND, indent=2),
                mime_type="application/json",
            )
        ]
    if uri_str == "audit://log":
        return [
            ReadResourceContents(
                content=json.dumps(AUDIT_LOG, indent=2), mime_type="application/json"
            )
        ]
    return [
        ReadResourceContents(
            content=f"Recurso no encontrado: {uri}", mime_type="text/plain"
        )
    ]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
