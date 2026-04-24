import os
import re
import time
import logging
from collections import defaultdict
from datetime import date as date_type

import httpx
from cachetools import TTLCache
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError, ResourceError
from fastmcp.server.middleware import Middleware

NASA_API_URL = "https://api.nasa.gov/planetary/apod"
DEFAULT_API_KEY = "DEMO_KEY"
HTTP_TIMEOUT = 8

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
APOD_MIN_DATE = date_type(1995, 6, 16)
RATE_LIMIT_MAX = 5
RATE_LIMIT_WINDOW = 60

APOD_DATA_CACHE_TTL = 3600
APOD_IMAGE_CACHE_TTL = 86400
APOD_DATA_CACHE_SIZE = 100
APOD_IMAGE_CACHE_SIZE = 50

logger = logging.getLogger("apod-server")

apod_data_cache: TTLCache[str, dict] = TTLCache(
    maxsize=APOD_DATA_CACHE_SIZE, ttl=APOD_DATA_CACHE_TTL
)
apod_image_cache: TTLCache[str, tuple[bytes, str]] = TTLCache(
    maxsize=APOD_IMAGE_CACHE_SIZE, ttl=APOD_IMAGE_CACHE_TTL
)


class RateLimitMiddleware(Middleware):
    def __init__(self, max_requests: int = RATE_LIMIT_MAX, window: int = RATE_LIMIT_WINDOW):
        self.max_requests = max_requests
        self.window = window
        self._requests: dict[str, list[float]] = defaultdict(list)

    async def on_call_tool(self, context, call_next):
        client_id = "default"
        now = time.time()
        self._requests[client_id] = [
            t for t in self._requests[client_id]
            if t > now - self.window
        ]
        if len(self._requests[client_id]) >= self.max_requests:
            raise ToolError(
                f"Rate limit excedido: maximo {self.max_requests} peticiones por minuto. Intente mas tarde."
            )
        self._requests[client_id].append(now)
        return await call_next(context)


mcp = FastMCP(
    "apod-server",
    instructions="Servidor MCP para consultar APOD (Astronomy Picture of the Day) de la NASA.",
    middleware=[RateLimitMiddleware()],
)


def _get_api_key() -> str:
    return os.environ.get("NASA_API_KEY", DEFAULT_API_KEY)


def _validate_date(date: str | None, allow_none: bool = True) -> None:
    if date is None:
        if allow_none:
            return
        raise ValueError("Fecha es requerida")
    if not DATE_PATTERN.match(date):
        raise ValueError(f"Formato de fecha invalido: '{date}'. Use YYYY-MM-DD.")
    parsed = date_type.fromisoformat(date)
    today = date_type.today()
    if parsed < APOD_MIN_DATE:
        raise ValueError(f"Fecha anterior al inicio de APOD: '{date}'. La primera fecha disponible es 1995-06-16.")
    if parsed > today:
        raise ValueError(f"Fecha futura no permitida: '{date}'. Use una fecha hasta {today.isoformat()}.")


def _validate_date_tool(date: str | None) -> None:
    try:
        _validate_date(date, allow_none=True)
    except ValueError as e:
        raise ToolError(str(e))


def _validate_date_resource(date: str) -> None:
    try:
        _validate_date(date, allow_none=False)
    except ValueError as e:
        raise ResourceError(str(e))


def _build_normalized(data: dict) -> dict:
    return {
        "service": "APOD",
        "date": data.get("date", ""),
        "title": data.get("title", ""),
        "explanation": data.get("explanation", ""),
        "media_type": data.get("media_type", ""),
        "url": data.get("url", ""),
        "hdurl": data.get("hdurl") or None,
        "thumbnail_url": data.get("thumbnail_url") or None,
        "copyright": data.get("copyright") or None,
        "source_api": NASA_API_URL,
    }


def _classify_nasa_error(status_code: int, detail: str) -> str:
    if status_code == 403:
        return f"Error de autenticacion NASA (403): {detail}. Verifique NASA_API_KEY."
    if status_code == 429:
        return f"Limite de peticiones excedido (429): {detail}. Intente mas tarde o use una API key propia."
    if status_code == 400:
        return f"Peticion invalida a NASA (400): {detail}"
    return f"Error NASA ({status_code}): {detail}"


def _make_cache_key(date: str, hd: bool) -> str:
    return f"{date}:{hd}"


async def _fetch_apod_data(date: str | None = None, hd: bool = False) -> dict:
    api_key = _get_api_key()
    params: dict = {"api_key": api_key}

    if date is not None:
        params["date"] = date
    if hd:
        params["hd"] = "true"

    logger.info("Fetching APOD date=%s hd=%s", date, hd)

    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            response = await client.get(NASA_API_URL, params=params)
    except httpx.TimeoutException:
        raise RuntimeError("Timeout al consultar NASA APOD. Intente nuevamente en unos momentos.")
    except httpx.HTTPError as exc:
        raise RuntimeError(f"Error de red al consultar NASA APOD: {type(exc).__name__}. Intente nuevamente.")

    if response.status_code != 200:
        detail = ""
        try:
            body = response.json()
            detail = body.get("error", {}).get("message", response.text[:200])
        except Exception:
            detail = response.text[:200]
        raise RuntimeError(_classify_nasa_error(response.status_code, detail))

    data = response.json()
    return _build_normalized(data)


async def _fetch_apod_data_cached(date: str, hd: bool = False) -> dict:
    key = _make_cache_key(date, hd)
    if key in apod_data_cache:
        logger.info("Cache HIT for APOD data: %s", key)
        return apod_data_cache[key]
    
    logger.info("Cache MISS for APOD data: %s", key)
    data = await _fetch_apod_data(date, hd)
    apod_data_cache[key] = data
    return data


async def _fetch_apod_image_bytes(url: str) -> tuple[bytes, str]:
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT * 2) as client:
        response = await client.get(url)
        response.raise_for_status()
    
    content_type = response.headers.get("content-type", "image/jpeg")
    return response.content, content_type


async def _fetch_image_cached(url: str, date: str) -> tuple[bytes, str]:
    key = f"{date}:{url}"
    if key in apod_image_cache:
        logger.info("Cache HIT for APOD image: %s", key)
        return apod_image_cache[key]
    
    logger.info("Cache MISS for APOD image: %s", key)
    image_data = await _fetch_apod_image_bytes(url)
    apod_image_cache[key] = image_data
    return image_data


@mcp.tool
async def get_apod_info(date: str | None = None, hd: bool = False) -> dict:
    """Obtiene la informacion APOD (Astronomy Picture of the Day) de la NASA.

    Args:
        date: Fecha APOD en formato YYYY-MM-DD. Si no se envia, consulta del dia actual.
        hd: Solicita contenido HD cuando la API lo permita. Default false.

    Returns:
        Diccionario con la informacion normalizada del APOD.
    """
    _validate_date_tool(date)

    try:
        result = await _fetch_apod_data(date, hd)
    except RuntimeError as e:
        raise ToolError(str(e))

    logger.info("APOD OK date=%s title=%s", result["date"], result["title"])
    return result


@mcp.resource("apod://json/{date}{?hd}", mime_type="application/json")
async def get_apod_json(date: str, hd: bool = False) -> dict:
    """Resource que retorna datos APOD en formato JSON.
    
    Args:
        date: Fecha APOD en formato YYYY-MM-DD (obligatorio).
        hd: Solicita contenido HD cuando la API lo permita. Default false.
    
    Returns:
        Diccionario con la informacion normalizada del APOD.
    """
    _validate_date_resource(date)

    try:
        result = await _fetch_apod_data_cached(date, hd)
    except RuntimeError as e:
        raise ResourceError(str(e))

    logger.info("APOD JSON resource OK date=%s title=%s", result["date"], result["title"])
    return result


@mcp.resource("apod://markdown/{date}{?hd}", mime_type="text/markdown")
async def get_apod_markdown(date: str, hd: bool = False) -> str:
    """Resource que retorna datos APOD formateados como Markdown.
    
    Args:
        date: Fecha APOD en formato YYYY-MM-DD (obligatorio).
        hd: Solicita contenido HD cuando la API lo permita. Default false.
    
    Returns:
        String con el contenido formateado en Markdown.
    """
    _validate_date_resource(date)

    try:
        data = await _fetch_apod_data_cached(date, hd)
    except RuntimeError as e:
        raise ResourceError(str(e))

    lines = [
        f"# {data['title']}",
        "",
        f"**Date:** {data['date']}",
        f"**Media Type:** {data['media_type']}",
        "",
        "## Explanation",
        "",
        data['explanation'],
        "",
        "## Links",
    ]

    if data.get('url'):
        lines.append(f"- [Media URL]({data['url']})")
    if data.get('hdurl'):
        lines.append(f"- [HD URL]({data['hdurl']})")
    if data.get('thumbnail_url'):
        lines.append(f"- [Thumbnail]({data['thumbnail_url']})")
    
    if data.get('copyright'):
        lines.append("")
        lines.append(f"**Copyright:** {data['copyright']}")
    
    lines.append("")
    lines.append(f"*Source: [NASA APOD]({NASA_API_URL})*")

    logger.info("APOD Markdown resource OK date=%s title=%s", data["date"], data["title"])
    return "\n".join(lines)


@mcp.resource("apod://image/{date}")
async def get_apod_image(date: str) -> bytes:
    """Resource que retorna la imagen APOD en formato binario.
    
    Args:
        date: Fecha APOD en formato YYYY-MM-DD (obligatorio).
    
    Returns:
        Bytes de la imagen (JPEG, PNG, etc.).
    """
    _validate_date_resource(date)

    try:
        data = await _fetch_apod_data_cached(date, hd=False)
    except RuntimeError as e:
        raise ResourceError(str(e))

    image_url = data.get('hdurl') or data.get('url')
    if not image_url:
        raise ResourceError(f"No hay imagen disponible para la fecha {date}")

    if data.get('media_type') != 'image':
        raise ResourceError(f"El contenido para {date} no es una imagen (media_type: {data.get('media_type')})")

    try:
        image_bytes, content_type = await _fetch_image_cached(image_url, date)
    except httpx.HTTPError as e:
        raise ResourceError(f"Error descargando imagen: {type(e).__name__}")

    logger.info("APOD Image resource OK date=%s url=%s content_type=%s", date, image_url, content_type)
    return image_bytes


if __name__ == "__main__":
    mcp.run()