from __future__ import annotations

import asyncio
import json
import sqlite3

import mcp.types as types
from mcp.server import Server
from mcp.server.lowlevel.helper_types import ReadResourceContents
from mcp.server.stdio import stdio_server

server = Server("sdk-sqlite-crud")

DB = sqlite3.connect(":memory:")
DB.execute(
    "CREATE TABLE IF NOT EXISTS tasks "
    "(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, completed INTEGER DEFAULT 0)"
)
DB.commit()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="create_task",
            description="Crea una tarea",
            inputSchema={
                "type": "object",
                "properties": {"title": {"type": "string"}},
                "required": ["title"],
            },
        ),
        types.Tool(
            name="list_tasks",
            description="Lista todas las tareas",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="complete_task",
            description="Marca una tarea como completada",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "integer"}},
                "required": ["id"],
            },
        ),
        types.Tool(
            name="delete_task",
            description="Elimina una tarea",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "integer"}},
                "required": ["id"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "create_task":
        DB.execute("INSERT INTO tasks (title) VALUES (?)", (arguments["title"],))
        DB.commit()
        row = DB.execute("SELECT last_insert_rowid()").fetchone()
        return [
            types.TextContent(
                type="text",
                text=f"Tarea creada: id={row[0]}, title='{arguments['title']}'",
            )
        ]

    if name == "list_tasks":
        rows = DB.execute("SELECT id, title, completed FROM tasks").fetchall()
        lines = [f"  {r[0]}: {r[1]} {'[DONE]' if r[2] else '[TODO]'}" for r in rows]
        if not lines:
            return [types.TextContent(type="text", text="No hay tareas")]
        return [types.TextContent(type="text", text="Tareas:\n" + "\n".join(lines))]

    if name == "complete_task":
        DB.execute("UPDATE tasks SET completed=1 WHERE id=?", (arguments["id"],))
        DB.commit()
        return [
            types.TextContent(type="text", text=f"Tarea {arguments['id']} completada")
        ]

    if name == "delete_task":
        DB.execute("DELETE FROM tasks WHERE id=?", (arguments["id"],))
        DB.commit()
        return [
            types.TextContent(type="text", text=f"Tarea {arguments['id']} eliminada")
        ]

    return [types.TextContent(type="text", text=f"Tool desconocida: {name}")]


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri="tasks://all", name="all-tasks", mimeType="application/json"
        ),
    ]


@server.list_resource_templates()
async def handle_list_resource_templates() -> list[types.ResourceTemplate]:
    return [
        types.ResourceTemplate(
            uriTemplate="tasks://{status}",
            name="tasks-by-status",
            mimeType="application/json",
        ),
    ]


@server.read_resource()
async def handle_read_resource(uri) -> object:
    uri_str = str(uri)
    if uri_str == "tasks://all":
        rows = DB.execute("SELECT id, title, completed FROM tasks").fetchall()
        data = [{"id": r[0], "title": r[1], "completed": bool(r[2])} for r in rows]
        return [
            ReadResourceContents(
                content=json.dumps(data, indent=2), mime_type="application/json"
            )
        ]

    if uri_str.startswith("tasks://"):
        status = uri_str[len("tasks://") :]
        if status in ("todo", "done"):
            completed = 1 if status == "done" else 0
            rows = DB.execute(
                "SELECT id, title, completed FROM tasks WHERE completed=?", (completed,)
            ).fetchall()
            data = [{"id": r[0], "title": r[1], "completed": bool(r[2])} for r in rows]
            return [
                ReadResourceContents(
                    content=json.dumps(data, indent=2), mime_type="application/json"
                )
            ]

    return [
        ReadResourceContents(
            content=json.dumps({"error": f"Recurso no encontrado: {uri}"}),
            mime_type="application/json",
        )
    ]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
