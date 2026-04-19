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
        command=sys.executable, args=[str(base_dir / "server.py")]
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools disponibles:")
            for tool in getattr(tools, "tools", []):
                print(f"  - {tool.name}: {tool.description}")

            print("\nCreando tareas...")
            for title in ["Aprender MCP", "Implementar servidor", "Escribir tests"]:
                r = await session.call_tool("create_task", {"title": title})
                print(f"  {_extract_text(r)}")

            print("\nListando tareas:")
            r = await session.call_tool("list_tasks", {})
            print(_extract_text(r))

            print("\nCompletando tarea 2:")
            r = await session.call_tool("complete_task", {"id": 2})
            print(_extract_text(r))

            print("\nResource tasks://all:")
            r = await session.read_resource("tasks://all")
            print(_readable_content(r))

            print("\nResource tasks://done:")
            r = await session.read_resource("tasks://done")
            print(_readable_content(r))

            print("\nEliminando tarea 1:")
            r = await session.call_tool("delete_task", {"id": 1})
            print(_extract_text(r))

            print("\nTareas finales:")
            r = await session.call_tool("list_tasks", {})
            print(_extract_text(r))


if __name__ == "__main__":
    asyncio.run(main())
