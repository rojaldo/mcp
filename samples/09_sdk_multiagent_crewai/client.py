from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

import ollama
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


PLANNER_PROMPT = """Eres un planificador de proyectos. Analiza este estado de tareas y decide la siguiente accion.

Estado de tareas:
{tasks}

Responde SOLO con JSON: {{"action": "update_task", "id": <id>, "status": "<nuevo_status>"}}
o {{"action": "create_task", "title": "<titulo>"}} si hace falta una nueva tarea.
o {{"action": "none"}} si no hay nada que hacer.

Prioriza: pasar tareas de pending a in_progress, y de in_progress a done."""


async def run(model: str) -> None:
    base_dir = Path(__file__).resolve().parent
    params = StdioServerParameters(
        command=sys.executable, args=[str(base_dir / "server.py")]
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools del servidor MCP:")
            for t in getattr(tools, "tools", []):
                print(f"  - {t.name}: {t.description}")

            r = await session.call_tool("list_tasks", {})
            tasks_text = _extract_text(r)
            print(f"\nEstado inicial:\n{tasks_text}")

            print(f"\n--- Agente Planificador (Ollama {model}) ---")
            planner_response = ollama.chat(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "Responde solo JSON valido, sin texto adicional.",
                    },
                    {
                        "role": "user",
                        "content": PLANNER_PROMPT.format(tasks=tasks_text),
                    },
                ],
            )
            raw = planner_response["message"]["content"]
            print(f"Plan: {raw}")

            try:
                plan = json.loads(raw)
            except json.JSONDecodeError:
                print("ERROR: el planificador no devolvio JSON valido")
                return

            action = plan.get("action", "none")
            if action == "update_task":
                tid = plan["id"]
                status = plan["status"]
                print(f"\n--- Agente Ejecutor: update_task({tid}, {status}) ---")
                r = await session.call_tool(
                    "update_task", {"id": tid, "status": status}
                )
                print(_extract_text(r))
            elif action == "create_task":
                title = plan["title"]
                print(f"\n--- Agente Ejecutor: create_task({title}) ---")
                r = await session.call_tool("create_task", {"title": title})
                print(_extract_text(r))
            else:
                print("\nNo hay acciones pendientes.")

            print("\n--- Agente Verificador ---")
            r = await session.call_tool("list_tasks", {})
            final_state = _extract_text(r)
            print(f"Estado final:\n{final_state}")

            verifier_response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": "Responde solo JSON valido."},
                    {
                        "role": "user",
                        "content": f'Verifica si este estado de proyecto es coherente:\n{final_state}\n\nResponde: {{"ok": true}} o {{"ok": false, "issue": "..."}}',
                    },
                ],
            )
            print(f"Verificacion: {verifier_response['message']['content']}")


def main() -> None:
    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    asyncio.run(run(model=model))


if __name__ == "__main__":
    main()
