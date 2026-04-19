from __future__ import annotations

import asyncio
import os
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


SAMPLE_DOCS = [
    "Model Context Protocol (MCP) es un protocolo que permite a las aplicaciones proporcionar contexto a los LLMs de forma estandarizada. "
    "MCP sigue una arquitectura cliente-servidor donde los servidores exponen tools, resources y prompts. "
    "Los clientes se conectan a los servidores y pueden descubrir sus capacidades dinamicamente.",
    "FastMCP es una capa de abstraccion sobre el servidor MCP que usa decoradores para definir tools, resources y prompts. "
    "Permite crear servidores MCP de forma rapida y concisa. "
    "Alternativamente, el SDK low-level ofrece control total sobre los handlers y los schemas JSON.",
    "Los resources en MCP son datos de solo lectura que el modelo puede consultar, similares a endpoints GET en REST. "
    "Los templates de resources permiten URIs parametrizadas como product://{sku}. "
    "Los prompts son plantillas de mensajes reutilizables que aceptan argumentos.",
]


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

            print("\nIngiendo documentos de ejemplo...")
            for i, doc in enumerate(SAMPLE_DOCS):
                r = await session.call_tool(
                    "ingest_document", {"text": doc, "chunk_size": 30}
                )
                print(f"  Doc {i + 1}: {_extract_text(r)}")

            r = await session.read_resource("rag://stats")
            print(f"\nStats: {_readable_content(r)}")

            print("\nBusqueda: 'como se definen tools en MCP'")
            r = await session.call_tool(
                "search", {"query": "como se definen tools en MCP", "top_k": 2}
            )
            print(_extract_text(r))

            print("\nBusqueda: 'resources de solo lectura'")
            r = await session.call_tool(
                "search", {"query": "resources de solo lectura", "top_k": 2}
            )
            print(_extract_text(r))


if __name__ == "__main__":
    asyncio.run(main())
