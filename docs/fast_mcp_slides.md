# FastMCP: El Framework Definitivo para MCP

---

# ¿Qué es FastMCP?

FastMCP es un framework de Python que simplifica la creación de servidores MCP (Model Context Protocol).

Diseñado por Prefect, proporciona una interfaz declarativa para exponer herramientas, recursos y prompts a clientes MCP como Claude Desktop.

**Filosofía**: Similar a FastAPI — código limpio, tipado fuerte, documentación automática.

---

# El Problema: SDK Oficial

Crear un servidor simple con el SDK oficial de MCP requiere ~50 líneas de código repetitivo:

- Definir schema manualmente
- Implementar `list_tools()` y `call_tool()`
- Manejar serialización
- Gestionar el protocolo MCP

---

# La Solución: FastMCP

El mismo servidor en ~10 líneas:

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

**FastMCP genera automáticamente**: JSON Schema, validación, documentación, protocolo.

---

# Comparación: FastMCP vs SDK Oficial

| Aspecto | SDK Oficial | FastMCP |
|---------|-------------|---------|
| Líneas de código | ~50+ | ~10 |
| Generación de Schema | Manual | Automática |
| Validación de entrada | Manual | Automática |
| Documentación | Mínima | Integrada |
| Testing | Complejo | Cliente integrado |
| Middlewares | No | Sí |
| HTTP Support | Manual | Integrado |

---

# Características Principales

| Característica | Descripción |
|---------------|-------------|
| **Decoradores intuitivos** | `@mcp.tool`, `@mcp.resource`, `@mcp.prompt` |
| **Tipado automático** | JSON Schema desde anotaciones Python |
| **Múltiples transportes** | STDIO, HTTP Streamable, SSE |
| **Cliente integrado** | Para testing y desarrollo |
| **Middlewares** | Logging, rate limiting, autenticación |
| **Autenticación** | OAuth 2.0 y Bearer Token |

---

# Instalación

```bash
# Con pip
pip install fastmcp

# Con uv (recomendado)
uv init my-mcp-server && cd my-mcp-server
uv add fastmcp

# Verificar instalación
fastmcp version
```

---

# Estructura de Proyecto

```
my-mcp-server/
├── src/my_server/
│   ├── server.py       # Servidor principal
│   ├── tools/          # Tools
│   ├── resources/      # Resources
│   └── prompts/        # Prompts
├── tests/
├── pyproject.toml
└── README.md
```

---

# El Servidor FastMCP

---

# Crear un Servidor Básico

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
def hello(name: str) -> str:
    """Say hello."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()  # STDIO por defecto
```

---

# Instrucciones del Servidor

Las instrucciones ayudan a los LLMs a entender tu servidor:

```python
mcp = FastMCP(
    "DataAnalysis",
    instructions="""
    Provides tools for analyzing datasets.
    Start with get_summary() for overview.
    Supported: CSV, JSON, Excel.
    """,
)
```

---

# Los Tres Componentes MCP

| Componente | Descripción | Uso |
|------------|-------------|-----|
| **Tools** | Funciones invocables | Calcular, procesar, consultar |
| **Resources** | Datos de solo lectura | Configuraciones, archivos |
| **Prompts** | Plantillas de mensajes | Guías de análisis |

---

# Transportes Disponibles

| Transporte | Comando | Uso |
|------------|---------|-----|
| **STDIO** | `mcp.run()` | CLI tools, Claude Desktop |
| **HTTP** | `mcp.run(transport="http")` | APIs, producción |
| **SSE** | `mcp.run(transport="sse")` | Legacy (deprecado) |

---

# CLI de FastMCP

```bash
# Ejecutar servidor STDIO
fastmcp run my_server.py

# Ejecutar con HTTP
fastmcp run my_server.py --transport http --port 8000

# Desarrollo con recarga
fastmcp dev my_server.py

# Inspeccionar servidor
fastmcp inspect my_server.py
```

---

# Parámetros del Servidor

```python
mcp = FastMCP(
    name="MyServer",              # Nombre
    instructions="...",           # Instrucciones
    version="1.0.0",             # Versión
    on_duplicate="warn",          # Manejo de duplicados
    strict_input_validation=False,# Validación estricta
    auth=my_auth_provider,        # Autenticación
    middleware=[LoggingMiddleware()], # Middlewares
)
```

---

# Tools (Herramientas)

---

# Concepto de Tools

Los Tools son **funciones invocables** que los clientes pueden ejecutar:

- **Input**: Argumentos con tipos validados
- **Output**: Resultados estructurados
- **Uso**: Realizar acciones, consultar APIs, procesar datos

Son el componente más utilizado en MCP.

---

# Tool Básico

```python
from fastmcp import FastMCP

mcp = FastMCP("MathServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum of a and b
    """
    return a + b
```

---

# Inferencia de Tipos Automática

FastMCP genera el JSON Schema desde las anotaciones:

```python
@mcp.tool
def process(
    text: str,           # string
    count: int,           # integer
    ratio: float = 0.5,   # number con default
    enabled: bool = True # boolean
) -> str:
    return f"Processed: {text}"
```

El cliente recibe automáticamente el schema correcto.

---

# Tipos Soportados

| Tipo Python | JSON Schema |
|-------------|-------------|
| `str` | string |
| `int` | integer |
| `float` | number |
| `bool` | boolean |
| `list[str]` | array of strings |
| `dict[str, int]` | object |
| `Literal["a", "b"]` | enum |

---

# Literales y Enums

```python
from typing import Literal

@mcp.tool
def sort_items(
    items: list[int],
    order: Literal["asc", "desc"] = "asc"
) -> list[int]:
    """Sort items in ascending or descending order."""
    return sorted(items, reverse=(order == "desc"))
```

El cliente solo puede enviar `"asc"` o `"desc"`.

---

# Modelos Pydantic

```python
from pydantic import BaseModel, Field

class UserFilter(BaseModel):
    name: str = Field(description="Name to search")
    age_min: int | None = Field(default=None)
    age_max: int | None = Field(default=None)

@mcp.tool
def search_users(filter: UserFilter) -> list[dict]:
    """Search users with filtering."""
    return [{"name": filter.name}]
```

Pydantic valida automáticamente los inputs.

---

# Parámetros del Decorador

```python
@mcp.tool(
    name="calculate_sum",       # Nombre personalizado
    description="Calculate sum",# Descripción
    tags={"math", "utility"},   # Tags para filtrado
    enabled=True,              # Habilitado
)
def add_numbers(a: int, b: int) -> int:
    return a + b

# Tool deshabilitado
@mcp.tool(enabled=False)
def internal_tool() -> str:
    return "Not exposed"
```

---

# Tools Asíncronos

Para I/O (consultas BD, HTTP), usa `async`:

```python
import aiohttp

@mcp.tool
async def fetch_url(url: str) -> str:
    """Fetch content from a URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

@mcp.tool
async def query_db(sql: str) -> list[dict]:
    """Query database."""
    await asyncio.sleep(0.1)  # Simular async
    return [{"id": 1, "name": "Alice"}]
```

---

# Validación de Entrada

**Modo Flexible (por defecto)**: Convierte tipos compatibles

```python
# Cliente envía: {"count": "10"}
# FastMCP convierte: "10" -> 10
# Resultado: funciona correctamente
```

**Modo Estricto**: Requiere tipos exactos

```python
mcp = FastMCP("Server", strict_input_validation=True)

# Cliente envía: {"count": "10"}
# Error: count must be integer
```

---

# Tipos de Retorno

```python
# String
@mcp.tool
def get_text() -> str:
    return "Hello"

# Diccionario (JSON automático)
@mcp.tool
def get_data() -> dict:
    return {"status": "ok"}

# Lista
@mcp.tool
def get_items() -> list[str]:
    return ["a", "b", "c"]

# Imagen
@mcp.tool
def get_image() -> Image:
    return Image(data=image_bytes, format="png")
```

---

# Manejo de Errores

```python
from fastmcp.exceptions import ToolError

@mcp.tool
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ToolError(
            "Division by zero is not allowed",
            error_code="DIVISION_BY_ZERO"
        )
    return a / b
```

---

# Testing de Tools

```python
import asyncio
from fastmcp import FastMCP, Client

mcp = FastMCP("TestServer")

@mcp.tool
def add(a: int, b: int) -> int:
    return a + b

async def test():
    client = Client(mcp)
    async with client:
        # Listar tools
        tools = await client.list_tools()
        
        # Llamar tool
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"Result: {result.data}")  # 8

asyncio.run(test())
```

---

# Resources (Recursos)

---

# Concepto de Resources

Los Resources son **fuentes de datos de solo lectura**:

- El cliente consulta pero no modifica
- Cada resource tiene una URI única
- Ejemplos: configuraciones, archivos, datos de BD

---

# Resource Estático

```python
from fastmcp import FastMCP

mcp = FastMCP("ResourceServer")

@mcp.resource("config://app")
def get_config() -> dict:
    """Application configuration."""
    return {
        "version": "1.0.0",
        "debug": False
    }

@mcp.resource("data://readme")
def get_readme() -> str:
    """Server README."""
    return "# My MCP Server"
```

---

# URIs de Resources

| URI | Descripción |
|-----|-------------|
| `file:///path/to/data.json` | Archivo local |
| `config://app` | URI scheme personalizado |
| `data://users/active` | Datos con namespace |
| `memory://cache` | Datos en memoria |

---

# Resource Templates

Recursos dinámicos con parámetros en la URI:

```python
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> dict:
    """Get user profile by ID."""
    users = {
        "1": {"id": "1", "name": "Alice"},
        "2": {"id": "2", "name": "Bob"}
    }
    return users.get(user_id, {"error": "Not found"})
```

El cliente llama a `users://123/profile` y FastMCP extrae `user_id="123"`.

---

# Templates con Múltiples Parámetros

```python
@mcp.resource("files://{project}/{filename}")
def get_file(project: str, filename: str) -> str:
    """Get file from project."""
    import os
    path = os.path.join("projects", project, filename)
    with open(path) as f:
        return f.read()
```

---

# Resources con Tipos Complejos

```python
from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    email: str
    active: bool = True

@mcp.resource("users://{user_id}")
def get_user(user_id: str) -> User | None:
    """Get user by ID."""
    return USERS_DB.get(user_id)

@mcp.resource("users://active")
def get_active_users() -> list[User]:
    """Get all active users."""
    return [u for u in USERS_DB.values() if u.active]
```

---

# Resources Binarios

```python
from fastmcp.utilities.types import Image

@mcp.resource("image://logo")
def get_logo() -> Image:
    """Get server logo."""
    with open("logo.png", "rb") as f:
        return Image(data=f.read(), format="png")

@mcp.resource("file://{filename}")
def get_binary_file(filename: str) -> bytes:
    """Get binary file."""
    with open(filename, "rb") as f:
        return f.read()
```

---

# Acceso desde Cliente

```python
from fastmcp import Client

async def main():
    client = Client(mcp)
    async with client:
        # Listar resources
        resources = await client.list_resources()
        
        # Leer resource
        config = await client.read_resource("config://app")
        print(config[0].text)
        
        # Leer template
        user = await client.read_resource("users://123/profile")
```

---

# Prompts

---

# Concepto de Prompts

Los Prompts son **plantillas de mensajes** para guiar interacciones con LLMs:

- Mensajes con variables
- Argumentos parametrizados
- Reutilizables y consistentes

---

# Prompt Básico

```python
from fastmcp import FastMCP

mcp = FastMCP("PromptServer")

@mcp.prompt
def analyze_data(data: str) -> str:
    """Analyze provided data.
    
    Args:
        data: The data to analyze
    """
    return f"Please analyze the following data:\n\n{data}"
```

---

# Prompt con Múltiples Argumentos

```python
@mcp.prompt
def code_review(code: str, language: str = "python") -> str:
    """Review code for improvements."""
    return f"""Review this {language} code:

```{language}
{code}
```

Focus on:
1. Code quality
2. Performance
3. Security
"""
```

---

# Prompt Estructurado

```python
from fastmcp.server.prompts import UserMessage, AssistantMessage, SystemMessage

@mcp.prompt
def analysis_session(dataset: str) -> list:
    """Start analysis session."""
    return [
        SystemMessage("You are a data analyst."),
        UserMessage(f"Analyze: {dataset}"),
        AssistantMessage("I'll help analyze this data."),
    ]
```

---

# Prompt Dinámico

```python
from datetime import datetime

@mcp.prompt
def analyze_with_context(data: str, type: str = "general") -> str:
    """Analyze data with timestamp."""
    context = {
        "timestamp": datetime.now().isoformat(),
        "type": type
    }
    return f"""Analyze (type: {type}):

{data}

Context: {json.dumps(context)}
"""
```

---

# Acceso desde Cliente

```python
from fastmcp import Client

async def main():
    client = Client(mcp)
    async with client:
        # Listar prompts
        prompts = await client.list_prompts()
        
        # Obtener prompt
        result = await client.get_prompt(
            "analyze_data",
            {"data": "1, 2, 3, 4, 5"}
        )
        
        for msg in result.messages:
            print(f"{msg.role}: {msg.content}")
```

---

# Context

---

# ¿Qué es el Context?

El objeto `Context` proporciona acceso a capacidades MCP desde dentro de tus funciones:

| Capacidad | Descripción |
|-----------|-------------|
| Logging | Mensajes al cliente |
| Progress | Reportar progreso |
| Resources | Acceder a resources |
| Sampling | Solicitar generación de LLM |
| Elicitation | Pedir input al usuario |
| Session State | Guardar datos entre requests |

---

# Acceder al Context

```python
from fastmcp import FastMCP, Context
from fastmcp.dependencies import CurrentContext

mcp = FastMCP("ContextDemo")

@mcp.tool
async def process(data: str, ctx: Context = CurrentContext()) -> str:
    """Process data with context."""
    await ctx.info(f"Processing {len(data)} bytes")
    return "Done"
```

El parámetro `ctx` se inyecta automáticamente y no aparece en el schema.

---

# Logging

```python
@mcp.tool
async def analyze(data: list[int], ctx: Context = CurrentContext()) -> dict:
    """Analyze data with logging."""
    await ctx.debug("Starting analysis")
    await ctx.info(f"Analyzing {len(data)} items")
    
    if len(data) > 10000:
        await ctx.warning("Large dataset")
    
    result = {"mean": sum(data) / len(data)}
    
    await ctx.info("Analysis complete")
    return result
```

Niveles: `debug`, `info`, `warning`, `error`

---

# Progress Reporting

```python
@mcp.tool
async def process_file(
    path: str,
    ctx: Context = CurrentContext()
) -> str:
    """Process file with progress."""
    total = 1000
    
    for i in range(total):
        await process_line(i)
        
        if i % 100 == 0:
            await ctx.report_progress(
                progress=i,
                total=total,
                message=f"Processing {i}/{total}"
            )
    
    return "Done"
```

---

# Resource Access desde Tools

```python
@mcp.resource("config://settings")
def get_settings() -> dict:
    return {"api_key": "secret"}

@mcp.tool
async def use_config(ctx: Context = CurrentContext()) -> str:
    """Use config in tool."""
    # Listar resources
    resources = await ctx.list_resources()
    
    # Leer resource
    content = await ctx.read_resource("config://settings")
    settings = content[0].content
    
    return f"Using API: {settings['api_key']}"
```

---

# Session State

```python
@mcp.tool
async def set_value(
    key: str,
    value: str,
    ctx: Context = CurrentContext()
) -> str:
    """Save value in session."""
    await ctx.set_state(key, value)
    return f"Saved {key}"

@mcp.tool
async def get_value(
    key: str,
    ctx: Context = CurrentContext()
) -> str | None:
    """Get value from session."""
    return await ctx.get_state(key)
```

El state está aislado por cliente.

---

# LLM Sampling

```python
@mcp.tool
async def summarize(
    text: str,
    ctx: Context = CurrentContext()
) -> str:
    """Summarize using client's LLM."""
    response = await ctx.sample(
        f"Summarize in 3 sentences:\n\n{text}",
        temperature=0.7,
        max_tokens=200
    )
    return response.text
```

---

# User Elicitation

```python
from pydantic import BaseModel

class UserInfo(BaseModel):
    name: str
    email: str
    age: int

@mcp.tool
async def collect_info(ctx: Context = CurrentContext()) -> dict:
    """Collect user info."""
    result = await ctx.elicit(
        "Please provide your info:",
        response_type=UserInfo
    )
    
    if result.action == "accept":
        return result.data.model_dump()
    return {"status": "cancelled"}
```

---

# Cliente FastMCP

---

# Concepto de Cliente

El cliente (`fastmcp.Client`) proporciona interfaz programática para interactuar con servidores MCP:

- **Testing**: Probar servidores durante desarrollo
- **Integración**: Conectar múltiples servidores
- **Automatización**: Scripts que usan tools MCP

---

# Crear Cliente

```python
import asyncio
from fastmcp import Client, FastMCP

# Servidor de ejemplo
server = FastMCP("TestServer")

@server.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Cliente
async def main():
    client = Client(server)
    
    async with client:
        await client.ping()
        tools = await client.list_tools()
        result = await client.call_tool("greet", {"name": "World"})
        print(result.data)  # "Hello, World!"

asyncio.run(main())
```

---

# Tipos de Transporte

| Tipo | Uso |
|------|-----|
| **In-Memory** | Testing, desarrollo |
| **STDIO** | Claude Desktop, CLI tools |
| **HTTP** | Servicios web, producción |

---

# Cliente STDIO

```python
from fastmcp import Client

# Conectar a servidor Python
client = Client("my_server.py")

# Con variables de entorno
client = Client("my_server.py", env={"API_KEY": "secret"})

# Con comando específico
client = Client(
    command="python",
    args=["my_server.py", "--debug"]
)
```

---

# Cliente HTTP

```python
from fastmcp import Client

# HTTP Streamable (recomendado)
client = Client("https://api.example.com/mcp")

# Con headers de autenticación
client = Client(
    "https://api.example.com/mcp",
    headers={"Authorization": "Bearer token123"}
)
```

---

# Operaciones del Cliente

```python
async with client:
    # Ping
    await client.ping()
    
    # Tools
    tools = await client.list_tools()
    result = await client.call_tool("add", {"a": 5, "b": 3})
    
    # Resources
    resources = await client.list_resources()
    content = await client.read_resource("config://app")
    
    # Prompts
    prompts = await client.list_prompts()
    messages = await client.get_prompt("analyze", {"data": "test"})
```

---

# Callback Handlers

```python
from fastmcp.client.logging import LogMessage

async def log_handler(message: LogMessage):
    print(f"[{message.level}] {message.data}")

async def progress_handler(progress, total, message):
    print(f"Progress: {progress}/{total}")

client = Client(
    "my_server.py",
    log_handler=log_handler,
    progress_handler=progress_handler,
    timeout=30.0
)
```

---

# Testing con Cliente

```python
import pytest
from fastmcp import Client, FastMCP

mcp = FastMCP("TestServer")

@mcp.tool
def add(a: int, b: int) -> int:
    return a + b

@pytest.mark.asyncio
async def test_add():
    client = Client(mcp)
    async with client:
        result = await client.call_tool("add", {"a": 2, "b": 3})
        assert result.data == 5
```

---

# Middlewares

---

# Concepto de Middleware

Los middlewares interceptan cada mensaje MCP:

- **Request**: Antes de procesar
- **Response**: Después de procesar
- **Notification**: En ambas direcciones

Usos: logging, rate limiting, autenticación, métricas.

---

# Middleware Básico

```python
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware

class LoggingMiddleware(Middleware):
    async def on_request(self, request, context):
        print(f"[REQUEST] {request.method}")
        return request
    
    async def on_response(self, response, context):
        print(f"[RESPONSE] {response}")
        return response

mcp = FastMCP("Server", middleware=[LoggingMiddleware()])
```

---

# Middleware con Timing

```python
import time

class TimingMiddleware(Middleware):
    async def on_request(self, request, context):
        context.start_time = time.time()
        return request
    
    async def on_response(self, response, context):
        duration = time.time() - context.start_time
        print(f"Request took {duration:.3f}s")
        return response
```

---

# Rate Limiting

```python
import time
from collections import defaultdict

class RateLimitMiddleware(Middleware):
    def __init__(self, max_requests=100, window=60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    async def on_request(self, request, context):
        client_id = context.client_id or "anon"
        now = time.time()
        
        # Limpiar requests antiguos
        self.requests[client_id] = [
            t for t in self.requests[client_id]
            if t > now - self.window
        ]
        
        if len(self.requests[client_id]) >= self.max_requests:
            raise ToolError("Rate limit exceeded")
        
        self.requests[client_id].append(now)
        return request
```

---

# Múltiples Middlewares

```python
mcp = FastMCP(
    "Server",
    middleware=[
        LoggingMiddleware(),
        RateLimitMiddleware(max_requests=100),
        AuthMiddleware(),
        MetricsMiddleware(),
    ]
)
```

**Orden**: Request fluye del primero al último, Response del último al primero.

---

# Autenticación

---

# Bearer Token

```python
from fastmcp import FastMCP
from fastmcp.server.auth import BearerAuthProvider

auth = BearerAuthProvider(
    tokens=["secret-token-1", "secret-token-2"]
)

mcp = FastMCP("SecureServer", auth=auth)

@mcp.tool
def protected_data() -> str:
    return "Secret information"

if __name__ == "__main__":
    mcp.run(transport="http")
```

---

# OAuth 2.0

```python
from fastmcp.server.auth import OAuthProvider

auth = OAuthProvider(
    issuer="https://auth.example.com",
    client_id="my-mcp-server",
    client_secret="secret",
    authorization_endpoint="https://auth.example.com/authorize",
    token_endpoint="https://auth.example.com/token",
    jwks_uri="https://auth.example.com/.well-known/jwks.json"
)

mcp = FastMCP("OAuthServer", auth=auth)
```

---

# Ocultar Errores

Para producción, oculta detalles de errores internos:

```python
mcp = FastMCP(
    "ProductionServer",
    mask_error_details=True  # Reemplaza detalles con mensaje genérico
)
```

El cliente ve: `"Internal server error"` en lugar de trazas detalladas.

---

# Lifetime Hooks

---

# Concepto de Lifespan

Los lifetime hooks ejecutan código al iniciar/terminar el servidor:

- **Setup**: Inicializar conexiones, cargar config
- **Teardown**: Cerrar conexiones, limpiar recursos

---

# Lifespan Básico

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan(app):
    # Setup
    print("Server starting...")
    app.db = await connect_to_database()
    
    yield {"db": app.db}
    
    # Teardown
    print("Server shutting down...")
    await app.db.close()

mcp = FastMCP("Server", lifespan=app_lifespan)
```

---

# Acceder a Recursos

```python
# Estado global
db = None

@asynccontextmanager
async def app_lifespan(app):
    global db
    db = await Database.connect()
    yield {"db": db}
    await db.disconnect()

mcp = FastMCP("Server", lifespan=app_lifespan)

@mcp.tool
async def query(sql: str) -> list:
    return await db.query(sql)
```

---

# Despliegue

---

# STDIO (Por Defecto)

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

if __name__ == "__main__":
    mcp.run()  # STDIO por defecto
```

Configuración en Claude Desktop:

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

# HTTP Streamable

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```

Con autenticación:

```python
auth = BearerAuthProvider(tokens=["my-token"])
mcp = FastMCP("SecureServer", auth=auth)
mcp.run(transport="http", port=8000)
```

---

# Rutas HTTP Personalizadas

```python
from starlette.responses import PlainTextResponse, JSONResponse

@mcp.custom_route("/health", methods=["GET"])
async def health(request):
    return PlainTextResponse("OK")

@mcp.custom_route("/status", methods=["GET"])
async def status(request):
    return JSONResponse({
        "status": "running",
        "tools": len(mcp._tools)
    })

mcp.run(transport="http", port=8000)
```

---

# Integración con FastAPI

```python
from fastapi import FastAPI
from fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("McpServer")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Montar MCP
@app.on_event("startup")
async def startup():
    mcp_app = mcp.get_http_app()
    app.mount("/mcp", mcp_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
```

---

# Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
```

```bash
docker build -t my-mcp-server .
docker run -p 8000:8000 my-mcp-server
```

---

# Mejores Prácticas

---

# Organización del Código

```
src/my_server/
├── server.py       # Servidor principal
├── tools/
│   ├── users.py    # Tools de usuarios
│   └── data.py     # Tools de datos
├── resources/
│   └── config.py   # Resources
├── prompts/
│   └── analysis.py # Prompts
└── middleware/
    └── logging.py  # Middlewares
```

---

# Usa Type Hints

```python
# ✅ Correcto
@mcp.tool
def process(
    items: list[dict[str, int]],
    threshold: float = 0.5,
    mode: Literal["fast", "slow"] = "fast"
) -> dict[str, float]:
    """Process data with clear types."""
    ...

# ❌ Incorrecto
@mcp.tool
def process(items, threshold=0.5, mode="fast"):
    """Process data."""
    ...
```

---

# Documenta con Docstrings

```python
@mcp.tool
def analyze(data: list[float], method: str = "mean") -> dict:
    """Analyze numerical data.
    
    Args:
        data: List of numbers to analyze
        method: Analysis method (mean, median, mode)
    
    Returns:
        Analysis result with statistics
    
    Raises:
        ValueError: If data is empty
    
    Example:
        >>> analyze([1, 2, 3, 4, 5])
        {"mean": 3.0, "median": 3}
    """
    ...
```

---

# Testing

```python
import pytest
from fastmcp import Client, FastMCP

mcp = FastMCP("TestServer")

@mcp.tool
def add(a: int, b: int) -> int:
    return a + b

@pytest.mark.asyncio
async def test_add():
    client = Client(mcp)
    async with client:
        result = await client.call_tool("add", {"a": 2, "b": 3})
        assert result.data == 5

@pytest.mark.asyncio
async def test_add_negative():
    client = Client(mcp)
    async with client:
        result = await client.call_tool("add", {"a": -1, "b": 1})
        assert result.data == 0
```

---

# Referencia Rápida

---

# Decoradores

| Decorador | Descripción |
|-----------|-------------|
| `@mcp.tool` | Registrar tool |
| `@mcp.resource("uri")` | Registrar resource |
| `@mcp.prompt` | Registrar prompt |
| `@mcp.custom_route("/path")` | Añadir ruta HTTP |

---

# Context Methods

| Método | Descripción |
|--------|-------------|
| `ctx.debug/info/warning/error(msg)` | Logging |
| `ctx.report_progress(p, t, msg)` | Progreso |
| `ctx.list_resources()` | Listar resources |
| `ctx.read_resource(uri)` | Leer resource |
| `ctx.set_state(k, v)` | Guardar state |
| `ctx.get_state(k)` | Leer state |
| `ctx.sample(prompt)` | LLM sampling |
| `ctx.elicit(prompt, type)` | Pedir input |

---

# Cliente Methods

| Método | Descripción |
|--------|-------------|
| `client.ping()` | Verificar conexión |
| `client.list_tools()` | Listar tools |
| `client.call_tool(name, args)` | Llamar tool |
| `client.list_resources()` | Listar resources |
| `client.read_resource(uri)` | Leer resource |
| `client.list_prompts()` | Listar prompts |
| `client.get_prompt(name, args)` | Obtener prompt |

---

# Comandos CLI

| Comando | Descripción |
|---------|-------------|
| `fastmcp run server.py` | Ejecutar STDIO |
| `fastmcp run server.py --transport http` | Ejecutar HTTP |
| `fastmcp dev server.py` | Desarrollo con reload |
| `fastmcp inspect server.py` | Mostrar info |
| `fastmcp version` | Ver versión |

---

# Ejemplo Completo: Servidor de Producción

---

# Servidor Completo (Parte 1)

```python
from fastmcp import FastMCP, Context
from fastmcp.dependencies import CurrentContext
from fastmcp.server.middleware import Middleware
from fastmcp.server.auth import BearerAuthProvider
from pydantic import BaseModel
from typing import Literal

# Modelos
class User(BaseModel):
    id: str
    name: str
    email: str
    role: Literal["admin", "user"]

# Estado global
USERS = {
    "1": User(id="1", name="Alice", email="alice@test.com", role="admin"),
    "2": User(id="2", name="Bob", email="bob@test.com", role="user"),
}
```

---

# Servidor Completo (Parte 2)

```python
# Middlewares
class LoggingMiddleware(Middleware):
    async def on_request(self, request, context):
        print(f">>> {request.method}")
        return request
    
    async def on_response(self, response, context):
        print(f"<<< Response")
        return response

# Autenticación
auth = BearerAuthProvider(tokens=["admin-token"])

# Servidor
mcp = FastMCP(
    "ProductionServer",
    auth=auth,
    middleware=[LoggingMiddleware()],
    mask_error_details=True,
)
```

---

# Servidor Completo (Parte 3: Tools)

```python
@mcp.tool(tags={"users", "read"})
async def list_users(ctx: Context = CurrentContext()) -> list[dict]:
    """List all users."""
    await ctx.info(f"Listing {len(USERS)} users")
    return [u.model_dump() for u in USERS.values()]

@mcp.tool(tags={"users", "write"})
async def create_user(
    name: str,
    email: str,
    role: Literal["admin", "user"] = "user",
    ctx: Context = CurrentContext()
) -> dict:
    """Create a new user."""
    user_id = str(len(USERS) + 1)
    user = User(id=user_id, name=name, email=email, role=role)
    USERS[user_id] = user
    await ctx.info(f"Created user: {name}")
    return user.model_dump()
```

---

# Servidor Completo (Parte 4: Resources y Prompts)

```python
@mcp.resource("users://all")
def get_all_users() -> list[dict]:
    """Get all users."""
    return [u.model_dump() for u in USERS.values()]

@mcp.resource("users://{user_id}")
def get_user(user_id: str) -> User | None:
    """Get user by ID."""
    return USERS.get(user_id)

@mcp.prompt
def analyze_user(user_id: str) -> str:
    """Analyze user data."""
    return f"""Analyze user {user_id}.

Focus on:
1. Activity patterns
2. Engagement metrics
3. Recommendations
"""
```

---

# Servidor Completo (Parte 5: Main)

```python
@mcp.custom_route("/health", methods=["GET"])
async def health(request):
    from starlette.responses import PlainTextResponse
    return PlainTextResponse("OK")

if __name__ == "__main__":
    import sys
    transport = "http" if "--http" in sys.argv else "stdio"
    port = 8000
    
    if "--port" in sys.argv:
        idx = sys.argv.index("--port")
        port = int(sys.argv[idx + 1])
    
    print(f"Starting with transport: {transport}")
    
    if transport == "http":
        mcp.run(transport="http", host="0.0.0.0", port=port)
    else:
        mcp.run()
```

---

# FAQ

---

# FAQ: ¿FastMCP es compatible con Claude Desktop?

**Sí, completamente.**

FastMCP sigue el protocolo MCP estándar, funciona con:

- Claude Desktop
- VS Code con Copilot
- Cualquier cliente MCP compatible

Configuración:

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

# FAQ: ¿Cuándo usar FastMCP vs SDK oficial?

| Situación | Recomendación |
|-----------|---------------|
| Nuevo proyecto | **FastMCP** |
| Necesitas middlewares | **FastMCP** |
| Necesitas cliente de testing | **FastMCP** |
| Control total del protocolo | SDK oficial |
| Proyecto existente | Mantener SDK |

---

# FAQ: ¿Cómo manejo operaciones largas?

Usa **Progress Reporting**:

```python
@mcp.tool
async def long_operation(ctx: Context = CurrentContext()) -> str:
    total = 1000
    for i in range(total):
        await process(i)
        if i % 100 == 0:
            await ctx.report_progress(
                progress=i, total=total,
                message=f"Processing {i}/{total}"
            )
    return "Done"
```

---

# FAQ: ¿Cómo comparto datos entre requests?

Usa **Session State**:

```python
@mcp.tool
async def set_pref(key: str, value: str, ctx: Context = CurrentContext()):
    await ctx.set_state(key, value)
    return "Saved"

@mcp.tool
async def get_pref(key: str, ctx: Context = CurrentContext()):
    return await ctx.get_state(key)
```

El state está aislado por cliente.

---

# Recursos

---

# Enlaces Útiles

| Recurso | URL |
|---------|-----|
| **Documentación oficial** | https://gofastmcp.com |
| **Repositorio GitHub** | https://github.com/PrefectHQ/fastmcp |
| **Ejemplos** | https://github.com/PrefectHQ/fastmcp/tree/main/examples |
| **MCP Spec** | https://modelcontextprotocol.io |

---

# ¡Gracias!

**FastMCP: La forma más productiva de crear servidores MCP**

🔥 Documentación: https://gofastmcp.com

📦 GitHub: https://github.com/PrefectHQ/fastmcp

**¡Feliz coding!** 🚀