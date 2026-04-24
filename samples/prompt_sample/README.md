# NASA APOD Week Prompt MCP

MCP que implementa un prompt para obtener las fechas de una semana completa y consultar la API NASA APOD.

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python server.py
```

## Prompt disponible

### `nasa_apod_week`

Recibe una fecha en formato `YYYY-MM-DD` y genera un prompt con las 7 fechas de la semana (lunes a domingo) para consultar la API NASA APOD.

**Argumentos:**
- `fecha`: Fecha en formato YYYY-MM-DD

**Ejemplo:**
```
Input: fecha="2025-04-22"

Output:
Semana del 2025-04-21 al 2025-04-27:
- 2025-04-21 (lunes)
- 2025-04-22 (martes)
- 2025-04-23 (miércoles)
- 2025-04-24 (jueves)
- 2025-04-25 (viernes)
- 2025-04-26 (sábado)
- 2025-04-27 (domingo)

NASA APOD API endpoint: https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=YYYY-MM-DD
```

## Validaciones

El prompt valida la fecha de entrada y retorna errores descriptivos:

| Error | Ejemplo | Mensaje |
|-------|---------|---------|
| Formato inválido | `2025/04/22` | Formato de fecha inválido. Use YYYY-MM-DD. |
| Fecha no existe | `2025-02-30` | Fecha inválida. day is out of range for month |
| Muy antigua | `1995-06-01` | Fecha anterior al inicio de APOD. Primera fecha disponible: 1995-06-16. |
| Fecha futura | `2099-01-01` | Fecha futura no permitida. Use una fecha hasta {hoy}. |
| Semana antigua | `1995-06-17` | La semana contiene fechas anteriores al inicio de APOD. Primera semana disponible desde: 1995-06-16. |

**Rango válido:** Desde `1995-06-16` hasta hoy (fecha actual).

## NASA APOD API

La API de NASA APOD (Astronomy Picture of the Day) devuelve información sobre la imagen astronómica del día.

- **Primera fecha disponible:** 1995-06-16
- **Endpoint:** `https://api.nasa.gov/planetary/apod?api_key=YOUR_KEY&date=YYYY-MM-DD`
- **Más información:** https://api.nasa.gov/