from __future__ import annotations

import asyncio
import hashlib
import json
import math

import mcp.types as types
from mcp.server import Server
from mcp.server.lowlevel.helper_types import ReadResourceContents
from mcp.server.stdio import stdio_server

server = Server("sdk-rag-memory")

CHUNKS: list[dict[str, str]] = []
EMBEDDINGS: list[list[float]] = []


def _cosine_sim(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="ingest_document",
            description="Ingiere un documento de texto y lo indexa por chunks",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Texto a ingerir"},
                    "chunk_size": {
                        "type": "integer",
                        "description": "Tamano de chunk (default 200)",
                    },
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="search",
            description="Busca chunks semanticamente similares a una query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Query de busqueda"},
                    "top_k": {
                        "type": "integer",
                        "description": "Resultados (default 3)",
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        import ollama
    except ImportError:
        return [
            types.TextContent(
                type="text", text="ERROR: instala ollama (pip install ollama)"
            )
        ]

    if name == "ingest_document":
        text = arguments["text"]
        chunk_size = arguments.get("chunk_size", 200)
        words = text.split()
        new_chunks: list[str] = []
        for i in range(0, len(words), chunk_size):
            chunk_text = " ".join(words[i : i + chunk_size])
            new_chunks.append(chunk_text)

        if not new_chunks:
            return [types.TextContent(type="text", text="No se generaron chunks")]

        model = "nomic-embed-text"
        for chunk_text in new_chunks:
            response = ollama.embed(model=model, input=chunk_text)
            embedding = response["embeddings"][0]
            chunk_id = hashlib.md5(chunk_text.encode()).hexdigest()[:8]
            CHUNKS.append({"id": chunk_id, "text": chunk_text})
            EMBEDDINGS.append(embedding)

        return [
            types.TextContent(
                type="text",
                text=f"Ingeridos {len(new_chunks)} chunks (modelo: {model}). Total: {len(CHUNKS)} chunks.",
            )
        ]

    if name == "search":
        query = arguments["query"]
        top_k = arguments.get("top_k", 3)
        if not CHUNKS:
            return [
                types.TextContent(
                    type="text",
                    text="No hay documentos ingeridos. Usa ingest_document primero.",
                )
            ]

        model = "nomic-embed-text"
        response = ollama.embed(model=model, input=query)
        query_embedding = response["embeddings"][0]

        scores = []
        for i, emb in enumerate(EMBEDDINGS):
            sim = _cosine_sim(query_embedding, emb)
            scores.append((i, sim))
        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, sim in scores[:top_k]:
            results.append(
                {
                    "id": CHUNKS[idx]["id"],
                    "similarity": round(sim, 4),
                    "text": CHUNKS[idx]["text"][:150],
                }
            )

        return [
            types.TextContent(
                type="text", text=json.dumps(results, indent=2, ensure_ascii=False)
            )
        ]

    return [types.TextContent(type="text", text=f"Tool desconocida: {name}")]


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri="rag://stats", name="rag-stats", mimeType="application/json"
        ),
    ]


@server.read_resource()
async def handle_read_resource(uri) -> object:
    uri_str = str(uri)
    if uri_str == "rag://stats":
        data = {
            "total_chunks": len(CHUNKS),
            "embedding_dim": len(EMBEDDINGS[0]) if EMBEDDINGS else 0,
        }
        return [
            ReadResourceContents(
                content=json.dumps(data, indent=2), mime_type="application/json"
            )
        ]
    return [
        ReadResourceContents(
            content=f"Recurso no encontrado: {uri}", mime_type="text/plain"
        )
    ]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
