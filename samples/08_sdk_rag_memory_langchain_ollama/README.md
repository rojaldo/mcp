# 08 - SDK RAG Local en Memoria con Ollama

Servidor MCP low-level que implementa RAG (Retrieval-Augmented Generation) con embeddings de Ollama y un indice en memoria.

## Requisitos

- Python 3.10+
- Ollama local corriendo
- Modelo de embeddings descargado: `ollama pull nomic-embed-text`

## Preparacion

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama pull nomic-embed-text
```

## Ejecucion

```bash
python client.py
```

## Como funciona

- El servidor crea chunks del texto ingerido.
- Usa `ollama.embed()` con `nomic-embed-text` para generar embeddings.
- Busqueda por similitud coseno sobre la lista de embeddings en RAM.
- Resource `rag://stats` muestra estadisticas del indice.

## Tools

| Tool | Descripcion |
|------|-------------|
| `ingest_document(text, chunk_size)` | Ingiere texto y lo indexa |
| `search(query, top_k)` | Busca chunks semanticamente similares |

## Resources

| URI | Descripcion |
|-----|-------------|
| `rag://stats` | Estadisticas del indice (chunks, dimension) |

## Nota

No usa ninguna vector DB externa. Todo el indice vive en memoria (listas Python). Para produccion, usaria ChromaDB/Qdrant.