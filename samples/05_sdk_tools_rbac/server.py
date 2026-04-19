from __future__ import annotations

import asyncio
import os

import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

server = Server("sdk-tools-rbac")

ROLES_TOOLS: dict[str, list[str]] = {
    "viewer": ["list_users", "get_config"],
    "operator": ["list_users", "get_config", "create_user", "reset_password"],
    "admin": [
        "list_users",
        "get_config",
        "create_user",
        "reset_password",
        "delete_user",
        "update_config",
    ],
}

USERS: list[dict[str, str]] = [
    {"id": "1", "name": "alice", "role": "admin"},
    {"id": "2", "name": "bob", "role": "operator"},
    {"id": "3", "name": "carol", "role": "viewer"},
]

CONFIG: dict[str, str] = {"env": "local", "log_level": "INFO"}

ALL_TOOLS = [
    types.Tool(
        name="list_users",
        description="Lista todos los usuarios",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="get_config",
        description="Obtiene configuracion del sistema",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="create_user",
        description="Crea un nuevo usuario",
        inputSchema={
            "type": "object",
            "properties": {"name": {"type": "string"}, "role": {"type": "string"}},
            "required": ["name", "role"],
        },
    ),
    types.Tool(
        name="reset_password",
        description="Resetea password de un usuario",
        inputSchema={
            "type": "object",
            "properties": {"user_id": {"type": "string"}},
            "required": ["user_id"],
        },
    ),
    types.Tool(
        name="delete_user",
        description="Elimina un usuario",
        inputSchema={
            "type": "object",
            "properties": {"user_id": {"type": "string"}},
            "required": ["user_id"],
        },
    ),
    types.Tool(
        name="update_config",
        description="Actualiza configuracion",
        inputSchema={
            "type": "object",
            "properties": {"key": {"type": "string"}, "value": {"type": "string"}},
            "required": ["key", "value"],
        },
    ),
]


def _get_role() -> str:
    return os.getenv("MCP_ROLE", "admin")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    role = _get_role()
    allowed = ROLES_TOOLS.get(role, [])
    return [t for t in ALL_TOOLS if t.name in allowed]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    role = _get_role()
    allowed = ROLES_TOOLS.get(role, [])
    if name not in allowed:
        return [
            types.TextContent(
                type="text", text=f"ERROR: rol '{role}' no tiene permiso para '{name}'"
            )
        ]

    if name == "list_users":
        lines = [f"  {u['id']}: {u['name']} ({u['role']})" for u in USERS]
        return [types.TextContent(type="text", text="Usuarios:\n" + "\n".join(lines))]

    if name == "get_config":
        return [types.TextContent(type="text", text=f"Config: {CONFIG}")]

    if name == "create_user":
        new_id = str(len(USERS) + 1)
        USERS.append(
            {"id": new_id, "name": arguments["name"], "role": arguments["role"]}
        )
        return [
            types.TextContent(
                type="text",
                text=f"Usuario creado: {arguments['name']} ({arguments['role']})",
            )
        ]

    if name == "reset_password":
        uid = arguments["user_id"]
        user = next((u for u in USERS if u["id"] == uid), None)
        if not user:
            return [
                types.TextContent(
                    type="text", text=f"ERROR: usuario {uid} no encontrado"
                )
            ]
        return [
            types.TextContent(
                type="text", text=f"Password reseteado para {user['name']}"
            )
        ]

    if name == "delete_user":
        uid = arguments["user_id"]
        idx = next((i for i, u in enumerate(USERS) if u["id"] == uid), None)
        if idx is None:
            return [
                types.TextContent(
                    type="text", text=f"ERROR: usuario {uid} no encontrado"
                )
            ]
        removed = USERS.pop(idx)
        return [
            types.TextContent(type="text", text=f"Usuario eliminado: {removed['name']}")
        ]

    if name == "update_config":
        CONFIG[arguments["key"]] = arguments["value"]
        return [types.TextContent(type="text", text=f"Config actualizada: {CONFIG}")]

    return [types.TextContent(type="text", text=f"Tool desconocida: {name}")]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
