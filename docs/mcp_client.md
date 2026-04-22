# Desarrollo de Clientes MCP con Python y FastMCP

## Creación de Clientes MCP, Integración con Agentes CrewAI y Buenas Prácticas

---

# Agenda

1. **Introducción a MCP y Clientes**
2. **FastMCP: Framework para Desarrollo**
3. **Clientes MCP Básicos**
4. **Clientes MCP Avanzados**
5. **Integración con Agentes CrewAI**
6. **Patrones de Diseño**
7. **Buenas Prácticas**
8. **Ejemplos Completos**
9. **Troubleshooting y Debugging**
10. **Recursos y Referencias**

---

# PARTE 1: INTRODUCCIÓN A MCP Y CLIENTES

---

## ¿Qué es MCP?

**Model Context Protocol (MCP)** es un protocolo abierto que estandariza cómo los modelos de lenguaje (LLMs) se conectan con fuentes de datos y herramientas externas.

### Componentes principales:

- **Servidor MCP**: Expone herramientas, recursos y prompts
- **Cliente MCP**: Consume las capacidades del servidor
- **Transporte**: Canal de comunicación (stdio, HTTP, WebSocket)

---

## Arquitectura MCP

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Cliente MCP   │◄───►│    Transporte   │◄───►│  Servidor MCP   │
│   (FastMCP)     │     │   (stdio/HTTP)  │     │   (FastMCP)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                                              │
         │                                              │
         ▼                                              ▼
┌─────────────────�                           ┌─────────────────┐
│   Aplicación   │                           │   Herramientas  │
│   (LLM/Agente) │                           │   Recursos       │
└─────────────────┘                           │   Prompts        │
                                              └─────────────────┘
```

---

## Tipos de Cliente MCP

| Tipo | Descripción | Caso de uso |
|------|-------------|-------------|
| **CLI Client** | Cliente de línea de comandos | Testing, scripts |
| **Library Client** | Biblioteca integrable | Aplicaciones Python |
| **Agent Client** | Cliente con agente de IA | Automatización inteligente |
| **Web Client** | Cliente HTTP/WebSocket | APIs web |

---

## ¿Por qué FastMCP?

### Ventajas sobre el SDK oficial:

| Característica | SDK Oficial | FastMCP |
|----------------|-------------|---------|
| Decoradores | Manual | `@mcp.tool`, `@mcp.resource` |
| Tipado | Básico | Annotated + Field |
| Validación | Manual | Pydantic automático |
| Server + Client | Separados | Integrados |
| Documentación | Externa | Auto-generada |
| Testing | Manual | Fixtures incluidos |

---

# PARTE 2: FASTMCP - FRAMEWORK PARA DESARROLLO

---

## Instalación de FastMCP

```bash
# Instalación básica
pip install fastmcp

# Con dependencias adicionales
pip install "fastmcp[all]"

# Para desarrollo
pip install "fastmcp[dev]"

# Con soporte HTTP
pip install "fastmcp[http]"
```

---

## Estructura de un Proyecto FastMCP

```
mi-proyecto-mcp/
├── src/
│   ├── __init__.py
│   ├── server.py          # Servidor MCP
│   ├── client.py          # Cliente MCP
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── database.py    # Herramientas de BD
│   │   └── filesystem.py  # Herramientas de archivos
│   └── resources/
│       ├── __init__.py
│       └── config.py      # Recursos de configuración
├── tests/
│   ├── __init__.py
│   ├── test_server.py
│   └── test_client.py
├── pyproject.toml
└── README.md
```

---

## Servidor MCP con FastMCP

```python
# server.py
from fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

# Crear servidor
mcp = FastMCP("mi-servidor", version="1.0.0")

# Herramienta con validación
@mcp.tool
def calcular_suma(
    a: Annotated[int, Field(description="Primer número", ge=0)],
    b: Annotated[int, Field(description="Segundo número", ge=0)]
) -> dict:
    """
    Calcula la suma de dos números.
    
    Returns:
        dict con el resultado de la operación
    """
    return {
        "operacion": "suma",
        "a": a,
        "b": b,
        "resultado": a + b
    }

# Recurso dinámico
@mcp.resource("config://{seccion}")
def obtener_config(seccion: str) -> dict:
    """Obtiene configuración de una sección."""
    configs = {
        "database": {"host": "localhost", "port": 5432},
        "api": {"host": "0.0.0.0", "port": 8080}
    }
    return configs.get(seccion, {})

# Prompt parametrizado
@mcp.prompt
def prompt_analisis(datos: str) -> str:
    """Prompt para análisis de datos."""
    return f"""
    Analiza los siguientes datos y proporciona un resumen:
    
    {datos}
    
    Incluye:
    - Puntos clave
    - Tendencias identificadas
    - Recomendaciones
    """

if __name__ == "__main__":
    mcp.run()
```

---

## Ejecutar el Servidor

```bash
# Modo stdio (por defecto)
python server.py

# Modo SSE (Server-Sent Events)
fastmcp run server.py:mcp --transport sse --port 8080

# Con Inspector (debugging)
npx @modelcontextprotocol/inspector python server.py
```

---

# PARTE 3: CLIENTES MCP BÁSICOS

---

## Cliente MCP Simple (stdio)

```python
# client.py
from fastmcp import Client
from fastmcp.client.stdio import StdioServerParameters
from fastmcp.client.transports import StdioTransport

# Configuración del servidor
server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
    env=None
)

# Crear cliente
async def cliente_simple():
    async with Client(StdioTransport(server_params)) as client:
        # Listar herramientas disponibles
        tools = await client.list_tools()
        print("Herramientas disponibles:", [t.name for t in tools])
        
        # Llamar a una herramienta
        resultado = await client.call_tool(
            "calcular_suma",
            {"a": 10, "b": 20}
        )
        print("Resultado:", resultado)
        
        # Listar recursos
        resources = await client.list_resources()
        print("Recursos:", [r.uri for r in resources])
        
        # Leer un recurso
        config = await client.read_resource("config://database")
        print("Config BD:", config)

# Ejecutar
import asyncio
asyncio.run(cliente_simple())
```

---

## Cliente MCP con Context Manager

```python
# client_context.py
from fastmcp import Client
from contextlib import asynccontextmanager
from typing import AsyncIterator

@asynccontextmanager
async def crear_cliente(server_path: str) -> AsyncIterator[Client]:
    """Context manager para cliente MCP."""
    server_params = StdioServerParameters(
        command="python",
        args=[server_path]
    )
    
    client = Client(StdioTransport(server_params))
    
    try:
        await client.connect()
        yield client
    finally:
        await client.disconnect()

# Uso
async def main():
    async with crear_cliente("server.py") as client:
        tools = await client.list_tools()
        print(f"Conectado. {len(tools)} herramientas disponibles.")

asyncio.run(main())
```

---

## Cliente MCP con Reintentos

```python
# client_resilient.py
from fastmcp import Client
from tenacity import retry, stop_after_attempt, wait_exponential
import asyncio

class ClienteResiliente:
    def __init__(self, server_path: str, max_reintentos: int = 3):
        self.server_path = server_path
        self.max_reintentos = max_reintentos
        self._client: Client = None
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def conectar(self) -> None:
        """Conecta al servidor con reintentos."""
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_path]
        )
        self._client = Client(StdioTransport(server_params))
        await self._client.connect()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def llamar_herramienta(self, nombre: str, args: dict):
        """Llama a una herramienta con reintentos."""
        if not self._client:
            raise RuntimeError("Cliente no conectado")
        return await self._client.call_tool(nombre, args)
    
    async def desconectar(self) -> None:
        """Desconecta del servidor."""
        if self._client:
            await self._client.disconnect()

# Uso
async def main():
    cliente = ClienteResiliente("server.py")
    
    try:
        await cliente.conectar()
        resultado = await cliente.llamar_herramienta(
            "calcular_suma",
            {"a": 5, "b": 10}
        )
        print(resultado)
    finally:
        await cliente.desconectar()

asyncio.run(main())
```

---

# PARTE 4: CLIENTES MCP AVANZADOS

---

## Cliente MCP con Pool de Conexiones

```python
# client_pool.py
from fastmcp import Client
from typing import List, Optional
import asyncio

class PoolClientesMCP:
    """Pool de conexiones MCP para alta concurrencia."""
    
    def __init__(
        self,
        server_path: str,
        pool_size: int = 5,
        max_overflow: int = 10
    ):
        self.server_path = server_path
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self._pool: List[Client] = []
        self._available = asyncio.Queue()
        self._lock = asyncio.Lock()
    
    async def inicializar(self):
        """Inicializa el pool de conexiones."""
        for _ in range(self.pool_size):
            client = await self._crear_cliente()
            self._pool.append(client)
            await self._available.put(client)
    
    async def _crear_cliente(self) -> Client:
        """Crea un nuevo cliente."""
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_path]
        )
        client = Client(StdioTransport(server_params))
        await client.connect()
        return client
    
    async def adquirir(self, timeout: float = 30.0) -> Client:
        """Adquiere un cliente del pool."""
        try:
            client = await asyncio.wait_for(
                self._available.get(),
                timeout=timeout
            )
            return client
        except asyncio.TimeoutError:
            # Crear cliente overflow si es posible
            async with self._lock:
                if len(self._pool) < self.pool_size + self.max_overflow:
                    client = await self._crear_cliente()
                    self._pool.append(client)
                    return client
            raise RuntimeError("Pool agotado")
    
    async def liberar(self, client: Client):
        """Libera un cliente al pool."""
        await self._available.put(client)
    
    async def cerrar(self):
        """Cierra todas las conexiones."""
        for client in self._pool:
            try:
                await client.disconnect()
            except Exception:
                pass
        self._pool.clear()

# Uso con context manager
@asynccontextmanager
async def pool_cliente(pool: PoolClientesMCP):
    client = await pool.adquirir()
    try:
        yield client
    finally:
        await pool.liberar(client)

# Ejemplo
async def main():
    pool = PoolClientesMCP("server.py", pool_size=5)
    await pool.inicializar()
    
    try:
        async with pool_cliente(pool) as client:
            resultado = await client.call_tool("calcular_suma", {"a": 1, "b": 2})
            print(resultado)
    finally:
        await pool.cerrar()

asyncio.run(main())
```

---

## Cliente MCP con Cache

```python
# client_cached.py
from fastmcp import Client
from functools import wraps
import hashlib
import json
from typing import Any, Callable
import asyncio

class CacheMCP:
    """Cache para respuestas de MCP."""
    
    def __init__(self, ttl: int = 300):
        self._cache: dict = {}
        self._ttl = ttl
    
    def _hash_key(self, tool: str, args: dict) -> str:
        """Genera clave hash para la llamada."""
        key = f"{tool}:{json.dumps(args, sort_keys=True)}"
        return hashlib.sha256(key.encode()).hexdigest()
    
    async def get_or_call(
        self,
        client: Client,
        tool: str,
        args: dict,
        force_refresh: bool = False
    ) -> Any:
        """Obtiene del cache o llama a la herramienta."""
        key = self._hash_key(tool, args)
        
        if not force_refresh and key in self._cache:
            entry = self._cache[key]
            if asyncio.get_event_loop().time() - entry['timestamp'] < self._ttl:
                return entry['result']
        
        # Llamar a la herramienta
        result = await client.call_tool(tool, args)
        
        # Guardar en cache
        self._cache[key] = {
            'result': result,
            'timestamp': asyncio.get_event_loop().time()
        }
        
        return result
    
    def invalidate(self, tool: str = None, args: dict = None):
        """Invalida cache."""
        if tool is None:
            self._cache.clear()
        elif args is None:
            # Invalidar todas las entradas de esta herramienta
            keys_to_remove = [
                k for k in self._cache
                if k.startswith(f"{tool}:")
            ]
            for k in keys_to_remove:
                del self._cache[k]
        else:
            key = self._hash_key(tool, args)
            self._cache.pop(key, None)

class ClienteConCache:
    """Cliente MCP con cache integrado."""
    
    def __init__(self, server_path: str, cache_ttl: int = 300):
        self.server_path = server_path
        self._client: Client = None
        self._cache = CacheMCP(ttl=cache_ttl)
    
    async def conectar(self):
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_path]
        )
        self._client = Client(StdioTransport(server_params))
        await self._client.connect()
    
    async def call_tool(
        self,
        tool: str,
        args: dict,
        use_cache: bool = True,
        force_refresh: bool = False
    ):
        """Llama a herramienta con cache opcional."""
        if use_cache:
            return await self._cache.get_or_call(
                self._client,
                tool,
                args,
                force_refresh
            )
        return await self._client.call_tool(tool, args)
    
    async def invalidate_cache(self, tool: str = None):
        """Invalida cache."""
        self._cache.invalidate(tool)
    
    async def desconectar(self):
        if self._client:
            await self._client.disconnect()

# Uso
async def main():
    cliente = ClienteConCache("server.py", cache_ttl=600)
    await cliente.conectar()
    
    # Primera llamada (cache miss)
    resultado1 = await cliente.call_tool("calcular_suma", {"a": 1, "b": 2})
    
    # Segunda llamada (cache hit)
    resultado2 = await cliente.call_tool("calcular_suma", {"a": 1, "b": 2})
    
    # Forzar refresh
    resultado3 = await cliente.call_tool(
        "calcular_suma",
        {"a": 1, "b": 2},
        force_refresh=True
    )
    
    await cliente.desconectar()

asyncio.run(main())
```

---

## Cliente MCP con Logging y Métricas

```python
# client_observability.py
from fastmcp import Client
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import asyncio
import logging
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp_client")

@dataclass
class MetricaLlamada:
    """Métrica de una llamada a herramienta."""
    tool: str
    args: dict
    resultado: Any
    duracion_ms: float
    timestamp: datetime
    cache_hit: bool = False
    error: Optional[str] = None

class ClienteObservable:
    """Cliente MCP con logging y métricas."""
    
    def __init__(self, server_path: str):
        self.server_path = server_path
        self._client: Client = None
        self._metricas: List[MetricaLlamada] = []
        self._metricas_por_tool: Dict[str, List[MetricaLlamada]] = {}
    
    async def conectar(self):
        """Conecta al servidor."""
        logger.info(f"Conectando a servidor: {self.server_path}")
        
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_path]
        )
        self._client = Client(StdioTransport(server_params))
        await self._client.connect()
        
        logger.info("Conexión establecida")
        
        # Listar capacidades
        tools = await self._client.list_tools()
        logger.info(f"Herramientas disponibles: {len(tools)}")
        for tool in tools:
            logger.debug(f"  - {tool.name}: {tool.description}")
    
    async def call_tool(
        self,
        tool: str,
        args: dict,
        **kwargs
    ) -> Any:
        """Llama a herramienta con métricas."""
        inicio = time.perf_counter()
        metrica = MetricaLlamada(
            tool=tool,
            args=args,
            resultado=None,
            duracion_ms=0,
            timestamp=datetime.now()
        )
        
        logger.info(f"Llamando herramienta: {tool}")
        logger.debug(f"Argumentos: {args}")
        
        try:
            resultado = await self._client.call_tool(tool, args, **kwargs)
            metrica.resultado = resultado
            logger.info(f"Herramienta {tool} completada")
            logger.debug(f"Resultado: {resultado}")
            
        except Exception as e:
            metrica.error = str(e)
            logger.error(f"Error en {tool}: {e}")
            raise
        
        finally:
            metrica.duracion_ms = (time.perf_counter() - inicio) * 1000
            self._registrar_metrica(metrica)
            logger.debug(f"Duración: {metrica.duracion_ms:.2f}ms")
        
        return resultado
    
    def _registrar_metrica(self, metrica: MetricaLlamada):
        """Registra métrica."""
        self._metricas.append(metrica)
        
        if metrica.tool not in self._metricas_por_tool:
            self._metricas_por_tool[metrica.tool] = []
        self._metricas_por_tool[metrica.tool].append(metrica)
    
    def obtener_estadisticas(self) -> dict:
        """Obtiene estadísticas de uso."""
        stats = {
            "total_llamadas": len(self._metricas),
            "llamadas_exitosas": sum(1 for m in self._metricas if not m.error),
            "llamadas_fallidas": sum(1 for m in self._metricas if m.error),
            "duracion_promedio_ms": 0,
            "por_herramienta": {}
        }
        
        if self._metricas:
            stats["duracion_promedio_ms"] = sum(
                m.duracion_ms for m in self._metricas
            ) / len(self._metricas)
        
        for tool, metricas in self._metricas_por_tool.items():
            stats["por_herramienta"][tool] = {
                "llamadas": len(metricas),
                "exitosas": sum(1 for m in metricas if not m.error),
                "duracion_promedio_ms": sum(
                    m.duracion_ms for m in metricas
                ) / len(metricas) if metricas else 0
            }
        
        return stats
    
    async def desconectar(self):
        """Desconecta del servidor."""
        if self._client:
            await self._client.disconnect()
            logger.info("Desconectado del servidor")

# Uso
async def main():
    cliente = ClienteObservable("server.py")
    
    try:
        await cliente.conectar()
        
        # Realizar algunas llamadas
        for i in range(5):
            await cliente.call_tool("calcular_suma", {"a": i, "b": i * 2})
        
        # Mostrar estadísticas
        stats = cliente.obtener_estadisticas()
        print("Estadísticas:", json.dumps(stats, indent=2, default=str))
        
    finally:
        await cliente.desconectar()

asyncio.run(main())
```

---

# PARTE 5: INTEGRACIÓN CON AGENTES CREWAI

---

## ¿Qué es CrewAI?

**CrewAI** es un framework para crear agentes de IA que colaboran entre sí para completar tareas complejas.

### Componentes:

- **Agent**: Entidad con rol, objetivo y backstory
- **Task**: Tarea específica a completar
- **Crew**: Grupo de agentes que trabajan juntos
- **Tool**: Herramientas que los agentes pueden usar

---

## Arquitectura Cliente MCP + CrewAI

```
┌─────────────────────────────────────────────────────────────┐
│                    APLICACIÓN                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Agent 1   │  │   Agent 2   │  │   Agent 3   │         │
│  │  (Analyst)  │  │ (Researcher)│  │  (Writer)   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          │                                  │
│                          ▼                                  │
│               ┌─────────────────┐                           │
│               │   MCP Client    │                           │
│               │  (FastMCP)      │                           │
│               └────────┬────────┘                           │
│                        │                                    │
└────────────────────────┼────────────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   MCP Server         │
              │   (Tools/Resources)  │
              └─────────────────────┘
```

---

## Cliente MCP como Herramienta CrewAI

```python
# crew_mcp_tool.py
from fastmcp import Client
from fastmcp.client.stdio import StdioServerParameters
from fastmcp.client.transports import StdioTransport
from crewai_tools import tool
from typing import Annotated
from pydantic import Field
import asyncio

class MCPToolFactory:
    """Factoría para crear herramientas CrewAI desde MCP."""
    
    def __init__(self, server_path: str):
        self.server_path = server_path
        self._client: Client = None
        self._tools_cache: dict = {}
    
    async def conectar(self):
        """Conecta al servidor MCP."""
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_path]
        )
        self._client = Client(StdioTransport(server_params))
        await self._client.connect()
    
    async def listar_herramientas(self):
        """Lista herramientas disponibles en el servidor."""
        tools = await self._client.list_tools()
        return tools
    
    def crear_herramienta(self, tool_name: str, tool_schema: dict):
        """Crea una herramienta CrewAI desde una herramienta MCP."""
        
        # Crear función dinámicamente
        async def mcp_tool_func(**kwargs):
            """Ejecuta herramienta MCP."""
            result = await self._client.call_tool(tool_name, kwargs)
            return result
        
        # Crear decorador tool
        @tool(f"{tool_name}_mcp")
        def herramienta_wrapper(**kwargs):
            """Wrapper síncrono para herramienta MCP."""
            return asyncio.run(mcp_tool_func(**kwargs))
        
        return herramienta_wrapper
    
    async def crear_todas_herramientas(self):
        """Crea todas las herramientas del servidor."""
        tools = await self.listar_herramientas()
        crewai_tools = []
        
        for tool in tools:
            crewai_tool = self.crear_herramienta(tool.name, tool.inputSchema)
            crewai_tools.append(crewai_tool)
        
        return crewai_tools
    
    async def desconectar(self):
        """Desconecta del servidor."""
        if self._client:
            await self._client.disconnect()


# Ejemplo de uso
async def crear_herramientas_mcp():
    factory = MCPToolFactory("server.py")
    await factory.conectar()
    
    # Crear herramientas
    tools = await factory.crear_todas_herramientas()
    
    return factory, tools
```

---

## Agente CrewAI con Cliente MCP

```python
# crew_mcp_agent.py
from fastmcp import Client
from fastmcp.client.stdio import StdioServerParameters
from fastmcp.client.transports import StdioTransport
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from typing import List
import asyncio
import json

# Herramienta MCP para CrewAI
class MCPClientTool:
    """Herramienta que envuelve un cliente MCP para CrewAI."""
    
    def __init__(self, client: Client, tool_name: str, description: str):
        self.client = client
        self.tool_name = tool_name
        self.description = description
        self.name = f"mcp_{tool_name}"
    
    async def execute(self, **kwargs):
        """Ejecuta la herramienta MCP."""
        return await self.client.call_tool(self.tool_name, kwargs)
    
    def to_crewai_tool(self):
        """Convierte a herramienta CrewAI."""
        @tool(self.name)
        def herramienta(**kwargs):
            """Herramienta MCP."""
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.execute(**kwargs))
        
        herramienta.description = self.description
        return herramienta


class CrewAIWithMCP:
    """Integración de CrewAI con servidor MCP."""
    
    def __init__(self, server_path: str):
        self.server_path = server_path
        self.client: Client = None
        self.tools: List[MCPClientTool] = []
    
    async def inicializar(self):
        """Inicializa cliente y carga herramientas."""
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_path]
        )
        self.client = Client(StdioTransport(server_params))
        await self.client.connect()
        
        # Cargar herramientas del servidor
        mcp_tools = await self.client.list_tools()
        
        for tool in mcp_tools:
            mcp_tool = MCPClientTool(
                self.client,
                tool.name,
                tool.description
            )
            self.tools.append(mcp_tool)
        
        print(f"Cargadas {len(self.tools)} herramientas MCP")
    
    def crear_agente_analista(self) -> Agent:
        """Crea agente analista."""
        # Obtener herramientas CrewAI
        crewai_tools = [t.to_crewai_tool() for t in self.tools]
        
        return Agent(
            role="Analista de Datos",
            goal="Analizar datos y extraer insights",
            backstory="""Eres un analista experto que utiliza herramientas 
            MCP para procesar y analizar datos. Tu trabajo es interpretar 
            resultados y proporcionar recomendaciones.""",
            tools=crewai_tools,
            verbose=True,
            allow_delegation=False
        )
    
    def crear_agente_investigador(self) -> Agent:
        """Crea agente investigador."""
        crewai_tools = [t.to_crewai_tool() for t in self.tools]
        
        return Agent(
            role="Investigador",
            goal="Investigar y recopilar información",
            backstory="""Eres un investigador que utiliza herramientas MCP
            para buscar y recopilar información relevante.""",
            tools=crewai_tools,
            verbose=True,
            allow_delegation=True
        )
    
    def crear_tarea_analisis(self, agente: Agent, datos: str) -> Task:
        """Crea tarea de análisis."""
        return Task(
            description=f"Analiza los siguientes datos: {datos}",
            agent=agente,
            expected_output="Un análisis detallado con insights y recomendaciones"
        )
    
    def crear_crew(self, agentes: List[Agent], tareas: List[Task]) -> Crew:
        """Crea un crew con los agentes y tareas."""
        return Crew(
            agents=agentes,
            tasks=tareas,
            process=Process.sequential,
            verbose=True
        )
    
    async def ejecutar(self, datos: str) -> str:
        """Ejecuta el análisis."""
        # Crear agentes
        analista = self.crear_agente_analista()
        investigador = self.crear_agente_investigador()
        
        # Crear tareas
        tarea1 = self.crear_tarea_analisis(investigador, datos)
        tarea2 = Task(
            description="Sintetiza los hallazgos del análisis",
            agent=analista,
            expected_output="Un resumen ejecutivo"
        )
        
        # Crear y ejecutar crew
        crew = self.crear_crew(
            [investigador, analista],
            [tarea1, tarea2]
        )
        
        resultado = crew.kickoff()
        return resultado
    
    async def cerrar(self):
        """Cierra la conexión."""
        if self.client:
            await self.client.disconnect()


# Ejemplo completo
async def main():
    # Crear integración
    crew_mcp = CrewAIWithMCP("server.py")
    
    try:
        # Inicializar
        await crew_mcp.inicializar()
        
        # Ejecutar análisis
        resultado = await crew_mcp.ejecutar(
            "Datos de ventas del Q1: 1000, 1200, 1500 unidades"
        )
        
        print("Resultado:", resultado)
        
    finally:
        await crew_mcp.cerrar()

asyncio.run(main())
```

---

## Crew Completo con Múltiples Agentes MCP

```python
# crew_mcp_multiagent.py
from fastmcp import Client
from fastmcp.client.stdio import StdioServerParameters
from fastmcp.client.transports import StdioTransport
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from typing import List, Dict, Any
import asyncio

class MultiAgentMCPClient:
    """Cliente MCP con múltiples agentes CrewAI."""
    
    def __init__(self, server_path: str):
        self.server_path = server_path
        self.client: Client = None
        self.mcp_tools: List[Dict] = []
    
    async def inicializar(self):
        """Inicializa cliente MCP."""
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_path]
        )
        self.client = Client(StdioTransport(server_params))
        await self.client.connect()
        
        # Cargar herramientas
        tools = await self.client.list_tools()
        self.mcp_tools = [
            {"name": t.name, "description": t.description}
            for t in tools
        ]
        
        print(f"Cargadas {len(self.mcp_tools)} herramientas MCP")
    
    def _crear_herramienta(self, tool_name: str):
        """Crea herramienta CrewAI desde MCP."""
        @tool(f"mcp_{tool_name}")
        async def herramienta_mcp(**kwargs):
            """Herramienta MCP."""
            return await self.client.call_tool(tool_name, kwargs)
        
        return herramienta_mcp
    
    def crear_agente_orquestador(self) -> Agent:
        """Agente que orquesta a los demás."""
        return Agent(
            role="Orquestador",
            goal="Coordinar agentes y distribuir tareas",
            backstory="""Eres el orquestador principal. Tu trabajo es 
            coordinar a los agentes especialistas y asegurar que 
            cada tarea sea asignada al agente correcto.""",
            verbose=True,
            allow_delegation=True
        )
    
    def crear_agente_datos(self) -> Agent:
        """Agente especialista en datos."""
        tools = [self._crear_herramienta("calcular_suma")]
        
        return Agent(
            role="Especialista en Datos",
            goal="Procesar y analizar datos numéricos",
            backstory="""Eres un especialista en análisis de datos. 
            Utilizas herramientas MCP para realizar cálculos y 
            transformaciones de datos.""",
            tools=tools,
            verbose=True
        )
    
    def crear_agente_investigacion(self) -> Agent:
        """Agente especialista en investigación."""
        tools = [self._crear_herramienta("obtener_config")]
        
        return Agent(
            role="Investigador",
            goal="Buscar y recopilar información",
            backstory="""Eres un investigador experto. Utilizas 
            herramientas MCP para acceder a recursos y bases de datos.""",
            tools=tools,
            verbose=True
        )
    
    def crear_agente_escritor(self) -> Agent:
        """Agente especialista en redacción."""
        return Agent(
            role="Escritor Técnico",
            goal="Crear documentos y reportes",
            backstory="""Eres un escritor técnico experto. Tu trabajo 
            es sintetizar la información en documentos claros y 
            profesionales.""",
            verbose=True
        )
    
    def crear_flujo_analisis(
        self,
        datos: str
    ) -> Crew:
        """Crea flujo de análisis completo."""
        
        # Agentes
        orquestador = self.crear_agente_orquestador()
        especialista_datos = self.crear_agente_datos()
        investigador = self.crear_agente_investigacion()
        escritor = self.crear_agente_escritor()
        
        # Tareas
        tarea1 = Task(
            description=f"Analiza los datos: {datos}",
            agent=especialista_datos,
            expected_output="Análisis numérico detallado"
        )
        
        tarea2 = Task(
            description="Investiga contexto adicional para el análisis",
            agent=investigador,
            expected_output="Información de contexto relevante"
        )
        
        tarea3 = Task(
            description="Sintetiza análisis e investigación en reporte",
            agent=escritor,
            expected_output="Reporte final en formato markdown"
        )
        
        tarea4 = Task(
            description="Revisa y valida el reporte final",
            agent=orquestador,
            expected_output="Reporte validado y aprobado"
        )
        
        # Crew
        crew = Crew(
            agents=[
                orquestador,
                especialista_datos,
                investigador,
                escritor
            ],
            tasks=[tarea1, tarea2, tarea3, tarea4],
            process=Process.sequential,
            verbose=True
        )
        
        return crew
    
    async def ejecutar_analisis(self, datos: str) -> str:
        """Ejecuta análisis con múltiples agentes."""
        crew = self.crear_flujo_analisis(datos)
        resultado = crew.kickoff()
        return resultado
    
    async def cerrar(self):
        """Cierra conexión MCP."""
        if self.client:
            await self.client.disconnect()


# Ejemplo de uso
async def main():
    cliente = MultiAgentMCPClient("server.py")
    
    try:
        await cliente.inicializar()
        
        # Datos de ejemplo
        datos_ventas = """
        Ventas Q1: $1,500,000
        Ventas Q2: $1,750,000
        Ventas Q3: $1,600,000
        Ventas Q4: $2,000,000
        """
        
        # Ejecutar análisis
        resultado = await cliente.ejecutar_analisis(datos_ventas)
        
        print("\n" + "="*50)
        print("RESULTADO DEL ANÁLISIS")
        print("="*50)
        print(resultado)
        
    finally:
        await cliente.cerrar()

asyncio.run(main())
```

---

## Ejemplo: Agente de Investigación con MCP

```python
# research_agent_mcp.py
from fastmcp import Client
from fastmcp.client.stdio import StdioServerParameters
from fastmcp.client.transports import StdioTransport
from crewai import Agent, Task, Crew
from crewai_tools import tool, SerperDevTool
from typing import Annotated
from pydantic import Field
import asyncio
import os

class ResearchAgentMCP:
    """Agente de investigación que usa MCP y herramientas web."""
    
    def __init__(self, server_path: str):
        self.server_path = server_path
        self.client: Client = None
    
    async def inicializar(self):
        """Inicializa cliente MCP."""
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_path]
        )
        self.client = Client(StdioTransport(server_params))
        await self.client.connect()
    
    @tool("buscar_documentos_mcp")
    async def buscar_documentos(
        query: Annotated[str, Field(description="Término de búsqueda")]
    ) -> str:
        """Busca documentos usando MCP."""
        # Supongamos que el servidor MCP tiene una herramienta de búsqueda
        result = await self.client.call_tool("buscar", {"query": query})
        return result
    
    def crear_agente_investigador(self) -> Agent:
        """Crea agente investigador."""
        # Herramientas
        serper = SerperDevTool()
        
        return Agent(
            role="Investigador Senior",
            goal="Conducir investigaciones exhaustivas y recopilar información",
            backstory="""Eres un investigador senior con años de experiencia.
            Tienes acceso a bases de datos MCP y herramientas de búsqueda web.
            Tu trabajo es encontrar información precisa y relevante.""",
            tools=[serper, self.buscar_documentos],
            verbose=True,
            max_iter=10,
            max_rpm=60
        )
    
    def crear_tarea_investigacion(
        self,
        tema: str,
        agente: Agent
    ) -> Task:
        """Crea tarea de investigación."""
        return Task(
            description=f"""
            Investiga el siguiente tema de forma exhaustiva: {tema}
            
            Tu investigación debe incluir:
            1. Contexto histórico
            2. Estado actual
            3. Tendencias futuras
            4. Referencias y fuentes
            
            Utiliza las herramientas disponibles para recopilar información.
            """,
            agent=agente,
            expected_output="""
            Un reporte de investigación estructurado con:
            - Resumen ejecutivo
            - Hallazgos principales
            - Fuentes consultadas
            - Conclusiones
            """
        )
    
    def crear_crew(self, tema: str) -> Crew:
        """Crea crew de investigación."""
        agente = self.crear_agente_investigador()
        tarea = self.crear_tarea_investigacion(tema, agente)
        
        return Crew(
            agents=[agente],
            tasks=[tarea],
            verbose=True
        )
    
    async def investigar(self, tema: str) -> str:
        """Ejecuta investigación."""
        crew = self.crear_crew(tema)
        resultado = crew.kickoff()
        return resultado
    
    async def cerrar(self):
        """Cierra conexión."""
        if self.client:
            await self.client.disconnect()


# Ejemplo
async def main():
    # Configurar API key para SerperDev
    os.environ["SERPER_API_KEY"] = "tu-api-key"
    
    agente = ResearchAgentMCP("server.py")
    
    try:
        await agente.inicializar()
        
        resultado = await agente.investigar(
            "Inteligencia Artificial Generativa en 2024"
        )
        
        print(resultado)
        
    finally:
        await agente.cerrar()

asyncio.run(main())
```

---

# PARTE 6: PATRONES DE DISEÑO

---

## Patrón Repository para MCP

```python
# pattern_repository.py
from fastmcp import Client
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from dataclasses import dataclass
import asyncio

T = TypeVar('T')

@dataclass
class Filtro:
    """Filtro genérico para búsquedas."""
    campo: str
    operador: str
    valor: Any

class MCPRepository(ABC, Generic[T]):
    """Repositorio abstracto sobre MCP."""
    
    def __init__(self, client: Client, tool_prefix: str):
        self.client = client
        self.tool_prefix = tool_prefix
    
    async def obtener_todos(self) -> List[T]:
        """Obtiene todos los registros."""
        return await self.client.call_tool(
            f"{self.tool_prefix}_list",
            {}
        )
    
    async def obtener_por_id(self, id: str) -> Optional[T]:
        """Obtiene por ID."""
        return await self.client.call_tool(
            f"{self.tool_prefix}_get",
            {"id": id}
        )
    
    async def crear(self, entidad: T) -> T:
        """Crea nueva entidad."""
        return await self.client.call_tool(
            f"{self.tool_prefix}_create",
            entidad
        )
    
    async def actualizar(self, id: str, entidad: T) -> T:
        """Actualiza entidad."""
        return await self.client.call_tool(
            f"{self.tool_prefix}_update",
            {"id": id, **entidad}
        )
    
    async def eliminar(self, id: str) -> bool:
        """Elimina entidad."""
        return await self.client.call_tool(
            f"{self.tool_prefix}_delete",
            {"id": id}
        )
    
    async def buscar(self, filtros: List[Filtro]) -> List[T]:
        """Busca con filtros."""
        return await self.client.call_tool(
            f"{self.tool_prefix}_search",
            {"filtros": [f.__dict__ for f in filtros]}
        )


# Implementación concreta
@dataclass
class Usuario:
    id: str
    nombre: str
    email: str
    activo: bool

class UsuarioRepository(MCPRepository[Usuario]):
    """Repositorio de usuarios sobre MCP."""
    
    def __init__(self, client: Client):
        super().__init__(client, "usuario")
    
    async def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca usuario por email."""
        resultados = await self.buscar([
            Filtro("email", "==", email)
        ])
        return resultados[0] if resultados else None
    
    async def listar_activos(self) -> List[Usuario]:
        """Lista usuarios activos."""
        return await self.buscar([
            Filtro("activo", "==", True)
        ])


# Uso
async def main():
    client = Client(StdioTransport(
        StdioServerParameters(command="python", args=["server.py"])
    ))
    await client.connect()
    
    repo = UsuarioRepository(client)
    
    # Crear usuario
    nuevo = await repo.crear({
        "nombre": "Juan Pérez",
        "email": "juan@example.com",
        "activo": True
    })
    
    # Buscar por email
    usuario = await repo.buscar_por_email("juan@example.com")
    
    # Listar activos
    activos = await repo.listar_activos()
    
    await client.disconnect()

asyncio.run(main())
```

---

## Patrón Observer para Eventos MCP

```python
# pattern_observer.py
from fastmcp import Client
from typing import Callable, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
import asyncio

class EventType(Enum):
    """Tipos de eventos MCP."""
    TOOL_CALLED = "tool_called"
    TOOL_COMPLETED = "tool_completed"
    TOOL_ERROR = "tool_error"
    RESOURCE_READ = "resource_read"
    PROMPT_USED = "prompt_used"

@dataclass
class EventoMCP:
    """Evento del sistema MCP."""
    tipo: EventType
    tool: str
    args: dict
    resultado: Any = None
    error: str = None
    timestamp: float = None

class ObservadorMCP(ABC):
    """Observador de eventos MCP."""
    
    @abstractmethod
    async def actualizar(self, evento: EventoMCP):
        """Actualiza el observador."""
        pass

class LogObservador(ObservadorMCP):
    """Observador que registra logs."""
    
    async def actualizar(self, evento: EventoMCP):
        if evento.error:
            print(f"[ERROR] {evento.tipo.value}: {evento.tool} - {evento.error}")
        else:
            print(f"[INFO] {evento.tipo.value}: {evento.tool}")

class MetricasObservador(ObservadorMCP):
    """Observador que recolecta métricas."""
    
    def __init__(self):
        self.metricas: Dict[str, List[float]] = {}
    
    async def actualizar(self, evento: EventoMCP):
        if evento.tipo == EventType.TOOL_COMPLETED:
            if evento.tool not in self.metricas:
                self.metricas[evento.tool] = []
            # Duración sería calculada en el cliente observable
            self.metricas[evento.tool].append(evento.timestamp or 0)
    
    def obtener_promedios(self) -> Dict[str, float]:
        return {
            tool: sum(tiempos) / len(tiempos)
            for tool, tiempos in self.metricas.items()
        }

class ClienteMCPObservable:
    """Cliente MCP con patrón Observer."""
    
    def __init__(self, server_path: str):
        self.server_path = server_path
        self.client: Client = None
        self.observadores: List[ObservadorMCP] = []
        self._tiempos: Dict[str, float] = {}
    
    def agregar_observador(self, observador: ObservadorMCP):
        """Agrega observador."""
        self.observadores.append(observador)
    
    def remover_observador(self, observador: ObservadorMCP):
        """Remueve observador."""
        self.observadores.remove(observador)
    
    async def _notificar(self, evento: EventoMCP):
        """Notifica a todos los observadores."""
        for observador in self.observadores:
            await observador.actualizar(evento)
    
    async def conectar(self):
        """Conecta al servidor."""
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_path]
        )
        self.client = Client(StdioTransport(server_params))
        await self.client.connect()
    
    async def call_tool(self, tool: str, args: dict) -> Any:
        """Llama herramienta con notificación."""
        inicio = asyncio.get_event_loop().time()
        
        # Notificar inicio
        await self._notificar(EventoMCP(
            tipo=EventType.TOOL_CALLED,
            tool=tool,
            args=args,
            timestamp=inicio
        ))
        
        try:
            resultado = await self.client.call_tool(tool, args)
            
            # Notificar completado
            await self._notificar(EventoMCP(
                tipo=EventType.TOOL_COMPLETED,
                tool=tool,
                args=args,
                resultado=resultado,
                timestamp=asyncio.get_event_loop().time() - inicio
            ))
            
            return resultado
            
        except Exception as e:
            # Notificar error
            await self._notificar(EventoMCP(
                tipo=EventType.TOOL_ERROR,
                tool=tool,
                args=args,
                error=str(e),
                timestamp=asyncio.get_event_loop().time() - inicio
            ))
            raise
    
    async def desconectar(self):
        """Desconecta."""
        if self.client:
            await self.client.disconnect()

# Uso
async def main():
    cliente = ClienteMCPObservable("server.py")
    
    # Agregar observadores
    cliente.agregar_observador(LogObservador())
    metricas = MetricasObservador()
    cliente.agregar_observador(metricas)
    
    await cliente.conectar()
    
    try:
        # Realizar operaciones
        await cliente.call_tool("calcular_suma", {"a": 1, "b": 2})
        await cliente.call_tool("calcular_suma", {"a": 5, "b": 10})
        
        # Ver métricas
        print("Promedios:", metricas.obtener_promedios())
        
    finally:
        await cliente.desconectar()

asyncio.run(main())
```

---

## Patrón Factory para Clientes MCP

```python
# pattern_factory.py
from fastmcp import Client
from fastmcp.client.stdio import StdioServerParameters
from fastmcp.client.transports import StdioTransport, HttpClientTransport
from typing import Protocol, Optional
from enum import Enum
import os

class TransportType(Enum):
    """Tipos de transporte."""
    STDIO = "stdio"
    HTTP = "http"
    WEBSOCKET = "websocket"

class MCPClientFactory:
    """Factoría para crear clientes MCP."""
    
    @staticmethod
    def crear_cliente(
        server_type: TransportType,
        **kwargs
    ) -> Client:
        """Crea cliente según el tipo de servidor."""
        
        if server_type == TransportType.STDIO:
            return MCPClientFactory._crear_stdio_client(**kwargs)
        elif server_type == TransportType.HTTP:
            return MCPClientFactory._crear_http_client(**kwargs)
        elif server_type == TransportType.WEBSOCKET:
            return MCPClientFactory._crear_websocket_client(**kwargs)
        else:
            raise ValueError(f"Tipo de servidor no soportado: {server_type}")
    
    @staticmethod
    def _crear_stdio_client(
        command: str = "python",
        args: list = None,
        env: dict = None
    ) -> Client:
        """Crea cliente stdio."""
        params = StdioServerParameters(
            command=command,
            args=args or [],
            env=env
        )
        return Client(StdioTransport(params))
    
    @staticmethod
    def _crear_http_client(
        url: str,
        headers: dict = None
    ) -> Client:
        """Crea cliente HTTP."""
        return Client(HttpClientTransport(url, headers=headers))
    
    @staticmethod
    def _crear_websocket_client(url: str) -> Client:
        """Crea cliente WebSocket."""
        # WebSocket transport aún en desarrollo
        raise NotImplementedError("WebSocket transport no implementado")


class MCPClientBuilder:
    """Builder para configurar cliente MCP."""
    
    def __init__(self):
        self._transport_type: TransportType = TransportType.STDIO
        self._command: str = "python"
        self._args: list = []
        self._env: dict = {}
        self._url: str = None
        self._headers: dict = {}
        self._cache_enabled: bool = False
        self._cache_ttl: int = 300
        self._retry_count: int = 3
        self._timeout: int = 30
    
    def con_stdio(self, command: str, args: list = None) -> 'MCPClientBuilder':
        """Configura transporte stdio."""
        self._transport_type = TransportType.STDIO
        self._command = command
        self._args = args or []
        return self
    
    def con_http(self, url: str, headers: dict = None) -> 'MCPClientBuilder':
        """Configura transporte HTTP."""
        self._transport_type = TransportType.HTTP
        self._url = url
        self._headers = headers or {}
        return self
    
    def con_env(self, env: dict) -> 'MCPClientBuilder':
        """Añade variables de entorno."""
        self._env.update(env)
        return self
    
    def con_cache(self, ttl: int = 300) -> 'MCPClientBuilder':
        """Habilita cache."""
        self._cache_enabled = True
        self._cache_ttl = ttl
        return self
    
    def con_reintentos(self, count: int) -> 'MCPClientBuilder':
        """Configura reintentos."""
        self._retry_count = count
        return self
    
    def con_timeout(self, timeout: int) -> 'MCPClientBuilder':
        """Configura timeout."""
        self._timeout = timeout
        return self
    
    def build(self) -> Client:
        """Construye el cliente."""
        client = MCPClientFactory.crear_cliente(
            self._transport_type,
            command=self._command,
            args=self._args,
            env=self._env,
            url=self._url,
            headers=self._headers
        )
        
        # Aplicar decoradores según configuración
        if self._cache_enabled:
            client = self._aplicar_cache(client)
        
        if self._retry_count > 0:
            client = self._aplicar_reintentos(client)
        
        return client
    
    def _aplicar_cache(self, client: Client) -> Client:
        """Aplica decorador de cache."""
        # Implementar decorador de cache
        # (ver ejemplo anterior de ClienteConCache)
        return client
    
    def _aplicar_reintentos(self, client: Client) -> Client:
        """Aplica decorador de reintentos."""
        # Implementar decorador de reintentos
        # (ver ejemplo anterior de ClienteResiliente)
        return client


# Uso con Builder
async def main():
    # Cliente stdio simple
    client1 = (MCPClientBuilder()
        .con_stdio("python", ["server.py"])
        .con_env({"DEBUG": "1"})
        .build())
    
    # Cliente HTTP con cache
    client2 = (MCPClientBuilder()
        .con_http("http://localhost:8080/mcp")
        .con_cache(ttl=600)
        .con_reintentos(3)
        .build())
    
    # Usar clientes
    await client1.connect()
    # ...
    await client1.disconnect()

asyncio.run(main())
```

---

# PARTE 7: BUENAS PRÁCTICAS

---

## 1. Gestión de Conexiones

### ✅ Correcto

```python
# Usar context managers
async with Client(transport) as client:
    result = await client.call_tool("mi_herramienta", args)
```

### ❌ Incorrecto

```python
# Olvidar desconectar
client = Client(transport)
await client.connect()
result = await client.call_tool("mi_herramienta", args)
# ¡Falta client.disconnect()!
```

---

## 2. Manejo de Errores

### ✅ Correcto

```python
try:
    result = await client.call_tool("herramienta", args)
except MCPError as e:
    logger.error(f"Error MCP: {e}")
    # Manejar error específico
except Exception as e:
    logger.exception(f"Error inesperado: {e}")
    raise
finally:
    await client.disconnect()
```

### ❌ Incorrecto

```python
result = await client.call_tool("herramienta", args)
# Sin manejo de errores
```

---

## 3. Validación de Entradas

### ✅ Correcto

```python
from pydantic import BaseModel, Field, validator

class EntradaValidada(BaseModel):
    valor: int = Field(..., ge=0, le=100)
    nombre: str = Field(..., min_length=1, max_length=50)
    
    @validator('nombre')
    def nombre_sin_espacios(cls, v):
        return v.strip()

# Validar antes de enviar
try:
    entrada = EntradaValidada(valor=10, nombre="  test  ")
    result = await client.call_tool("herramienta", entrada.dict())
except ValidationError as e:
    logger.error(f"Validación fallida: {e}")
```

### ❌ Incorrecto

```python
# Sin validación
result = await client.call_tool("herramienta", {
    "valor": -5,  # Valor inválido
    "nombre": ""  # Nombre vacío
})
```

---

## 4. Timeout y Reintentos

### ✅ Correcto

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(MCPTimeoutError)
)
async def llamar_con_reintentos(client, tool, args, timeout=30):
    return await asyncio.wait_for(
        client.call_tool(tool, args),
        timeout=timeout
    )
```

### ❌ Incorrecto

```python
# Sin timeout ni reintentos
result = await client.call_tool("herramienta", args)
# Puede colgar indefinidamente
```

---

## 5. Logging y Observabilidad

### ✅ Correcto

```python
import logging
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger("mcp_client")

@dataclass
class CallMetric:
    tool: str
    args: dict
    duration_ms: float
    success: bool
    error: str = None

async def llamar_con_metricas(client, tool, args):
    start = datetime.now()
    try:
        result = await client.call_tool(tool, args)
        metric = CallMetric(
            tool=tool,
            args=args,
            duration_ms=(datetime.now() - start).total_seconds() * 1000,
            success=True
        )
        logger.info(f"Métrica: {metric}")
        return result
    except Exception as e:
        metric = CallMetric(
            tool=tool,
            args=args,
            duration_ms=(datetime.now() - start).total_seconds() * 1000,
            success=False,
            error=str(e)
        )
        logger.error(f"Error: {metric}")
        raise
```

---

## 6. Configuración por Entorno

### ✅ Correcto

```python
from pydantic import BaseSettings

class MCPConfig(BaseSettings):
    server_command: str = "python"
    server_args: list = ["server.py"]
    timeout: int = 30
    retry_count: int = 3
    cache_ttl: int = 300
    
    class Config:
        env_prefix = "MCP_"

# config.py
config = MCPConfig(
    server_command=os.getenv("MCP_SERVER_COMMAND", "python"),
    server_args=os.getenv("MCP_SERVER_ARGS", "server.py").split(),
    timeout=int(os.getenv("MCP_TIMEOUT", "30"))
)
```

### ❌ Incorrecto

```python
# Hardcoded
server_params = StdioServerParameters(
    command="python",
    args=["server.py"]
)
timeout = 30
```

---

## 7. Testing

### ✅ Correcto

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
async def mock_client():
    """Cliente MCP mockeado para tests."""
    client = AsyncMock(spec=Client)
    client.call_tool = AsyncMock(return_value={"result": "ok"})
    yield client

@pytest.mark.asyncio
async def test_llamada_herramienta(mock_client):
    result = await mock_client.call_tool("test_tool", {"arg": "value"})
    assert result["result"] == "ok"
    mock_client.call_tool.assert_called_once()

# Integration test con servidor real
@pytest.mark.integration
async def test_con_servidor_real():
    async with Client(StdioTransport(
        StdioServerParameters(command="python", args=["test_server.py"])
    )) as client:
        result = await client.call_tool("echo", {"message": "hello"})
        assert result == {"message": "hello"}
```

---

## 8. Seguridad

### ✅ Correcto

```python
import os
from typing import Optional

class SecureMCPClient:
    """Cliente MCP con prácticas seguras."""
    
    def __init__(self):
        # No hardcodear secrets
        self.api_key = os.getenv("MCP_API_KEY")
        if not self.api_key:
            raise ValueError("MCP_API_KEY no configurada")
        
        # Validar entradas
        self.max_args_size = 1024 * 1024  # 1MB max
    
    def validate_args(self, args: dict) -> dict:
        """Valida argumentos antes de enviar."""
        # Tamaño
        if len(str(args)) > self.max_args_size:
            raise ValueError("Argumentos demasiado grandes")
        
        # Sanitizar
        sanitized = {}
        for key, value in args.items():
            if isinstance(value, str):
                # Prevenir inyección
                value = value.replace("\x00", "")
            sanitized[key] = value
        
        return sanitized
    
    async def call_tool(self, tool: str, args: dict):
        """Llama herramienta de forma segura."""
        # Validar
        args = self.validate_args(args)
        
        # Autorización (si aplica)
        if self._requires_auth(tool):
            if not self.api_key:
                raise PermissionError("Autorización requerida")
        
        # Llamar
        return await self.client.call_tool(tool, args)
    
    def _requires_auth(self, tool: str) -> bool:
        """Verifica si la herramienta requiere autorización."""
        restricted_tools = {"delete_user", "update_config"}
        return tool in restricted_tools
```

---

## 9. Performance

### ✅ Correcto

```python
# Cache para llamadas repetitivas
from functools import lru_cache
import hashlib
import json

class CachedMCPClient:
    def __init__(self, client: Client, ttl: int = 300):
        self.client = client
        self.ttl = ttl
        self._cache: dict = {}
        self._cache_times: dict = {}
    
    def _cache_key(self, tool: str, args: dict) -> str:
        """Genera clave de cache."""
        key = f"{tool}:{json.dumps(args, sort_keys=True)}"
        return hashlib.sha256(key.encode()).hexdigest()
    
    async def call_tool(self, tool: str, args: dict, use_cache: bool = True):
        """Llama herramienta con cache."""
        if not use_cache:
            return await self.client.call_tool(tool, args)
        
        key = self._cache_key(tool, args)
        
        # Verificar cache
        if key in self._cache:
            cache_time = self._cache_times.get(key, 0)
            if time.time() - cache_time < self.ttl:
                return self._cache[key]
        
        # Llamar y cachear
        result = await self.client.call_tool(tool, args)
        self._cache[key] = result
        self._cache_times[key] = time.time()
        
        return result
    
    def invalidate(self, tool: str = None):
        """Invalida cache."""
        if tool is None:
            self._cache.clear()
            self._cache_times.clear()
        else:
            keys_to_remove = [
                k for k in self._cache
                if k.startswith(f"{tool}:")
            ]
            for k in keys_to_remove:
                del self._cache[k]
                del self._cache_times[k]
```

---

## 10. Documentación

### ✅ Correcto

```python
class MCPClientWrapper:
    """
    Wrapper para cliente MCP con funcionalidades adicionales.
    
    Este wrapper proporciona:
    - Cache automático
    - Reintentos configurables
    - Logging integrado
    - Métricas de uso
    
    Ejemplo:
        ```python
        async with MCPClientWrapper("server.py") as client:
            result = await client.call_tool("calc", {"a": 1, "b": 2})
            print(result)
        ```
    
    Args:
        server_path: Ruta al script del servidor MCP
        cache_ttl: Tiempo de vida del cache en segundos (default: 300)
        retry_count: Número de reintentos (default: 3)
    
    Raises:
        MCPConnectionError: Si no puede conectar al servidor
        MCPToolError: Si la herramienta falla
    """
    
    def __init__(
        self,
        server_path: str,
        cache_ttl: int = 300,
        retry_count: int = 3
    ):
        """
        Inicializa el wrapper.
        
        Args:
            server_path: Ruta al servidor MCP
            cache_ttl: TTL del cache en segundos
            retry_count: Número de reintentos
        """
        self.server_path = server_path
        self.cache_ttl = cache_ttl
        self.retry_count = retry_count
        self._client: Client = None
        self._cache: dict = {}
    
    async def call_tool(
        self,
        tool: str,
        args: dict,
        use_cache: bool = True
    ) -> Any:
        """
        Llama a una herramienta del servidor MCP.
        
        Args:
            tool: Nombre de la herramienta
            args: Argumentos para la herramienta
            use_cache: Si usar cache (default: True)
        
        Returns:
            Resultado de la herramienta
        
        Raises:
            MCPToolError: Si la herramienta falla
        
        Example:
            ```python
            result = await client.call_tool(
                "calculate_sum",
                {"a": 10, "b": 20},
                use_cache=False
            )
            ```
        """
        pass
```

---

# PARTE 8: TROUBLESHOOTING Y DEBUGGING

---

## Problemas Comunes

### 1. Error de Conexión

```python
# Error
MCPConnectionError: Cannot connect to server

# Solución: Verificar que el servidor está ejecutándose
async def debug_connection():
    try:
        async with Client(transport) as client:
            print("Conexión exitosa")
    except MCPConnectionError as e:
        print(f"Error de conexión: {e}")
        print("Verificar:")
        print("1. El servidor MCP está ejecutándose")
        print("2. La ruta al servidor es correcta")
        print("3. Las dependencias están instaladas")
```

---

### 2. Timeout

```python
# Error
asyncio.TimeoutError: Operation timed out

# Solución: Aumentar timeout
async def call_with_timeout(client, tool, args, timeout=60):
    try:
        result = await asyncio.wait_for(
            client.call_tool(tool, args),
            timeout=timeout
        )
        return result
    except asyncio.TimeoutError:
        print(f"Timeout después de {timeout}s")
        raise
```

---

### 3. Error de Validación

```python
# Error
ValidationError: Invalid arguments for tool 'xxx'

# Solución: Verificar schema
async def debug_tool_schema(client, tool_name):
    tools = await client.list_tools()
    tool = next((t for t in tools if t.name == tool_name), None)
    
    if tool:
        print(f"Herramienta: {tool.name}")
        print(f"Descripción: {tool.description}")
        print(f"Schema: {json.dumps(tool.inputSchema, indent=2)}")
    else:
        print(f"Herramienta '{tool_name}' no encontrada")
```

---

### 4. Memory Leak

```python
# Problema: Conexiones no cerradas

# ❌ Mal
async def bad_pattern():
    for _ in range(1000):
        client = Client(transport)
        await client.connect()
        # ... usar cliente
        # ¡Falta disconnect!

# ✅ Bien
async def good_pattern():
    async with Client(transport) as client:
        for _ in range(1000):
            result = await client.call_tool("tool", args)
```

---

## Herramientas de Debug

### MCP Inspector

```bash
# Ejecutar servidor con Inspector
npx @modelcontextprotocol/inspector python server.py

# O con FastMCP
fastmcp run server.py:mcp --transport sse
# Y abrir http://localhost:8080
```

---

### Logging Detallado

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Logger específico para MCP
mcp_logger = logging.getLogger("fastmcp")
mcp_logger.setLevel(logging.DEBUG)

# Añadir handler para archivo
handler = logging.FileHandler("mcp_debug.log")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
mcp_logger.addHandler(handler)
```

---

# PARTE 9: RECURSOS Y REFERENCIAS

---

## Documentación Oficial

| Recurso | URL |
|---------|-----|
| FastMCP Docs | https://gofastmcp.com |
| MCP Specification | https://modelcontextprotocol.io |
| MCP Python SDK | https://github.com/modelcontextprotocol/python-sdk |
| CrewAI Docs | https://docs.crewai.com |

---

## Repositorios de Ejemplo

```bash
# Clonar ejemplos
git clone https://github.com/modelcontextprotocol/servers
git clone https://github.com/modelcontextprotocol/python-sdk

# Ejemplos de FastMCP
pip install fastmcp[examples]
```

---

## Checklist de Producción

- [ ] Manejo de errores completo
- [ ] Logging configurado
- [ ] Métricas implementadas
- [ ] Timeout configurado
- [ ] Reintentos implementados
- [ ] Cache según necesidad
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Documentación actualizada
- [ ] CI/CD configurado
- [ ] Monitorización en producción

---

## Próximos Pasos

1. **Profundizar en FastMCP**: Revisar documentación avanzada
2. **Practicar con ejemplos**: Crear servidores MCP propios
3. **Integrar con agentes**: Explorar más frameworks de agentes
4. **Desplegar en producción**: Configurar entorno real
5. **Contribuir**: Open source en MCP ecosystem

---

# FIN DE LA PRESENTACIÓN

---

## Resumen

- MCP es el estándar para conectar LLMs con herramientas
- FastMCP simplifica el desarrollo de servidores y clientes
- Los clientes MCP pueden integrarse con frameworks de agentes
- CrewAI permite crear equipos de agentes colaborativos
- Las buenas prácticas son esenciales para producción
- El debugging y testing son fundamentales

---

## ¿Preguntas?

**Contacto:**
- Documentación: https://gofastmcp.com
- MCP Spec: https://modelcontextprotocol.io
- CrewAI: https://docs.crewai.com

---

**¡Gracias!** 🚀