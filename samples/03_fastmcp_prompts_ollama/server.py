from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("fastmcp-prompts-demo")


@mcp.prompt(title="Resumen tecnico")
def resumen_tecnico(tema: str, audiencia: str = "equipo de plataforma") -> str:
    """Genera un prompt para resumen tecnico."""
    return (
        f"Genera un resumen tecnico sobre '{tema}' para '{audiencia}'.\n"
        "Incluye:\n"
        "1) Definicion\n"
        "2) Arquitectura\n"
        "3) Riesgos comunes\n"
        "4) Recomendaciones practicas"
    )


@mcp.prompt(title="Plan de migracion")
def plan_migracion(sistema_actual: str, objetivo: str) -> str:
    """Genera un prompt para plan de migracion."""
    return (
        f"Disena un plan de migracion desde '{sistema_actual}' hacia '{objetivo}'.\n"
        "Responde con:\n"
        "- Fases\n"
        "- Dependencias\n"
        "- Rollback\n"
        "- Metricas de exito"
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
