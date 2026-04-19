from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _extract_text(value: object) -> str:
    if hasattr(value, "text"):
        return str(value.text)
    if hasattr(value, "content"):
        parts = []
        for item in value.content:
            if hasattr(item, "text"):
                parts.append(str(item.text))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    return str(value)


def _readable_content(read_response: object) -> str:
    items = []
    if hasattr(read_response, "contents"):
        items = list(read_response.contents)
    elif hasattr(read_response, "content"):
        items = list(read_response.content)
    lines = []
    for item in items:
        if hasattr(item, "text"):
            lines.append(str(item.text))
        else:
            lines.append(str(item))
    return "\n".join(lines) if lines else str(read_response)


async def main() -> None:
    base_dir = Path(__file__).resolve().parent
    params = StdioServerParameters(
        command=sys.executable, args=[str(base_dir / "backend.py")]
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools del backend MCP:")
            for t in getattr(tools, "tools", []):
                print(f"  - {t.name}: {t.description}")

            resources = await session.list_resources()
            print("\nResources del backend:")
            for r in getattr(resources, "resources", []):
                print(f"  - {r.name}: {r.uri}")

            print("\n--- Demo del backend ---")

            print("\nCheck stock widget-a:")
            r = await session.call_tool("check_stock", {"product_id": "widget-a"})
            print(_extract_text(r))

            print("\nSync cart:")
            r = await session.call_tool(
                "sync_cart",
                {
                    "items": [
                        {"name": "Widget A", "qty": 2},
                        {"name": "Gadget B", "qty": 1},
                    ]
                },
            )
            print(_extract_text(r))

            print("\nCheckout:")
            r = await session.call_tool("checkout", {})
            print(_extract_text(r))

            print("\nAudit log:")
            r = await session.read_resource("audit://log")
            print(_readable_content(r))

            print("\nCatalog:")
            r = await session.read_resource("catalog://all")
            print(_readable_content(r))


if __name__ == "__main__":
    asyncio.run(main())
