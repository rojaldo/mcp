from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import Any

import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _flatten_messages(prompt_result: Any) -> str:
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


async def run(run_llm: bool, model: str) -> None:
    base_dir = Path(__file__).resolve().parent
    params = StdioServerParameters(
        command=sys.executable, args=[str(base_dir / "server.py")]
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            prompts_result = await session.list_prompts()
            prompts = getattr(prompts_result, "prompts", [])
            print("Prompts disponibles:")
            for p in prompts:
                print(f"  - {p.name}: {p.description}")

            prompt_data = await session.get_prompt(
                "resumen_tecnico",
                {
                    "tema": "Model Context Protocol",
                    "audiencia": "arquitectos de software",
                },
            )

            final_prompt = _flatten_messages(prompt_data)
            print(f"\nPrompt renderizado:\n{final_prompt}")

            if run_llm:
                response = ollama.chat(
                    model=model, messages=[{"role": "user", "content": final_prompt}]
                )
                print(f"\nRespuesta de Ollama:\n{response['message']['content']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente MCP - Prompts")
    parser.add_argument(
        "--run-llm", action="store_true", help="Ejecuta el prompt con Ollama"
    )
    parser.add_argument(
        "--model", type=str, default=os.getenv("OLLAMA_MODEL", "llama3.2")
    )
    args = parser.parse_args()
    asyncio.run(run(run_llm=args.run_llm, model=args.model))


if __name__ == "__main__":
    main()
