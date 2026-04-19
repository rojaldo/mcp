from __future__ import annotations

import re
from collections import Counter

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("fastmcp-tools-demo")

STOPWORDS = {
    "el",
    "la",
    "los",
    "las",
    "de",
    "del",
    "y",
    "o",
    "a",
    "en",
    "un",
    "una",
    "para",
    "con",
    "por",
    "que",
    "se",
    "es",
}


@mcp.tool()
def sumar(a: float, b: float) -> float:
    """Suma dos numeros."""
    return a + b


@mcp.tool()
def normalizar_texto(texto: str) -> str:
    """Normaliza texto: trim + lowercase + espacios simples."""
    return " ".join(texto.strip().split()).lower()


@mcp.tool()
def extraer_keywords(texto: str, max_keywords: int = 5) -> list[str]:
    """Extrae keywords con heuristica de frecuencia."""
    tokens = re.findall(r"[a-zA-Z0-9_]+", texto.lower())
    tokens = [t for t in tokens if len(t) > 2 and t not in STOPWORDS]
    frecuencia = Counter(tokens)
    return [palabra for palabra, _ in frecuencia.most_common(max_keywords)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
