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


def _flatten_messages(prompt_result: object) -> str:
    messages = getattr(prompt_result, "messages", [])
    chunks: list[str] = []
    for msg in messages:
        role = getattr(msg, "role", "user")
        content = getattr(msg, "content", None)
        text = (
            str(content.text)
            if content is not None and hasattr(content, "text")
            else str(content)
        )
        chunks.append(f"[{role}] {text}")
    return "\n".join(chunks).strip()


async def main() -> None:
    base_dir = Path(__file__).resolve().parent
    params = StdioServerParameters(
        command=sys.executable, args=[str(base_dir / "server.py")]
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:")
            for t in getattr(tools, "tools", []):
                print(f"  - {t.name}: {t.description}")

            resources = await session.list_resources()
            print("\nResources:")
            for r in getattr(resources, "resources", []):
                print(f"  - {r.name}: {r.uri}")

            templates = await session.list_resource_templates()
            print("\nResource templates:")
            for t in getattr(templates, "resourceTemplates", []):
                print(f"  - {t.name}: {t.uriTemplate}")

            prompts = await session.list_prompts()
            print("\nPrompts:")
            for p in getattr(prompts, "prompts", []):
                print(f"  - {p.name}: {p.description}")

            print("\n--- Demo tools ---")
            r = await session.call_tool("search_catalog", {"query": "widget"})
            print(f"search_catalog('widget'): {_extract_text(r)}")

            print("\n--- Demo resources ---")
            r = await session.read_resource("system://status")
            print(f"system://status:\n{_readable_content(r)}")

            r = await session.read_resource("catalog://widgets")
            print(f"\ncatalog://widgets:\n{_readable_content(r)}")

            r = await session.read_resource("notes://arq-microservicios")
            print(f"\nnotes://arq-microservicios:\n{_readable_content(r)}")

            print("\n--- Demo prompts ---")
            r = await session.get_prompt(
                "technical-review", {"topic": "arq-microservicios", "depth": "advanced"}
            )
            print(f"technical-review:\n{_flatten_messages(r)}")

            r = await session.get_prompt("product-summary", {"product_id": "gadgets"})
            print(f"\nproduct-summary:\n{_flatten_messages(r)}")


if __name__ == "__main__":
    asyncio.run(main())
