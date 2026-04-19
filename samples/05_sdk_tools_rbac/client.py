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


async def run(role_env: str) -> None:
    base_dir = Path(__file__).resolve().parent
    env = {"MCP_ROLE": role_env}
    params = StdioServerParameters(
        command=sys.executable, args=[str(base_dir / "server.py")], env=env
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print(f"Rol: {role_env}")
            print("Tools permitidas:")
            for tool in getattr(tools, "tools", []):
                print(f"  - {tool.name}: {tool.description}")

            print("\nEjecutando list_users:")
            result = await session.call_tool("list_users", {})
            print(_extract_text(result))

            if role_env in ("admin", "operator"):
                print("\nEjecutando create_user:")
                result = await session.call_tool(
                    "create_user", {"name": "dave", "role": "viewer"}
                )
                print(_extract_text(result))

            if role_env == "admin":
                print("\nEjecutando update_config:")
                result = await session.call_tool(
                    "update_config", {"key": "log_level", "value": "DEBUG"}
                )
                print(_extract_text(result))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Cliente MCP - RBAC")
    parser.add_argument(
        "--role", type=str, default="viewer", choices=["viewer", "operator", "admin"]
    )
    args = parser.parse_args()
    asyncio.run(run(role_env=args.role))


if __name__ == "__main__":
    main()
