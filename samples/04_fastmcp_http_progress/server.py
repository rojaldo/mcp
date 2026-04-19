from __future__ import annotations

import asyncio

from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("fastmcp-http-progress", stateless_http=True, json_response=True)


@mcp.tool()
async def tarea_larga(pasos: int, ctx: Context) -> str:
    """Ejecuta una tarea larga con reporte de progreso."""
    await ctx.info(f"Iniciando tarea de {pasos} pasos")
    total = 0
    for i in range(pasos):
        await asyncio.sleep(0.3)
        total += i + 1
        await ctx.report_progress(
            progress=i + 1, total=pasos, message=f"Paso {i + 1}/{pasos}"
        )
    return f"Tarea completada: suma acumulada = {total}"


@mcp.tool()
async def analisis_datos(filas: int, ctx: Context) -> str:
    """Simula analisis de datos con progreso."""
    await ctx.info(f"Analizando {filas} filas")
    resultados = []
    for i in range(filas):
        await asyncio.sleep(0.1)
        resultados.append(i * 2)
        if (i + 1) % max(1, filas // 5) == 0:
            pct = (i + 1) / filas
            await ctx.report_progress(
                progress=i + 1, total=filas, message=f"{pct:.0%} completado"
            )
    return f"Analisis completado: {len(resultados)} filas, suma = {sum(resultados)}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
