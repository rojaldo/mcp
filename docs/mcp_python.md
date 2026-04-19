# MCP Python SDK - Guía Completa

## Del Fundamento a la Implementación Profesional

---

# Portada

## MCP Python SDK

### Guía Completa para Desarrolladores

---

**Basado en el repositorio oficial:**  
https://github.com/modelcontextprotocol/python-sdk

---

**Duración estimada: 2 horas**

---

# Agenda

## Contenido del curso

---

1. **Introducción** (15 min) - ¿Qué es MCP Python SDK?

2. **Instalación y Configuración** (10 min) - Setup del entorno

3. **FastMCP: Conceptos Básicos** (20 min) - El servidor simplificado

4. **Tools: Creando Herramientas** (25 min) - La primitiva más importante

5. **Resources: Exponiendo Datos** (15 min) - Contexto para el modelo

6. **Prompts: Plantillas Predefinidas** (10 min) - Interacciones reutilizables

7. **Context: Capacidades Avanzadas** (15 min) - Logging, progreso, sampling

8. **Transports: stdio, SSE, HTTP** (15 min) - Modos de comunicación

9. **Ejemplos Prácticos** (20 min) - Casos reales

10. **Despliegue y Producción** (15 min) - Claude Desktop, servidores HTTP

---

# PARTE 1

## Introducción

---

# ¿Qué es MCP?

## Model Context Protocol

---

MCP es un protocolo que permite a las aplicaciones proporcionar contexto a los LLMs de forma estandarizada.

---

**Analogía:**

MCP es como una API web, pero diseñada específicamente para interacciones con LLMs.

---

## ¿Qué pueden hacer los servidores MCP?

---

### 📊 Resources (Datos)

Exponer información para que el LLM la lea.

Similar a endpoints GET en REST.

---

### 🔧 Tools (Acciones)

Permitir que el LLM ejecute código o genere efectos.

Similar a endpoints POST en REST.

---

### 📝 Prompts (Plantillas)

Definir patrones de interacción reutilizables.

Plantillas para conversaciones comunes.

---

# MCP Python SDK

## Implementación oficial en Python

---

El SDK de Python implementa el protocolo MCP completo, facilitando:

---

✅ Crear clientes MCP que se conectan a cualquier servidor

✅ Crear servidores que exponen recursos, prompts y tools

✅ Usar transports estándar: stdio, SSE, Streamable HTTP

✅ Manejar todos los mensajes del protocolo MCP

---

# ¿Por qué usar el SDK de Python?

---

### Ventajas principales

---

**1. FastMCP** - API simplificada con decoradores

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Mi Server")

@mcp.tool()
def suma(a: int, b: int) -> int:
    """Suma dos números"""
    return a + b
```

---

**2. Tipado completo** - Type hints en todo el SDK

---

**3. Validación automática** - Pydantic para schemas

---

**4. Múltiples transports** - stdio, SSE, HTTP

---

**5. Integración con Claude Desktop** - Fácil configuración

---

# PARTE 2

## Instalación y Configuración

---

# Requisitos Previos

---

### Necesitas:

- Python 3.10 o superior
- uv (gestor de paquetes recomendado) o pip

---

# Instalación con uv

## Método recomendado

---

### Crear un nuevo proyecto

```bash
uv init mcp-server-demo
cd mcp-server-demo
```

---

### Añadir MCP al proyecto

```bash
uv add "mcp[cli]"
```

---

# Instalación con pip

## Método alternativo

---

```bash
pip install "mcp[cli]"
```

---

**Nota:** El extra `[cli]` incluye herramientas de desarrollo como `mcp dev` y `mcp install`.

---

# Verificar la instalación

---

```bash
uv run mcp --help
```

---

### Comandos disponibles:

- `mcp dev` - Ejecutar servidor en modo desarrollo con Inspector
- `mcp install` - Instalar servidor en Claude Desktop
- `mcp run` - Ejecutar servidor directamente

---

# Estructura de un proyecto MCP

---

```
mcp-server-demo/
├── pyproject.toml
├── README.md
├── src/
│   └── my_server.py
└── .python-version
```

---

# PARTE 3

## FastMCP: Conceptos Básicos

---

# ¿Qué es FastMCP?

## API simplificada para crear servidores MCP

---

FastMCP es una capa de abstracción sobre el servidor MCP que:

---

✅ Usa decoradores para definir tools, resources y prompts

✅ Genera schemas automáticamente desde type hints

✅ Maneja la comunicación con el cliente

✅ Simplifica el manejo de errores

---

# Crear un servidor básico

---

```python
from mcp.server.fastmcp import FastMCP

# Crear el servidor
mcp = FastMCP("Mi App")
```

---

**Parámetros opcionales:**

```python
mcp = FastMCP(
    "Mi App",
    instructions="Este servidor proporciona herramientas matemáticas",
    json_response=True,  # Respuestas JSON en lugar de SSE
    stateless_http=True  # Para servidores HTTP sin estado
)
```

---

# Quickstart completo

## Servidor mínimo funcional

---

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo", json_response=True)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Suma dos números"""
    return a + b


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Obtiene un saludo personalizado"""
    return f"¡Hola, {name}!"


@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Genera un prompt de saludo"""
    return f"Escribe un saludo {style} para {name}."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

---

# Ejecutar el servidor

---

### Modo desarrollo con Inspector

```bash
uv run mcp dev server.py
```

---

### Instalar en Claude Desktop

```bash
uv run mcp install server.py
```

---

### Ejecutar directamente

```bash
python server.py
```

---

# MCP Inspector

## Herramienta de desarrollo visual

---

```bash
npx -y @modelcontextprotocol/inspector
```

---

**Permite:**

- Conectar a servidores MCP
- Probar tools interactivamente
- Ver resources disponibles
- Debuggear prompts
- Ver logs en tiempo real

---

# PARTE 4

## Tools: Creando Herramientas

---

# ¿Qué son las Tools?

## Funciones que el LLM puede ejecutar

---

Las tools permiten que el modelo tome acciones:

- Calcular resultados
- Consultar APIs externas
- Modificar archivos
- Enviar mensajes

---

**A diferencia de los resources, las tools:**

- Pueden tener efectos secundarios
- Realizan cómputo
- Reciben parámetros

---

# Definir una Tool básica

---

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Tool Example")


@mcp.tool()
def sum(a: int, b: int) -> int:
    """Suma dos números."""
    return a + b


@mcp.tool()
def get_weather(city: str, unit: str = "celsius") -> str:
    """Obtiene el clima de una ciudad."""
    return f"Clima en {city}: 22 grados {unit[0].upper()}"
```

---

# El decorador @mcp.tool()

---

### Parámetros disponibles:

```python
@mcp.tool(
    name="custom_name",        # Nombre personalizado
    description="Mi tool",      # Descripción personalizada
    structured_output=True,     # Output estructurado
    annotations={...}           # Metadatos adicionales
)
def my_tool(x: int) -> str:
    ...
```

---

# Schemas automáticos

## Generación desde type hints

---

FastMCP genera automáticamente el JSON Schema para cada tool:

---

```python
@mcp.tool()
def process_user(
    name: str,
    age: int,
    email: str | None = None
) -> dict:
    """Procesa un usuario."""
    return {"name": name, "age": age}
```

---

**Schema generado:**

```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer"},
    "email": {"type": ["string", "null"]}
  },
  "required": ["name", "age"]
}
```

---

# Structured Output

## Respuestas tipadas y validadas

---

Las tools pueden devolver datos estructurados que se validan automáticamente:

---

### Con Pydantic

```python
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")


class WeatherData(BaseModel):
    temperature: float = Field(description="Temperatura en Celsius")
    humidity: float = Field(description="Humedad en %")
    condition: str
    wind_speed: float


@mcp.tool()
def get_weather(city: str) -> WeatherData:
    """Obtiene datos del clima."""
    return WeatherData(
        temperature=22.5,
        humidity=65.0,
        condition="soleado",
        wind_speed=5.2
    )
```

---

# Tipos de retorno soportados

---

| Tipo | Comportamiento |
|------|---------------|
| `str` | Texto directo |
| `int`, `float`, `bool` | Wrapp en `{"result": value}` |
| `dict[str, T]` | Dict como JSON |
| `list[T]` | Wrapp en `{"result": [...]}` |
| `BaseModel` | Structured output |
| `TypedDict` | Structured output |
| `dataclass` | Structured output |

---

# TypedDict

## Alternativa ligera a Pydantic

---

```python
from typing import TypedDict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Location")


class LocationInfo(TypedDict):
    latitude: float
    longitude: float
    name: str


@mcp.tool()
def get_location(address: str) -> LocationInfo:
    """Obtiene coordenadas."""
    return LocationInfo(
        latitude=51.5074,
        longitude=-0.1278,
        name="Londres, UK"
    )
```

---

# Clases con type hints

## Structured output sin Pydantic

---

```python
class UserProfile:
    name: str
    age: int
    email: str | None = None

    def __init__(self, name: str, age: int, email: str | None = None):
        self.name = name
        self.age = age
        self.email = email


@mcp.tool()
def get_user(user_id: str) -> UserProfile:
    """Obtiene perfil de usuario."""
    return UserProfile("Ana", 30, "ana@example.com")
```

---

**Importante:** Las clases SIN type hints NO generan schema.

---

# CallToolResult

## Control total de la respuesta

---

Para control avanzado sobre la respuesta, puedes devolver `CallToolResult` directamente:

---

```python
from mcp.types import CallToolResult, TextContent
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Advanced")


@mcp.tool()
def advanced_tool() -> CallToolResult:
    """Control total de la respuesta."""
    return CallToolResult(
        content=[TextContent(type="text", text="Respuesta visible")],
        structuredContent={"status": "success", "data": 42},
        _meta={"hidden": "datos para cliente"}
    )
```

---

# Tool con Context

## Accediendo a capacidades MCP

---

```python
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

mcp = FastMCP("Context Example")


@mcp.tool()
async def long_task(
    task_name: str,
    ctx: Context[ServerSession, None],
    steps: int = 5
) -> str:
    """Tarea larga con progreso."""
    
    await ctx.info(f"Iniciando: {task_name}")
    
    for i in range(steps):
        progress = (i + 1) / steps
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Paso {i + 1}/{steps}"
        )
        await ctx.debug(f"Completado paso {i + 1}")
    
    return f"Tarea '{task_name}' completada"
```

---

# Annotations

## Metadatos para las tools

---

```python
@mcp.tool(
    annotations={
        "readOnlyHint": True,        # Solo lectura
        "destructiveHint": True,     # Puede ser destructiva
        "idempotentHint": True,      # Idempotente
        "openWorldHint": True        # Accede a recursos externos
    }
)
def delete_file(path: str) -> bool:
    """Elimina un archivo."""
    # ...
```

---

# PARTE 5

## Resources: Exponiendo Datos

---

# ¿Qué son los Resources?

## Datos que el modelo puede leer

---

Los resources son como endpoints GET:

- Proporcionan información
- No deberían tener efectos secundarios
- Pueden ser estáticos o dinámicos

---

# Tipos de Resources

---

### Estáticos

Datos fijos que no cambian.

```python
@mcp.resource("config://settings")
def get_settings() -> str:
    """Configuración de la app."""
    return '{"theme": "dark", "language": "es"}'
```

---

### Dinámicos (Templates)

Datos que dependen de parámetros.

```python
@mcp.resource("file://documents/{name}")
def read_document(name: str) -> str:
    """Lee un documento por nombre."""
    return f"Contenido de {name}"
```

---

# Definir Resources

---

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Resource Example")


@mcp.resource("file://documents/{name}")
def read_document(name: str) -> str:
    """Lee un documento por nombre."""
    # Aquí iría la lógica de lectura
    return f"Contenido de {name}"


@mcp.resource("config://settings")
def get_settings() -> str:
    """Obtiene la configuración."""
    return """{
  "theme": "dark",
  "language": "es",
  "debug": false
}"""
```

---

# URI Templates

## Patrones para resources dinámicos

---

La sintaxis `{param}` crea parámetros en la URI:

---

| Template | Ejemplo de URI |
|----------|----------------|
| `file://{path}` | `file://readme.md` |
| `user://{id}/profile` | `user://123/profile` |
| `repo://{owner}/{repo}` | `repo://anthropics/claude` |

---

# Tipos MIME

## Especificando el formato

---

Por defecto, los resources devuelven texto plano.

Para especificar el tipo MIME:

---

```python
from mcp.types import Resource

# Al listar resources
@server.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="data://users",
            name="Lista de usuarios",
            mimeType="application/json"
        )
    ]
```

---

# Resource con datos binarios

## Imágenes, PDFs, etc.

---

```python
from mcp.server.fastmcp import FastMCP, Image

mcp = FastMCP("Image Example")


@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Crea un thumbnail."""
    from PIL import Image as PILImage
    
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    
    return Image(data=img.tobytes(), format="png")
```

---

# PARTE 6

## Prompts: Plantillas Predefinidas

---

# ¿Qué son los Prompts?

## Plantillas reutilizables para el modelo

---

Los prompts son mensajes predefinidos que:

- Establecen contexto
- Definen modos de operación
- Facilitan flujos comunes
- Pueden tener parámetros

---

# Definir Prompts básicos

---

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("Prompt Example")


@mcp.prompt(title="Code Review")
def review_code(code: str) -> str:
    """Prompt para revisar código."""
    return f"Por favor revisa este código:\n\n{code}"
```

---

# Prompts con múltiples mensajes

---

```python
@mcp.prompt(title="Debug Assistant")
def debug_error(error: str) -> list[base.Message]:
    """Prompt para debugging."""
    return [
        base.UserMessage("Estoy viendo este error:"),
        base.UserMessage(error),
        base.AssistantMessage(
            "Te ayudo a debuggear. ¿Qué has intentado?"
        ),
    ]
```

---

# Tipos de mensajes

---

```python
from mcp.server.fastmcp.prompts import base

base.UserMessage("Mensaje del usuario")
base.AssistantMessage("Respuesta del asistente")
base.SystemMessage("Instrucciones del sistema")
```

---

# Prompts con argumentos

---

```python
@mcp.prompt()
def analyze_code(
    code: str,
    language: str = "python",
    focus: str = "all"
) -> str:
    """Analiza código con enfoque específico."""
    
    focus_map = {
        "security": "vulnerabilidades de seguridad",
        "performance": "problemas de rendimiento",
        "style": "estilo y legibilidad",
        "all": "todos los aspectos"
    }
    
    return f"""Analiza este código {language}:

```{language}
{code}
```

Enfócate en: {focus_map.get(focus, focus_map["all"])}"""
```

---

# Argumentos requeridos vs opcionales

---

```python
@mcp.prompt()
def my_prompt(
    required_arg: str,           # Requerido
    optional_arg: str = "default"  # Opcional con valor por defecto
) -> str:
    ...
```

Los argumentos requeridos se validan automáticamente.

---

# PARTE 7

## Context: Capacidades Avanzadas

---

# El objeto Context

## Acceso a las capacidades MCP

---

El contexto se inyecta automáticamente en tools y resources que lo solicitan:

---

```python
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("Context Example")


@mcp.tool()
async def my_tool(x: int, ctx: Context) -> str:
    """Tool que usa contexto."""
    # ctx proporciona acceso a capacidades MCP
    return await process(x, ctx)
```

---

# Capacidades del Context

---

| Método/Propiedad | Descripción |
|------------------|-------------|
| `ctx.request_id` | ID único de la petición |
| `ctx.client_id` | ID del cliente |
| `ctx.fastmcp` | Instancia del servidor |
| `ctx.session` | Sesión subyacente |
| `await ctx.debug(msg)` | Log debug |
| `await ctx.info(msg)` | Log info |
| `await ctx.warning(msg)` | Log warning |
| `await ctx.error(msg)` | Log error |
| `await ctx.report_progress(...)` | Reportar progreso |
| `await ctx.read_resource(uri)` | Leer un resource |
| `await ctx.elicit(...)` | Pedir información al usuario |

---

# Logging

## Enviar mensajes de log

---

```python
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

mcp = FastMCP("Logging Example")


@mcp.tool()
async def process_data(
    data: str,
    ctx: Context[ServerSession, None]
) -> str:
    """Procesa datos con logging."""
    
    await ctx.debug(f"Debug: Procesando '{data}'")
    await ctx.info("Info: Iniciando procesamiento")
    await ctx.warning("Warning: Esto es experimental")
    await ctx.error("Error: (Solo demo)")
    
    return f"Procesado: {data}"
```

---

# Progress Reporting

## Reportar progreso de operaciones

---

```python
@mcp.tool()
async def long_running_task(
    task_name: str,
    ctx: Context[ServerSession, None],
    steps: int = 5
) -> str:
    """Tarea con progreso."""
    
    await ctx.info(f"Iniciando: {task_name}")
    
    for i in range(steps):
        progress = (i + 1) / steps
        
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Paso {i + 1}/{steps}"
        )
        
        await ctx.debug(f"Completado paso {i + 1}")
    
    return f"Tarea '{task_name}' completada"
```

---

# Sampling

## Generar texto con el LLM

---

Las tools pueden pedir al LLM que genere texto:

---

```python
from mcp.types import SamplingMessage, TextContent

@mcp.tool()
async def generate_poem(
    topic: str,
    ctx: Context[ServerSession, None]
) -> str:
    """Genera un poema."""
    
    prompt = f"Escribe un poema corto sobre {topic}"
    
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(type="text", text=prompt)
            )
        ],
        max_tokens=100
    )
    
    if result.content.type == "text":
        return result.content.text
    return str(result.content)
```

---

# Elicitation

## Pedir información al usuario

---

Las tools pueden solicitar información adicional al usuario:

---

```python
from pydantic import BaseModel, Field

class BookingPreferences(BaseModel):
    checkAlternative: bool = Field(
        description="¿Quieres otra fecha?"
    )
    alternativeDate: str = Field(
        default="2024-12-26",
        description="Fecha alternativa"
    )


@mcp.tool()
async def book_table(
    date: str,
    ctx: Context[ServerSession, None]
) -> str:
    """Reserva una mesa."""
    
    if date == "2024-12-25":
        result = await ctx.elicit(
            message="No hay mesas el 25. ¿Otra fecha?",
            schema=BookingPreferences
        )
        
        if result.action == "accept" and result.data:
            if result.data.checkAlternative:
                return f"Reservado para {result.data.alternativeDate}"
            return "Cancelado"
    
    return f"Reservado para {date}"
```

---

# Notificaciones

## Avisar a clientes de cambios

---

```python
@mcp.tool()
async def update_data(
    resource_uri: str,
    ctx: Context
) -> str:
    """Actualiza datos y notifica."""
    
    # Actualizar datos...
    
    # Notificar que este resource cambió
    await ctx.session.send_resource_updated(
        AnyUrl(resource_uri)
    )
    
    # Notificar que la lista de resources cambió
    await ctx.session.send_resource_list_changed()
    
    return "Actualizado y notificado"
```

---

# Lifespan

## Recursos compartidos

---

Define recursos que se inicializan al iniciar el servidor:

---

```python
from contextlib import asynccontextmanager
from dataclasses import dataclass

@dataclass
class AppContext:
    db: Database
    config: AppConfig


@asynccontextmanager
async def app_lifespan(server: FastMCP):
    """Gestiona el ciclo de vida."""
    # Startup
    db = await Database.connect()
    try:
        yield AppContext(db=db)
    finally:
        # Shutdown
        await db.disconnect()


mcp = FastMCP("My App", lifespan=app_lifespan)


@mcp.tool()
def query_db(ctx: Context) -> str:
    """Usa la base de datos."""
    db = ctx.request_context.lifespan_context.db
    return db.query()
```

---

# PARTE 8

## Transports: Modos de Comunicación

---

# ¿Qué son los Transports?

## Formas de comunicación servidor-cliente

---

MCP soporta varios mecanismos de transporte:

---

| Transport | Uso | Características |
|-----------|-----|-----------------|
| **stdio** | Claude Desktop | Simple, bidireccional |
| **SSE** | Web clients | Server-Sent Events |
| **Streamable HTTP** | Producción | HTTP moderno, escalable |

---

# stdio Transport

## El más simple

---

Comunicación via entrada/salida estándar.

Usado principalmente con Claude Desktop.

---

```python
# Ejecutar con stdio (por defecto)
mcp.run()
```

---

**Configuración en Claude Desktop:**

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

---

# Streamable HTTP Transport

## Recomendado para producción

---

HTTP moderno con soporte para:

- Sesiones stateful o stateless
- JSON o SSE responses
- Mejor escalabilidad

---

```python
# Servidor HTTP stateless (recomendado)
mcp = FastMCP(
    "Server",
    stateless_http=True,
    json_response=True
)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

---

# Configuración HTTP

---

```python
mcp = FastMCP(
    "My Server",
    stateless_http=True,      # Sin estado
    json_response=True,       # JSON en lugar de SSE
    host="0.0.0.0",          # Host
    port=8000                 # Puerto
)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

---

# Montar en Starlette

## Integración con ASGI

---

```python
from starlette.applications import Starlette
from starlette.routing import Mount

mcp = FastMCP("API", stateless_http=True, json_response=True)


@mcp.tool()
def hello() -> str:
    return "Hello!"


# Montar en Starlette
app = Starlette(
    routes=[
        Mount("/mcp", app=mcp.streamable_http_app())
    ]
)
```

---

# CORS para browsers

---

Para permitir acceso desde browsers:

---

```python
from starlette.middleware.cors import CORSMiddleware

app = CORSMiddleware(
    app,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE"],
    expose_headers=["Mcp-Session-Id"]
)
```

---

# PARTE 9

## Ejemplos Prácticos

---

# Ejemplo 1: Servidor de Clima

---

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("Weather Server", json_response=True)


class WeatherInfo(BaseModel):
    city: str
    temperature: float
    condition: str
    humidity: int


@mcp.tool()
def get_weather(city: str) -> WeatherInfo:
    """Obtiene información del clima."""
    # Simulación - en producción llamar a API real
    return WeatherInfo(
        city=city,
        temperature=22.5,
        condition="soleado",
        humidity=65
    )


@mcp.resource("weather://{city}")
def weather_resource(city: str) -> str:
    """Resource de clima."""
    return f"Clima actual en {city}: 22°C, soleado"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

---

# Ejemplo 2: Gestor de Tareas

---

```python
from mcp.server.fastmcp import FastMCP
from typing import TypedDict
import uuid

mcp = FastMCP("Todo Server")

# Almacenamiento en memoria
tasks = {}


class Task(TypedDict):
    id: str
    title: str
    completed: bool


@mcp.tool()
def create_task(title: str) -> Task:
    """Crea una nueva tarea."""
    task_id = str(uuid.uuid4())[:8]
    task = Task(id=task_id, title=title, completed=False)
    tasks[task_id] = task
    return task


@mcp.tool()
def list_tasks() -> list[Task]:
    """Lista todas las tareas."""
    return list(tasks.values())


@mcp.tool()
def complete_task(task_id: str) -> Task:
    """Marca una tarea como completada."""
    if task_id in tasks:
        tasks[task_id]["completed"] = True
        return tasks[task_id]
    raise ValueError(f"Tarea {task_id} no encontrada")


@mcp.tool()
def delete_task(task_id: str) -> dict:
    """Elimina una tarea."""
    if task_id in tasks:
        deleted = tasks.pop(task_id)
        return {"deleted": True, "task": deleted}
    raise ValueError(f"Tarea {task_id} no encontrada")
```

---

# Ejemplo 3: Calculadora Avanzada

---

```python
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel
import math

mcp = FastMCP("Calculator")


class CalculationResult(BaseModel):
    operation: str
    result: float
    explanation: str


@mcp.tool()
def add(a: float, b: float) -> CalculationResult:
    """Suma dos números."""
    return CalculationResult(
        operation=f"{a} + {b}",
        result=a + b,
        explanation="Suma aritmética básica"
    )


@mcp.tool()
def power(base: float, exponent: float) -> CalculationResult:
    """Calcula una potencia."""
    return CalculationResult(
        operation=f"{base}^{exponent}",
        result=base ** exponent,
        explanation="Exponenciación matemática"
    )


@mcp.tool()
def factorial(n: int, ctx: Context) -> CalculationResult:
    """Calcula el factorial de n."""
    if n < 0:
        raise ValueError("El factorial no está definido para negativos")
    if n > 170:
        raise ValueError("El resultado es demasiado grande")
    
    result = math.factorial(n)
    
    return CalculationResult(
        operation=f"{n}!",
        result=float(result),
        explanation=f"Factorial: producto de 1 a {n}"
    )


@mcp.tool()
async def slow_calculation(
    n: int,
    ctx: Context,
    steps: int = 10
) -> CalculationResult:
    """Cálculo lento con progreso."""
    import asyncio
    
    await ctx.info(f"Iniciando cálculo de {n}")
    
    total = 0
    for i in range(steps):
        await asyncio.sleep(0.1)
        total += n
        await ctx.report_progress(
            progress=(i + 1) / steps,
            total=1.0,
            message=f"Paso {i + 1}/{steps}"
        )
    
    return CalculationResult(
        operation=f"slow_add({n}, {steps} steps)",
        result=float(total),
        explanation="Suma iterativa con delay"
    )
```

---

# Ejemplo 4: Servidor de Archivos

---

```python
from mcp.server.fastmcp import FastMCP, Context
from pathlib import Path
import os

mcp = FastMCP("File Server")


@mcp.tool()
def read_file(path: str) -> str:
    """Lee un archivo de texto."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    return file_path.read_text()


@mcp.tool()
def write_file(path: str, content: str) -> dict:
    """Escribe contenido a un archivo."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)
    return {"path": path, "bytes_written": len(content)}


@mcp.tool()
def list_directory(path: str = ".") -> list[str]:
    """Lista contenido de un directorio."""
    dir_path = Path(path)
    if not dir_path.is_dir():
        raise ValueError(f"No es un directorio: {path}")
    return [str(p) for p in dir_path.iterdir()]


@mcp.resource("file://{path}")
def file_resource(path: str) -> str:
    """Resource de archivo."""
    return read_file(path)


@mcp.prompt(title="File Analysis")
def analyze_file_prompt(file_path: str) -> str:
    """Prompt para analizar un archivo."""
    return f"""Analiza el archivo en {file_path}:

1. Identifica el tipo de archivo
2. Resume su contenido
3. Sugiere mejoras si es código

Usa la herramienta read_file para leer el contenido."""
```

---

# PARTE 10

## Despliegue y Producción

---

# Instalar en Claude Desktop

---

El SDK incluye herramientas para instalar servidores:

---

```bash
# Instalación básica
uv run mcp install server.py

# Con nombre personalizado
uv run mcp install server.py --name "Mi Servidor"

# Con variables de entorno
uv run mcp install server.py -v API_KEY=abc123

# Desde archivo .env
uv run mcp install server.py -f .env
```

---

# Configuración manual

## claude_desktop_config.json

---

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

---

# Servidor HTTP de producción

---

```python
from mcp.server.fastmcp import FastMCP

# Configuración óptima para producción
mcp = FastMCP(
    "Production Server",
    stateless_http=True,      # Sin estado para escalabilidad
    json_response=True,       # JSON más eficiente que SSE
)


@mcp.tool()
def my_tool() -> str:
    return "Hello"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

---

**Ejecutar con uvicorn:**

```bash
uvicorn server:mcp.streamable_http_app() --host 0.0.0.0 --port 8000
```

---

# Autenticación OAuth

---

Para servidores que necesitan autenticación:

---

```python
from mcp.server.auth.provider import TokenVerifier, AccessToken
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl

class MyTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        # Implementar validación de token
        pass


mcp = FastMCP(
    "Protected Server",
    token_verifier=MyTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl("https://auth.example.com"),
        resource_server_url=AnyHttpUrl("http://localhost:8000"),
        required_scopes=["user"]
    )
)
```

---

# Debugging

## MCP Inspector

---

La mejor forma de debuggear servidores MCP:

---

```bash
# Ejecutar servidor en modo desarrollo
uv run mcp dev server.py

# O con el inspector standalone
npx -y @modelcontextprotocol/inspector
```

---

**Características del Inspector:**

- Conexión visual a servidores
- Probar tools interactivamente
- Ver resources y prompts
- Logs en tiempo real
- Debug de errores

---

# Mejores prácticas

---

### ✅ Haz:

- Usar type hints completos
- Documentar tools con docstrings
- Manejar errores apropiadamente
- Usar structured output para datos complejos
- Implementar progress para operaciones largas

---

### ❌ Evita:

- Tools que toman mucho tiempo sin progreso
- Errores sin mensaje claro
- Schemas ambiguos
- Resources con efectos secundarios

---

# Recursos

## Documentación oficial

---

- **SDK Python:** https://github.com/modelcontextprotocol/python-sdk
- **Protocolo MCP:** https://modelcontextprotocol.io
- **Especificación:** https://spec.modelcontextprotocol.io
- **Claude Code:** https://docs.anthropic.com/en/docs/claude-code

---

# Resumen

## Lo que aprendimos

---

✅ FastMCP simplifica la creación de servidores MCP

✅ Tools para acciones, Resources para datos, Prompts para plantillas

✅ Context proporciona logging, progreso y sampling

✅ Múltiples transports: stdio, SSE, HTTP

✅ Integración fácil con Claude Desktop

✅ Configuración de producción con HTTP stateless

---

# ¡Gracias!

## Preguntas

---

**Próximos pasos:**

1. Instalar el SDK: `uv add "mcp[cli]"`

2. Crear tu primer servidor con FastMCP

3. Probar con MCP Inspector

4. Instalar en Claude Desktop

5. ¡Construir herramientas útiles!

---

**Código fuente de esta presentación:**

Basado en https://github.com/modelcontextprotocol/python-sdk

---