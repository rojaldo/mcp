from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _iter_resources(resources_response: Any) -> list[Any]:
    if hasattr(resources_response, "resources"):
        return list(resources_response.resources)
    if isinstance(resources_response, list):
        return resources_response
    return []


def _readable_content(read_response: Any) -> str:
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
        command=sys.executable, args=[str(base_dir / "server.py")]
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            resources = await session.list_resources()
            print("Resources disponibles:")
            for r in _iter_resources(resources):
                uri = getattr(r, "uri", "<sin-uri>")
                name = getattr(r, "name", "<sin-name>")
                print(f"  - {name}: {uri}")

            for uri in ["config://app", "product://mcp-101", "kb://resources"]:
                result = await session.read_resource(uri)
                print(f"\nContenido de {uri}:\n{_readable_content(result)}")


if __name__ == "__main__":
    asyncio.run(main())
