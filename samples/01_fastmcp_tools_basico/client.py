from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _extract_text(value: Any) -> str:
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


def _parse_llm_plan(raw_json: str) -> tuple[str, dict[str, Any]]:
    data = json.loads(raw_json)
    tool_name = str(data.get("tool", "")).strip()
    arguments = data.get("arguments", {})
    if not isinstance(arguments, dict):
        raise ValueError("'arguments' debe ser un objeto JSON")
    if not tool_name:
        raise ValueError("No se encontro nombre de tool en respuesta del LLM")
    return tool_name, arguments


def choose_tool_with_ollama(question: str, model: str) -> tuple[str, dict[str, Any]]:
    system_prompt = (
        "Eres un planificador de tools MCP. Responde solo JSON valido: "
        '{"tool":"nombre_tool","arguments":{...}}. '
        "Tools: sumar(a:number,b:number), "
        "normalizar_texto(texto:string), "
        "extraer_keywords(texto:string,max_keywords:number opcional)."
    )
    response = ollama.chat(
        model=model,
        format="json",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    raw = response["message"]["content"]
    return _parse_llm_plan(raw)


async def run(question: str | None, model: str) -> None:
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

            result = await session.call_tool("sumar", {"a": 12, "b": 30})
            print(f"\nDemo sumar(12, 30) = {_extract_text(result)}")

            if question:
                tool_name, arguments = choose_tool_with_ollama(
                    question=question, model=model
                )
                print(
                    f"\nPlan Ollama: {json.dumps({'tool': tool_name, 'arguments': arguments}, indent=2)}"
                )
                result = await session.call_tool(tool_name, arguments)
                print(f"Resultado: {_extract_text(result)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente MCP - Tools")
    parser.add_argument(
        "--question", type=str, default=None, help="Pregunta en lenguaje natural"
    )
    parser.add_argument(
        "--model", type=str, default=os.getenv("OLLAMA_MODEL", "llama3.2")
    )
    args = parser.parse_args()
    asyncio.run(run(question=args.question, model=args.model))


if __name__ == "__main__":
    main()
