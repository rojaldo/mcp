from __future__ import annotations

import asyncio
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


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


async def main() -> None:
    url = "http://127.0.0.1:8000/mcp"

    async with streamablehttp_client(url) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools disponibles:")
            for tool in getattr(tools, "tools", []):
                print(f"  - {tool.name}: {tool.description}")

            print("\nEjecutando tarea_larga(pasos=5)...")
            result = await session.call_tool("tarea_larga", {"pasos": 5})
            print(f"Resultado: {_extract_text(result)}")

            print("\nEjecutando analisis_datos(filas=10)...")
            result = await session.call_tool("analisis_datos", {"filas": 10})
            print(f"Resultado: {_extract_text(result)}")


if __name__ == "__main__":
    asyncio.run(main())
