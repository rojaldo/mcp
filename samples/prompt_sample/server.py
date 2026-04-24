from __future__ import annotations

import re
from datetime import date, timedelta

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("nasa-apod-week")

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
APOD_MIN_DATE = date(1995, 6, 16)


def _validate_date(fecha: str) -> date:
    if not DATE_PATTERN.match(fecha):
        raise ValueError(f"Formato de fecha inválido: '{fecha}'. Use YYYY-MM-DD.")
    
    try:
        fecha_obj = date.fromisoformat(fecha)
    except ValueError as e:
        raise ValueError(f"Fecha inválida: '{fecha}'. {str(e)}") from None
    
    if fecha_obj < APOD_MIN_DATE:
        raise ValueError(
            f"Fecha anterior al inicio de APOD: '{fecha}'. "
            f"Primera fecha disponible: {APOD_MIN_DATE.isoformat()}."
        )
    
    hoy = date.today()
    if fecha_obj > hoy:
        raise ValueError(
            f"Fecha futura no permitida: '{fecha}'. "
            f"Use una fecha hasta {hoy.isoformat()}."
        )
    
    return fecha_obj


@mcp.prompt(title="NASA APOD Semana")
def nasa_apod_week(fecha: str) -> str:
    """
    Genera un prompt con las 7 fechas de la semana (lunes-domingo)
    para consultar la API NASA APOD de cada dia.
    
    Args:
        fecha: Fecha en formato YYYY-MM-DD
    
    Raises:
        ValueError: Si el formato es inválido, la fecha no existe,
                   está fuera del rango de APOD, o es fecha futura.
    """
    fecha_obj = _validate_date(fecha)
    
    dias_hasta_lunes = fecha_obj.weekday()
    lunes = fecha_obj - timedelta(days=dias_hasta_lunes)
    
    if lunes < APOD_MIN_DATE:
        primera_semana_lunes = APOD_MIN_DATE
        raise ValueError(
            f"La semana contiene fechas anteriores al inicio de APOD. "
            f"Primera semana disponible desde: {primera_semana_lunes.isoformat()}."
        )
    
    fechas = [(lunes + timedelta(days=i)) for i in range(7)]
    fechas_str = [f.isoformat() for f in fechas]
    dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    lineas = [f"- {f} ({d})" for f, d in zip(fechas_str, dias_semana)]
    fechas_lista = "\n".join(lineas)
    
    return f"""Actua como asistente de astronomía. El usuario quiere ver las imágenes astronómicas de la NASA (APOD - Astronomy Picture of the Day) para una semana completa.

Semana del {fechas_str[0]} al {fechas_str[6]}:
{fechas_lista}

NASA APOD API endpoint: https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=YYYY-MM-DD

Para cada fecha, consulta la API y devuelve el título, descripción y URL de la imagen."""


if __name__ == "__main__":
    mcp.run(transport="stdio")