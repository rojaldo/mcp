# 00_sample - MCP Server APOD (NASA)

Servidor MCP que expone una tool para consultar el servicio APOD (Astronomy Picture of the Day) de la NASA, implementado con FastMCP.

## Requisitos

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Variables de entorno

| Variable | Obligatoria | Default | Descripcion |
|----------|-------------|---------|-------------|
| `NASA_API_KEY` | No | `DEMO_KEY` | API key de [api.nasa.gov](https://api.nasa.gov/) |

> `DEMO_KEY` tiene limites de peticiones reducidos. Para uso intensivo, registre su propia key aqui: https://api.nasa.gov/

## Instalacion

```bash
cd samples/00_sample
uv sync
```

## Ejecucion

### Servidor standalone

```bash
uv run server.py
```

### Cliente de prueba

```bash
uv run client.py
```

Ejecuta los 4 casos de prueba contra el servidor via STDIO.

### MCP Inspector

```bash
npx @modelcontextprotocol/inspector uv run server.py
```

## Tool: `get_apod_info`

Obtiene la informacion APOD de una fecha dada o del dia actual.

### Parametros

| Parametro | Tipo | Requerido | Default | Descripcion |
|-----------|------|-----------|---------|-------------|
| `date` | string | No | dia actual | Fecha en formato `YYYY-MM-DD` |
| `hd` | boolean | No | `false` | Solicita contenido HD |

### Respuesta

```json
{
  "service": "APOD",
  "date": "2024-01-01",
  "title": "...",
  "explanation": "...",
  "media_type": "image",
  "url": "https://...",
  "hdurl": "https://...",
  "thumbnail_url": null,
  "copyright": "...",
  "source_api": "https://api.nasa.gov/planetary/apod"
}
```

### Errores

| Caso | Respuesta |
|------|-----------|
| Fecha con formato invalido | Error de validacion claro |
| API key invalida / limite excedido | Error clasificado de NASA |
| Timeout / error de red | Error temporal con sugerencia de reintento |

## Casos de prueba

| ID | Input | Esperado |
|----|-------|----------|
| CP-01 | `{}` | APOD del dia actual |
| CP-02 | `{"date":"2024-01-01"}` | APOD del 2024-01-01 |
| CP-03 | `{"date":"01-01-2024"}` | Error de validacion |
| CP-04 | `{"hd":true}` | APOD con hdurl (si disponible) |