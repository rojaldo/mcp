from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

TASKS_DB: dict[int, dict[str, str]] = {
    1: {"title": "Disenar API", "status": "done"},
    2: {"title": "Implementar backend", "status": "in_progress"},
    3: {"title": "Escribir tests", "status": "pending"},
}


@asynccontextmanager
async def lifespan(server: Server):
    yield {"tasks": TASKS_DB}


server = Server("sdk-multiagent-mcp", lifespan=lifespan)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_tasks",
            description="Lista todas las tareas del proyecto",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="get_task",
            description="Obtiene detalle de una tarea por ID",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "integer"}},
                "required": ["id"],
            },
        ),
        types.Tool(
            name="update_task",
            description="Actualiza estado de una tarea",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "status": {
                        "type": "string",
                        "description": "pending, in_progress, done",
                    },
                },
                "required": ["id", "status"],
            },
        ),
        types.Tool(
            name="create_task",
            description="Crea una nueva tarea",
            inputSchema={
                "type": "object",
                "properties": {"title": {"type": "string"}},
                "required": ["title"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    ctx = server.request_context
    tasks = ctx.lifespan_context["tasks"]

    if name == "list_tasks":
        lines = [f"  {k}: {v['title']} [{v['status']}]" for k, v in tasks.items()]
        return [types.TextContent(type="text", text="Tareas:\n" + "\n".join(lines))]

    if name == "get_task":
        tid = arguments["id"]
        task = tasks.get(tid)
        if not task:
            return [types.TextContent(type="text", text=f"Tarea {tid} no encontrada")]
        return [
            types.TextContent(
                type="text", text=f"Tarea {tid}: {task['title']} [{task['status']}]"
            )
        ]

    if name == "update_task":
        tid = arguments["id"]
        if tid not in tasks:
            return [types.TextContent(type="text", text=f"Tarea {tid} no encontrada")]
        tasks[tid]["status"] = arguments["status"]
        return [
            types.TextContent(
                type="text", text=f"Tarea {tid} actualizada a '{arguments['status']}'"
            )
        ]

    if name == "create_task":
        new_id = max(tasks.keys()) + 1 if tasks else 1
        tasks[new_id] = {"title": arguments["title"], "status": "pending"}
        return [
            types.TextContent(
                type="text", text=f"Tarea creada: {new_id}: {arguments['title']}"
            )
        ]

    return [types.TextContent(type="text", text=f"Tool desconocida: {name}")]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
