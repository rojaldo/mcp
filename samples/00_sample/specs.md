# Especificación: Servidor MCP con FastMCP para APOD (NASA)

## 1. Objetivo

Definir un servidor MCP implementado en Python con FastMCP que exponga una tool para consultar información del servicio APOD (Astronomy Picture of the Day) de la NASA.

La tool debe entregar una respuesta normalizada y estable para cualquier cliente MCP (Inspector, CLI o clientes personalizados).

## 2. Alcance

Incluye:
- Servidor MCP en Python usando FastMCP.
- Exposición de una tool pública: get_apod_info.
- Consumo del endpoint oficial APOD de NASA.
- Validación de entrada y manejo estándar de errores.

No incluye:
- Persistencia en base de datos.
- Autenticación/autorización por usuario final.
- Cache distribuido (solo opción futura).

## 3. Stack técnico

- Lenguaje: Python 3.10+
- Framework MCP: FastMCP
- Cliente HTTP sugerido: httpx
- Transporte de ejecución: stdio (para uso con MCP Inspector)

## 4. Referencias

- API NASA: https://api.nasa.gov/
- Endpoint APOD: https://api.nasa.gov/planetary/apod

## 5. Requisitos funcionales

### RF-01: Servidor FastMCP

El servidor debe inicializar FastMCP y registrar la tool get_apod_info.

### RF-02: Tool expuesta

Nombre de la tool:
- get_apod_info

Descripción funcional:
- Obtiene la información APOD de una fecha dada o del día actual.

### RF-03: Parámetros de entrada

La tool debe aceptar:

- date (string, opcional)
	- Formato estricto: YYYY-MM-DD.
	- Si no se envía, consultar APOD del día actual.

- hd (boolean, opcional, default false)
	- Solicita contenido HD cuando la API lo permita.

No se permiten propiedades adicionales en el input.

### RF-04: Integración con NASA APOD

La tool debe invocar:
- GET https://api.nasa.gov/planetary/apod

Query params:
- api_key: valor de NASA_API_KEY o DEMO_KEY por defecto.
- date: solo si fue recibido.
- hd: solo si fue recibido.

### RF-05: Respuesta normalizada

La salida debe tener estructura consistente:

- service: string (valor fijo "APOD")
- date: string
- title: string
- explanation: string
- media_type: string ("image" o "video")
- url: string
- hdurl: string o null
- thumbnail_url: string o null
- copyright: string o null
- source_api: string (valor fijo https://api.nasa.gov/planetary/apod)

### RF-06: Manejo de errores

Casos mínimos:

- Validación de entrada:
	- date inválida => error claro de validación.

- Error de NASA:
	- API key inválida, límite excedido, fecha inválida/fuera de rango.
	- Devolver error legible con clasificación interna.

- Error de red/timeout:
	- Devolver error temporal con sugerencia de reintento.

## 6. Requisitos no funcionales

- RNF-01: Tiempo objetivo de respuesta < 3 segundos en red normal.
- RNF-02: Timeout HTTP configurable (recomendado: 8 segundos).
- RNF-03: Logging mínimo:
	- inicio de invocación,
	- parámetros no sensibles,
	- resultado o error.
- RNF-04: No exponer NASA_API_KEY en logs, errores ni respuesta.
- RNF-05: Código legible y tipado básico en funciones públicas.

## 7. Contrato de la tool

### 7.1 Nombre

get_apod_info

### 7.2 Input schema (conceptual)

- type: object
- additionalProperties: false
- properties:
	- date:
		- type: string
		- pattern: ^\\d{4}-\\d{2}-\\d{2}$
		- description: Fecha APOD en formato YYYY-MM-DD.
	- hd:
		- type: boolean
		- default: false

### 7.3 Output schema (conceptual)

- type: object
- required:
	- service
	- date
	- title
	- explanation
	- media_type
	- url
	- source_api

## 8. Estructura mínima esperada

- server.py
	- Inicializa FastMCP.
	- Define y registra get_apod_info.
	- Implementa llamada HTTP a NASA APOD.

- requirements.txt
	- fastmcp
	- httpx

- README.md
	- Variables de entorno.
	- Comando de ejecución con Inspector.

## 9. Criterios de aceptación

- CA-01: El servidor inicia correctamente en stdio.
- CA-02: MCP Inspector detecta la tool get_apod_info.
- CA-03: Invocación sin parámetros retorna APOD del día.
- CA-04: Invocación con date válida retorna datos de esa fecha.
- CA-05: date inválida retorna error de validación claro.
- CA-06: Errores de NASA se propagan como error controlado y entendible.

## 10. Casos de prueba mínimos

- CP-01: Input {}
	- Esperado: éxito con campos obligatorios.

- CP-02: Input {"date":"2024-01-01"}
	- Esperado: éxito con date="2024-01-01".

- CP-03: Input {"date":"01-01-2024"}
	- Esperado: error de validación.

- CP-04: Input {"hd":true}
	- Esperado: éxito; incluye hdurl cuando NASA lo entregue.

## 11. Variables de entorno

- NASA_API_KEY (opcional)
	- Si falta, usar DEMO_KEY.

## 12. Ejecución de referencia

- Ejecución local del servidor (ejemplo):
	- python server.py

- Ejecución con Inspector (ejemplo):
	- npx @modelcontextprotocol/inspector python server.py

## 13. Evolución futura

- Cache en memoria con TTL para consultas repetidas.
- Tool adicional get_apod_range para rango de fechas.
- Traducción opcional de explanation al español.
