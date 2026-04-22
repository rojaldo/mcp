# Diseño de Servicios MCP: Buenas Prácticas

## Presentación Extensa para Desarrolladores - Python + FastMCP

---

# Portada

## Diseño de Servicios MCP

### Buenas Prácticas y Patrones de Arquitectura

---

**Implementación en Python con FastMCP**

**Duración estimada: 2-3 horas**

*De los fundamentos a la implementación profesional*

---

# Agenda

## Contenido del curso

---

1. **Fundamentos** (20 min) - ¿Qué hace un buen servicio MCP?

2. **Arquitectura** (25 min) - Patrones y estructura

3. **Diseño de Tools** (30 min) - La primitiva más importante

4. **Diseño de Resources** (20 min) - Contexto estructurado

5. **Diseño de Prompts** (15 min) - Plantillas efectivas

6. **Manejo de Errores** (20 min) - Robustez ante fallos

7. **Seguridad** (25 min) - Límites de confianza

8. **Rendimiento** (20 min) - Optimización

9. **Testing** (15 min) - Calidad garantizada

10. **Casos de Estudio** (20 min) - Lecciones aprendidas

---

# PARTE 1: FUNDAMENTOS

---

# ¿Qué es un servicio MCP?

## Definición

---

Un **servicio MCP** es un programa que implementa el protocolo Model Context Protocol para exponer herramientas, recursos y prompts a clientes de IA de forma estandarizada.

---

**Componentes:**

- Servidor que implementa el protocolo MCP
- Conjunto de tools, resources y prompts
- Transporte (STDIO, HTTP, WebSocket)
- Manejo del ciclo de vida de conexiones

---

# ¿Por qué importa el diseño?

## La calidad del servicio define la experiencia

---

**Un mal servicio MCP:**

- Descripciones vagas que confunden a la IA
- Errores sin contexto que interrumpen conversaciones
- Tools que fallan silenciosamente
- Recursos que cambian sin aviso
- Prompts que no se adaptan al contexto

---

**Un buen servicio MCP:**

- Descripciones precisas que guían al modelo
- Errores estructurados que permiten recuperación
- Tools robustas con validación completa
- Recursos estables con versionado
- Prompts que se adaptan al usuario

---

# Principios Fundamentales

## Los 5 pilares del diseño MCP

---

### 1. Claridad

Las descripciones deben ser comprensibles para humanos y modelos.

---

### 2. Consistencia

Todas las tools siguen los mismos patrones de diseño.

---

### 3. Robustez

El servicio maneja errores de forma controlada.

---

### 4. Seguridad

El servicio respeta los límites de confianza.

---

### 5. Eficiencia

El servicio minimiza tokens y latencia.

---

# Claridad en las Descripciones

## El arte de comunicar a la IA

---

**Principio:**

La IA no ve tu código. Solo ve el esquema JSON.

---

**Mala descripción:**

```python
@mcp.tool
def process(data: str) -> str:
    """Process the input."""
    return "done"
```

*¿Qué hace? ¿Qué devuelve? ¿Cuándo usarla?*

---

**Buena descripción:**

```python
@mcp.tool
def process_payment(
    card_number: str,
    amount: float
) -> dict:
    """Procesa un pago con tarjeta.
    
    Recibe los datos de la tarjeta y el importe.
    Devuelve el resultado de la transacción con 
    ID de confirmación o mensaje de error.
    """
    return {"success": True, "transaction_id": "tx_123"}
```

---

# Claridad - Patrón de Descripción

## Estructura recomendada

---

**Fórmula:**

```
[VERBO] [OBJETO]. [DETALLE DE ENTRADA]. [DETALLE DE SALIDA].
```

---

**Ejemplo completo con FastMCP:**

```python
from fastmcp import FastMCP

mcp = FastMCP("mi-servidor")

@mcp.tool
def search_users(
    query: str,
    limit: int = 20
) -> list[dict]:
    """Busca usuarios en el sistema por nombre o email.
    
    Devuelve una lista paginada de usuarios que coinciden
    con el criterio de búsqueda, ordenados por relevancia.
    
    Args:
        query: Texto a buscar (nombre o email)
        limit: Número máximo de resultados (1-100)
    
    Returns:
        Lista de usuarios con id, nombre y email
    """
    users = db.search_users(query, limit)
    return users
```

---

# Claridad - Parámetros Descriptivos

## Cada campo explicado

---

**Malo:**

```python
@mcp.tool
def search(q: str, n: int) -> list:
    """Search."""
    return []
```

---

**Bueno:**

```python
from typing import Annotated
from pydantic import Field

@mcp.tool
def search_users(
    query: Annotated[str, Field(
        description="Texto a buscar. Puede ser nombre completo, "
                    "email parcial o nombre de usuario.",
        min_length=1,
        max_length=200
    )],
    limit: Annotated[int, Field(
        description="Número máximo de resultados a devolver (1-100).",
        ge=1,
        le=100
    )] = 20
) -> list[dict]:
    """Busca usuarios en el sistema por nombre o email."""
    return db.search_users(query, limit)
```

---

# Claridad - Ejemplos en Descripción

## Cuando el esquema no es suficiente

---

**Añadir ejemplos para casos complejos:**

```python
@mcp.tool
def schedule_task(
    time: str,
    task: str
) -> dict:
    """Programa una tarea para ejecutarse en el futuro.
    
    El tiempo puede ser absoluto (ISO 8601) o relativo.
    
    Ejemplos de tiempo:
    - Absoluto: '2026-04-18T15:00:00Z'
    - Relativo: '30m', '2h', '1d'
    
    Args:
        time: Tiempo de ejecución
        task: Descripción de la tarea
    """
    scheduled_time = parse_time(time)
    return schedule(scheduled_time, task)
```

---

**Regla:**

Si el formato es complejo, incluye ejemplos en la descripción.

---

# Consistencia entre Tools

## El principio de familiaridad

---

**Una vez que el modelo aprende un patrón, espera que las otras tools lo sigan.**

---

**Inconsistente:**

```python
# Tool 1
@mcp.tool
def get_user(userId: str) -> dict: ...

# Tool 2
@mcp.tool
def delete_user(id: str) -> dict: ...

# Tool 3
@mcp.tool
def update_user(user_id: str) -> dict: ...
```

*¿userId, id o user_id?*

---

# Consistencia - Patrón de Nombres

## Nomenclatura estándar

---

**Convenciones recomendadas:**

| Acción | Patrón | Ejemplo |
|--------|--------|---------|
| Leer uno | `get_<entidad>` | `get_user`, `get_order` |
| Leer varios | `list_<entidad>s` | `list_users`, `list_orders` |
| Crear | `create_<entidad>` | `create_user`, `create_order` |
| Actualizar | `update_<entidad>` | `update_user`, `update_order` |
| Eliminar | `delete_<entidad>` | `delete_user`, `delete_order` |
| Buscar | `search_<entidad>s` | `search_users`, `search_orders` |

---

**Para parámetros:**

| Uso | Patrón | Ejemplo |
|-----|--------|---------|
| ID único | `<entidad>_id` | `user_id`, `order_id` |
| Límite | `limit` | `limit` |
| Desplazamiento | `offset` | `offset` |
| Filtros | `<campo>_filter` | `status_filter` |

---

# Consistencia - Estructura de Respuesta

## Respuestas predecibles

---

**Estructura estándar:**

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')

@dataclass
class MCPResponse(Generic[T]):
    success: bool
    data: T | None = None
    error: dict | None = None
    metadata: dict | None = None

# Uso
@mcp.tool
def get_user(user_id: str) -> dict:
    """Obtiene un usuario por ID."""
    user = db.get_user(user_id)
    
    if not user:
        return {
            "success": False,
            "error": {
                "code": "USER_NOT_FOUND",
                "message": f"Usuario {user_id} no encontrado"
            }
        }
    
    return {
        "success": True,
        "data": user,
        "metadata": {
            "timestamp": datetime.now().isoformat()
        }
    }
```

---

# Consistencia - Paginación

## Patrón estándar para listas

---

**Entrada:**

```python
@mcp.tool
def list_users(
    limit: Annotated[int, Field(ge=1, le=100)] = 20,
    offset: Annotated[int, Field(ge=0)] = 0,
    cursor: Annotated[str | None, Field(
        description="Token de paginación del resultado anterior"
    )] = None
) -> dict:
    """Lista usuarios con paginación."""
    # ...
```

---

**Salida:**

```python
return {
    "success": True,
    "data": {
        "items": users,
        "total": 150,
        "has_more": True,
        "next_cursor": "eyJvZmZzZXQiOjIwfQ=="
    }
}
```

---

# Robustez ante Fallos

## El servicio debe ser resiliente

---

**Principio:**

Un error en una tool no debe interrumpir la sesión del usuario.

---

**Estrategias:**

1. Validar la entrada antes de procesar
2. Capturar todas las excepciones
3. Devolver errores estructurados
4. Incluir sugerencias de recuperación
5. Registrar para depuración

---

# Robustez - Validación de Entrada

## Primera línea de defensa

---

**Validar antes de procesar:**

```python
import re
from typing import Annotated
from pydantic import Field, validate_call

@mcp.tool
def get_user(
    user_id: Annotated[str, Field(
        pattern=r"^usr_[a-zA-Z0-9]+$",
        description="ID del usuario (formato: usr_xxx)"
    )]
) -> dict:
    """Obtiene un usuario por su ID."""
    # La validación la hace Pydantic automáticamente
    
    user = db.get_user(user_id)
    
    if not user:
        return {
            "success": False,
            "error": {
                "code": "USER_NOT_FOUND",
                "message": f"Usuario {user_id} no encontrado"
            }
        }
    
    return {"success": True, "data": user}
```

---

# Robustez - Validación Manual

## Cuando Pydantic no es suficiente

---

```python
from pydantic import BaseModel, field_validator
import re

class UserInput(BaseModel):
    user_id: str
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        if not v:
            raise ValueError('user_id es obligatorio')
        if not re.match(r'^usr_[a-zA-Z0-9]+$', v):
            raise ValueError(
                'user_id debe tener formato usr_xxx'
            )
        return v

@mcp.tool
def get_user(user_id: str) -> dict:
    """Obtiene un usuario por ID."""
    try:
        # Validar con Pydantic
        validated = UserInput(user_id=user_id)
    except ValueError as e:
        return {
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(e),
                "field": "user_id"
            }
        }
    
    # Procesar...
```

---

# Robustez - Manejo de Excepciones

## Nunca lanzar sin capturar

---

**Incorrecto:**

```python
@mcp.tool
def get_user(user_id: str) -> dict:
    user = db.get_user(user_id)  # Puede lanzar excepción
    return {"success": True, "data": user}
```

---

**Correcto:**

```python
import logging
import uuid

logger = logging.getLogger(__name__)

@mcp.tool
def get_user(user_id: str) -> dict:
    """Obtiene un usuario por ID."""
    request_id = str(uuid.uuid4())[:8]
    
    try:
        user = db.get_user(user_id)
        
        if not user:
            return {
                "success": False,
                "error": {
                    "code": "USER_NOT_FOUND",
                    "message": f"Usuario {user_id} no encontrado",
                    "request_id": request_id
                }
            }
        
        return {"success": True, "data": user}
        
    except DatabaseError as e:
        logger.error(
            "Database error",
            extra={
                "request_id": request_id,
                "error": str(e),
                "user_id": user_id
            }
        )
        
        return {
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Error interno. Inténtelo más tarde.",
                "request_id": request_id
            }
        }
```

---

# Robustez - Errores con Sugerencias

## Ayudar al modelo a recuperarse

---

**Error sin sugerencia:**

```python
return {
    "success": False,
    "error": {
        "code": "INSUFFICIENT_STOCK",
        "message": "No hay suficiente stock"
    }
}
```

---

**Error con sugerencia:**

```python
@mcp.tool
def add_to_cart(
    product_id: str,
    quantity: int
) -> dict:
    """Añade un producto al carrito."""
    stock = get_stock(product_id)
    
    if stock < quantity:
        return {
            "success": False,
            "error": {
                "code": "INSUFFICIENT_STOCK",
                "message": "No hay suficiente stock del producto",
                "details": {
                    "requested": quantity,
                    "available": stock,
                    "suggestion": (
                        f"Puede añadir {stock} unidades ahora "
                        "o esperar reposición"
                    )
                }
            }
        }
    
    # Procesar...
```

---

**El modelo puede usar la sugerencia para proponer alternativas.**

---

# PARTE 2: ARQUITECTURA

---

# Arquitectura de un Servidor MCP con FastMCP

## Componentes principales

---

```python
# server.py - Estructura completa
from fastmcp import FastMCP

# Crear servidor
mcp = FastMCP(
    "mi-servidor",
    version="1.0.0",
    description="Servidor MCP para gestión de usuarios"
)

# Registrar tools
from tools import users, orders, products

# Tools se registran automáticamente al importar
# o usar mcp.add_tool() explícitamente

# Configurar logging
import logging
logging.basicConfig(level=logging.INFO)

# Ejecutar servidor
if __name__ == "__main__":
    mcp.run()
```

---

# Arquitectura Modular

## Organización de archivos

---

```
mi_servidor_mcp/
├── server.py           # Punto de entrada
├── tools/
│   ├── __init__.py
│   ├── users.py        # Tools de usuarios
│   ├── orders.py       # Tools de pedidos
│   └── products.py     # Tools de productos
├── resources/
│   ├── __init__.py
│   ├── configs.py      # Resources de configuración
│   └── docs.py         # Resources de documentación
├── prompts/
│   ├── __init__.py
│   └── templates.py    # Prompts predefinidos
├── models/
│   ├── __init__.py
│   ├── user.py         # Modelos Pydantic
│   └── order.py
├── validators/
│   ├── __init__.py
│   └── common.py       # Validadores reutilizables
├── errors/
│   ├── __init__.py
│   └── handlers.py      # Manejo de errores
└── utils/
    ├── __init__.py
    ├── cache.py        # Sistema de caché
    └── logging.py      # Utilidades de logging
```

---

# Tools Modulares

## Separar por dominio

---

```python
# tools/users.py
from fastmcp import FastMCP
from models.user import User, UserCreate, UserUpdate
from errors.handlers import MCPError, to_response

# Crear sub-aplicación o importar mcp principal
mcp = FastMCP.get_instance()  # O pasar como parámetro

@mcp.tool
def get_user(user_id: str) -> dict:
    """Obtiene un usuario por ID."""
    try:
        user = db.get_user(user_id)
        if not user:
            raise MCPError("NOT_FOUND", f"Usuario {user_id} no encontrado")
        return {"success": True, "data": user}
    except MCPError as e:
        return to_response(e)

@mcp.tool
def create_user(user: UserCreate) -> dict:
    """Crea un nuevo usuario."""
    # ...
    
@mcp.tool
def update_user(user_id: str, updates: UserUpdate) -> dict:
    """Actualiza un usuario existente."""
    # ...

@mcp.tool
def delete_user(user_id: str) -> dict:
    """Elimina un usuario."""
    # ...

@mcp.tool
def list_users(limit: int = 20, offset: int = 0) -> dict:
    """Lista usuarios con paginación."""
    # ...
```

---

# Patrón de Validación Centralizada

## Validadores reutilizables

---

```python
# validators/common.py
from typing import Any
import re

def validate_required(field: str, value: Any) -> tuple[bool, str | None]:
    """Valida que un campo no esté vacío."""
    if not value:
        return False, f"{field} es obligatorio"
    return True, None

def validate_pattern(
    field: str, 
    value: str, 
    pattern: str, 
    message: str
) -> tuple[bool, str | None]:
    """Valida que un campo coincida con un patrón."""
    if not re.match(pattern, value):
        return False, message
    return True, None

def validate_range(
    field: str,
    value: int | float,
    min_val: int | float,
    max_val: int | float
) -> tuple[bool, str | None]:
    """Valida que un valor esté en un rango."""
    if value < min_val or value > max_val:
        return False, f"{field} debe estar entre {min_val} y {max_val}"
    return True, None

def validate_email(field: str, value: str) -> tuple[bool, str | None]:
    """Valida formato de email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, value):
        return False, f"{field} no tiene formato de email válido"
    return True, None
```

---

# Uso de Validadores

---

```python
from validators.common import (
    validate_required,
    validate_pattern,
    validate_range
)

@mcp.tool
def search_users(
    query: str,
    limit: int = 20
) -> dict:
    """Busca usuarios con validación manual."""
    
    errors = []
    
    # Validar requerido
    valid, error = validate_required("query", query)
    if not valid:
        errors.append({"field": "query", "message": error})
    
    # Validar patrón
    valid, error = validate_pattern(
        "query", query,
        r'^[a-zA-Z0-9\s]+$',
        "query solo puede contener letras, números y espacios"
    )
    if not valid:
        errors.append({"field": "query", "message": error})
    
    # Validar rango
    valid, error = validate_range("limit", limit, 1, 100)
    if not valid:
        errors.append({"field": "limit", "message": error})
    
    if errors:
        return {
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Errores de validación",
                "details": errors
            }
        }
    
    # Procesar...
```

---

# Patrón de Error Handler

## Clases de error centralizadas

---

```python
# errors/handlers.py
from dataclasses import dataclass
from typing import Any
import uuid

@dataclass
class MCPError(Exception):
    """Error estructurado para MCP."""
    code: str
    message: str
    details: dict[str, Any] | None = None
    request_id: str | None = None
    
    def __post_init__(self):
        if self.request_id is None:
            self.request_id = str(uuid.uuid4())[:8]

class Errors:
    """Factory de errores comunes."""
    
    @staticmethod
    def not_found(resource: str, identifier: str) -> MCPError:
        return MCPError(
            "NOT_FOUND",
            f"{resource} no encontrado",
            {"resource": resource, "identifier": identifier}
        )
    
    @staticmethod
    def invalid_input(field: str, reason: str) -> MCPError:
        return MCPError(
            "INVALID_INPUT",
            f"Campo {field} inválido: {reason}",
            {"field": field, "reason": reason}
        )
    
    @staticmethod
    def unauthorized(action: str) -> MCPError:
        return MCPError(
            "UNAUTHORIZED",
            f"No autorizado para {action}",
            {"action": action}
        )
    
    @staticmethod
    def forbidden(
        permission: str,
        suggestion: str | None = None
    ) -> MCPError:
        return MCPError(
            "FORBIDDEN",
            "No tiene permisos para esta operación",
            {
                "required_permission": permission,
                "suggestion": suggestion
            }
        )
    
    @staticmethod
    def internal(message: str = "Error interno") -> MCPError:
        return MCPError("INTERNAL_ERROR", message)

def to_response(error: MCPError) -> dict:
    """Convierte un MCPError a respuesta JSON."""
    return {
        "success": False,
        "error": {
            "code": error.code,
            "message": error.message,
            "details": error.details,
            "request_id": error.request_id
        }
    }
```

---

# Uso del Error Handler

---

```python
from errors.handlers import Errors, MCPError, to_response
import logging

logger = logging.getLogger(__name__)

@mcp.tool
def delete_user(user_id: str, context: dict | None = None) -> dict:
    """Elimina un usuario del sistema."""
    request_id = str(uuid.uuid4())[:8]
    
    try:
        # Validar
        if not user_id:
            raise Errors.invalid_input("user_id", "es obligatorio")
        
        # Verificar permisos
        if context and not context.get("user", {}).get("is_admin"):
            raise Errors.forbidden(
                "users:delete",
                "Contacte al administrador"
            )
        
        # Buscar usuario
        user = db.get_user(user_id)
        if not user:
            raise Errors.not_found("Usuario", user_id)
        
        # Eliminar
        db.delete_user(user_id)
        
        return {"success": True, "data": {"deleted": True}}
        
    except MCPError as e:
        logger.error(f"MCP Error: {e.code}", extra={"request_id": request_id})
        return to_response(e)
        
    except Exception as e:
        logger.exception("Unexpected error", extra={"request_id": request_id})
        return to_response(Errors.internal())
```

---

# Patrón de Caché

## Sistema de caché simple

---

```python
# utils/cache.py
from typing import Any
from datetime import datetime, timedelta
import threading

class SimpleCache:
    """Caché en memoria con TTL."""
    
    def __init__(self, default_ttl_seconds: int = 60):
        self._cache: dict[str, tuple[Any, datetime]] = {}
        self._lock = threading.Lock()
        self._default_ttl = timedelta(seconds=default_ttl_seconds)
    
    def get(self, key: str) -> Any | None:
        """Obtiene un valor del caché."""
        with self._lock:
            entry = self._cache.get(key)
            if not entry:
                return None
            
            value, expires_at = entry
            if datetime.now() > expires_at:
                del self._cache[key]
                return None
            
            return value
    
    def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:
        """Guarda un valor en el caché."""
        ttl = timedelta(seconds=ttl_seconds) if ttl_seconds else self._default_ttl
        
        with self._lock:
            self._cache[key] = (value, datetime.now() + ttl)
    
    def delete(self, key: str) -> None:
        """Elimina una entrada del caché."""
        with self._lock:
            self._cache.pop(key, None)
    
    def invalidate_pattern(self, pattern: str) -> None:
        """Invalida todas las claves que contengan el patrón."""
        with self._lock:
            keys_to_delete = [
                k for k in self._cache.keys() 
                if pattern in k
            ]
            for key in keys_to_delete:
                del self._cache[key]

# Instancia global
cache = SimpleCache(default_ttl_seconds=300)  # 5 minutos
```

---

# Uso del Caché

---

```python
from utils.cache import cache

@mcp.tool
def get_user(
    user_id: str,
    use_cache: bool = True
) -> dict:
    """Obtiene un usuario con caché opcional."""
    
    # Intentar caché
    if use_cache:
        cache_key = f"user:{user_id}"
        cached = cache.get(cache_key)
        if cached:
            return {
                "success": True,
                "data": cached,
                "from_cache": True
            }
    
    # Buscar en DB
    user = db.get_user(user_id)
    
    if not user:
        return {
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": f"Usuario {user_id} no encontrado"
            }
        }
    
    # Guardar en caché
    if use_cache:
        cache.set(cache_key, user, ttl_seconds=60)
    
    return {
        "success": True,
        "data": user,
        "from_cache": False
    }

# Invalidar cuando cambia
@mcp.tool
def update_user(user_id: str, updates: dict) -> dict:
    """Actualiza un usuario."""
    result = db.update_user(user_id, updates)
    
    # Invalidar caché
    cache.invalidate_pattern(f"user:{user_id}")
    
    return {"success": True, "data": result}
```

---

# Patrón de Rate Limiting

## Proteger el servicio

---

```python
# utils/rate_limit.py
from typing import Dict
from datetime import datetime, timedelta
import threading

class RateLimiter:
    """Rate limiter por ventana deslizante."""
    
    def __init__(
        self,
        max_requests: int = 100,
        window_seconds: int = 60
    ):
        self._limits: Dict[str, tuple[int, datetime]] = {}
        self._lock = threading.Lock()
        self._max = max_requests
        self._window = timedelta(seconds=window_seconds)
    
    def check(self, identifier: str) -> dict:
        """Verifica si una petición está permitida."""
        now = datetime.now()
        
        with self._lock:
            entry = self._limits.get(identifier)
            
            if not entry:
                self._limits[identifier] = (1, now + self._window)
                return {
                    "allowed": True,
                    "remaining": self._max - 1,
                    "reset_at": now + self._window
                }
            
            count, reset_at = entry
            
            # Ventana expirada - reiniciar
            if now > reset_at:
                self._limits[identifier] = (1, now + self._window)
                return {
                    "allowed": True,
                    "remaining": self._max - 1,
                    "reset_at": now + self._window
                }
            
            # Límite excedido
            if count >= self._max:
                return {
                    "allowed": False,
                    "remaining": 0,
                    "reset_at": reset_at
                }
            
            # Incrementar contador
            self._limits[identifier] = (count + 1, reset_at)
            return {
                "allowed": True,
                "remaining": self._max - count - 1,
                "reset_at": reset_at
            }

# Instancia global
limiter = RateLimiter(max_requests=50, window_seconds=60)
```

---

# Uso del Rate Limiter

---

```python
from utils.rate_limit import limiter

@mcp.tool
def search_users(
    query: str,
    limit: int = 20,
    context: dict | None = None
) -> dict:
    """Busca usuarios con rate limiting."""
    
    # Obtener identificador
    identifier = (
        context.get("user", {}).get("id", "anonymous")
        if context else "anonymous"
    )
    
    # Verificar rate limit
    rate = limiter.check(identifier)
    
    if not rate["allowed"]:
        retry_after = int((rate["reset_at"] - datetime.now()).total_seconds())
        
        return {
            "success": False,
            "error": {
                "code": "RATE_LIMIT_EXCEEDED",
                "message": "Demasiadas peticiones. Inténtelo más tarde.",
                "retry_after": retry_after
            }
        }
    
    # Procesar normalmente
    users = db.search_users(query, limit)
    
    return {
        "success": True,
        "data": users,
        "rate_limit": {
            "remaining": rate["remaining"]
        }
    }
```

---

# PARTE 3: DISEÑO DE TOOLS

---

# Anatomía de una Tool en FastMCP

## Estructura completa

---

```python
from fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

mcp = FastMCP("mi-servidor")

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def get_user(
    user_id: Annotated[str, Field(
        description="ID único del usuario (formato: usr_xxx)",
        pattern=r"^usr_[a-zA-Z0-9]+$"
    )],
    fields: Annotated[list[str] | None, Field(
        description="Campos a devolver",
        examples=[["id", "name", "email"]]
    )] = None
) -> dict:
    """
    Obtiene un usuario por su ID.
    
    Busca un usuario en el sistema y devuelve sus datos.
    Si el usuario no existe, devuelve error NOT_FOUND.
    
    Args:
        user_id: ID del usuario a buscar
        fields: Lista de campos a incluir (opcional)
    
    Returns:
        Diccionario con success, data y metadata
    """
    user = db.get_user(user_id)
    
    if not user:
        return {
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": f"Usuario {user_id} no encontrado"
            }
        }
    
    return {"success": True, "data": user}
```

---

# Convenciones de Nombres

## Nombres descriptivos y consistentes

---

### Verbos de Acción

| Verbo | Significado | Ejemplo FastMCP |
|-------|-------------|-----------------|
| `get` | Obtener un recurso por ID | `get_user` |
| `list` | Obtener múltiples recursos | `list_users` |
| `search` | Búsqueda por criterios | `search_users` |
| `create` | Crear nuevo recurso | `create_user` |
| `update` | Modificar existente | `update_user` |
| `delete` | Eliminar recurso | `delete_user` |

---

### Evitar

| Malo | Por qué | Mejor |
|------|---------|-------|
| `process` | Vago | `process_payment` |
| `handle` | Vago | `handle_webhook` |
| `do` | Sin significado | `execute_task` |
| `run` | Ambiguo | `run_report` |
| `manage` | Demasiado amplio | `create_user`, `update_user` |

---

# Descripción Efectiva

## La descripción es tu API

---

**Fórmula de descripción completa:**

```
[VERBO] [RECURSO]. [QUÉ HACE]. [PARÁMETROS CLAVE]. [RETORNO]. [EFECTOS].
```

---

**Ejemplo completo:**

```python
@mcp.tool(
    annotations={"destructiveHint": True}
)
def delete_user(user_id: str) -> dict:
    """
    Elimina un usuario del sistema permanentemente.
    
    Requiere el ID del usuario. Devuelve confirmación
    de eliminación o error si el usuario no existe.
    
    Esta acción es irreversible y no se puede deshacer.
    
    Args:
        user_id: ID del usuario a eliminar
    
    Returns:
        Diccionario con success y confirmación
    """
    # Implementación
```

---

# Tipos de Datos con Annotated

## Validación automática con Pydantic

---

```python
from typing import Annotated, Literal
from pydantic import Field
from datetime import datetime

# String con restricciones
Username = Annotated[str, Field(
    min_length=1,
    max_length=100,
    pattern=r"^[a-zA-Z0-9_]+$",
    description="Nombre de usuario (solo alfanumérico y _)"
)]

# Entero con rango
Limit = Annotated[int, Field(
    ge=1,
    le=100,
    description="Número de resultados (1-100)"
)]

# Enum
Status = Literal["pending", "active", "completed", "cancelled"]

# Email
Email = Annotated[str, Field(
    pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    description="Email válido"
)]

# Uso
@mcp.tool
def create_user(
    username: Username,
    email: Email,
    status: Status = "pending"
) -> dict:
    """Crea un nuevo usuario."""
    # La validación es automática
```

---

# Objetos Anidados con Pydantic

---

```python
from pydantic import BaseModel
from typing import Literal

class Address(BaseModel):
    """Dirección del usuario."""
    street: str
    city: str
    postal_code: str
    country: str

class UserCreate(BaseModel):
    """Datos para crear un usuario."""
    name: Annotated[str, Field(min_length=2, max_length=100)]
    email: Email
    role: Literal["admin", "user", "guest"] = "user"
    address: Address | None = None

@mcp.tool
def create_user(user: UserCreate) -> dict:
    """Crea un nuevo usuario con datos anidados."""
    # user ya está validado por Pydantic
    new_user = db.create_user(user.model_dump())
    return {"success": True, "data": new_user}

# El schema JSON se genera automáticamente
```

---

# Arrays y Listas

---

```python
from typing import Annotated
from pydantic import Field

@mcp.tool
def bulk_delete_users(
    user_ids: Annotated[list[str], Field(
        min_length=1,
        max_length=50,
        description="Lista de IDs de usuarios a eliminar (1-50)"
    )]
) -> dict:
    """Elimina múltiples usuarios en una operación."""
    deleted = []
    failed = []
    
    for user_id in user_ids:
        try:
            db.delete_user(user_id)
            deleted.append(user_id)
        except Exception:
            failed.append(user_id)
    
    return {
        "success": True,
        "data": {
            "deleted": deleted,
            "failed": failed,
            "total_deleted": len(deleted)
        }
    }

@mcp.tool
def update_user_roles(
    user_id: str,
    roles: Annotated[list[Literal["admin", "user", "guest"]], Field(
        description="Lista de roles a asignar"
    )]
) -> dict:
    """Actualiza los roles de un usuario."""
    # ...
```

---

# Annotations en FastMCP

## Metadatos importantes

---

### readOnlyHint

```python
@mcp.tool(annotations={"readOnlyHint": True})
def get_user(user_id: str) -> dict:
    """Tool de solo lectura - no modifica datos."""
```

**Uso:** Los clientes pueden ejecutar sin confirmación.

---

### destructiveHint

```python
@mcp.tool(annotations={"destructiveHint": True})
def delete_user(user_id: str) -> dict:
    """Tool destructiva - efectos irreversibles."""
```

**Uso:** Los clientes deben mostrar confirmación explícita.

---

### idempotentHint

```python
@mcp.tool(annotations={"idempotentHint": True})
def set_user_status(
    user_id: str,
    status: str
) -> dict:
    """Tool idempotente - mismo resultado si se repite."""
```

**Uso:** Los clientes pueden reintentar automáticamente.

---

### openWorldHint

```python
@mcp.tool(annotations={"openWorldHint": True})
def send_email(
    to: str,
    subject: str,
    body: str
) -> dict:
    """Tool que interactúa con sistemas externos."""
```

**Uso:** Considerar implicaciones de privacidad.

---

# Idempotencia

## Diseñar para reintentos

---

**Principio:**

Una operación es idempotente si ejecutarla múltiples veces tiene el mismo efecto que ejecutarla una vez.

---

```python
import uuid

@mcp.tool(annotations={"idempotentHint": True})
def create_order(
    idempotency_key: Annotated[str, Field(
        description="Clave única para evitar duplicados. Use UUID."
    )],
    items: list[dict]
) -> dict:
    """Crea un pedido de forma idempotente."""
    
    # Verificar si ya existe
    existing = db.get_order_by_key(idempotency_key)
    if existing:
        return {
            "success": True,
            "data": existing,
            "idempotent": True,
            "message": "Pedido ya existente"
        }
    
    # Crear nuevo
    order = db.create_order(
        idempotency_key=idempotency_key,
        items=items,
        created_at=datetime.now()
    )
    
    return {
        "success": True,
        "data": order,
        "idempotent": False
    }
```

---

# Paginación

## Manejar grandes conjuntos de datos

---

### Paginación por Desplazamiento

```python
@mcp.tool(annotations={"readOnlyHint": True})
def list_users(
    limit: Annotated[int, Field(ge=1, le=100)] = 20,
    offset: Annotated[int, Field(ge=0)] = 0
) -> dict:
    """Lista usuarios con paginación por desplazamiento."""
    users = db.get_users(limit=limit, offset=offset)
    total = db.count_users()
    
    return {
        "success": True,
        "data": {
            "items": users,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total
        }
    }
```

---

### Paginación por Cursor

```python
import base64
import json

@mcp.tool(annotations={"readOnlyHint": True})
def list_users_cursor(
    limit: Annotated[int, Field(ge=1, le=100)] = 20,
    cursor: Annotated[str | None, Field(
        description="Token de la página anterior"
    )] = None
) -> dict:
    """Lista usuarios con paginación por cursor."""
    
    # Decodificar cursor
    if cursor:
        decoded = json.loads(base64.b64decode(cursor).decode())
        last_id = decoded.get("last_id")
    else:
        last_id = None
    
    # Obtener usuarios
    users = db.get_users_after(last_id, limit)
    
    # Generar siguiente cursor
    next_cursor = None
    if len(users) == limit:
        next_cursor = base64.b64encode(
            json.dumps({"last_id": users[-1]["id"]}).encode()
        ).decode()
    
    return {
        "success": True,
        "data": {
            "items": users,
            "next_cursor": next_cursor,
            "has_more": next_cursor is not None
        }
    }
```

---

# Filtrado y Búsqueda

## Encontrar lo que se necesita

---

```python
from datetime import datetime
from typing import Literal

@mcp.tool(annotations={"readOnlyHint": True})
def search_orders(
    query: Annotated[str | None, Field(
        description="Texto a buscar"
    )] = None,
    status: Annotated[list[Literal[
        "pending", "processing", "shipped", "delivered", "cancelled"
    ]] | None, Field(
        description="Filtrar por estados (puede ser múltiple)"
    )] = None,
    date_from: Annotated[str | None, Field(
        description="Fecha mínima (ISO 8601)"
    )] = None,
    date_to: Annotated[str | None, Field(
        description="Fecha máxima (ISO 8601)"
    )] = None,
    min_amount: Annotated[float | None, Field(ge=0)] = None,
    max_amount: Annotated[float | None, Field(ge=0)] = None,
    sort_by: Literal["date", "amount", "status"] = "date",
    sort_order: Literal["asc", "desc"] = "desc",
    limit: int = 20,
    offset: int = 0
) -> dict:
    """Busca pedidos con filtros avanzados."""
    
    # Validar rangos
    if min_amount and max_amount and min_amount > max_amount:
        return {
            "success": False,
            "error": {
                "code": "INVALID_RANGE",
                "message": "min_amount no puede ser mayor que max_amount"
            }
        }
    
    if date_from and date_to:
        if datetime.fromisoformat(date_from) > datetime.fromisoformat(date_to):
            return {
                "success": False,
                "error": {
                    "code": "INVALID_RANGE",
                    "message": "date_from no puede ser posterior a date_to"
                }
            }
    
    # Construir filtros
    filters = {}
    if status:
        filters["status"] = {"$in": status}
    if min_amount:
        filters["amount"] = {"$gte": min_amount}
    if max_amount:
        filters["amount"] = {**filters.get("amount", {}), "$lte": max_amount}
    
    # Buscar
    orders = db.search_orders(
        filters=filters,
        query=query,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset
    )
    
    return {"success": True, "data": orders}
```

---

# PARTE 4: DISEÑO DE RESOURCES

---

# ¿Qué son los Resources?

## Contexto pasivo para el modelo

---

**Definición:**

Un resource es un dato que el modelo puede leer para obtener contexto, pero no puede modificar directamente.

---

**Características:**

- Pasivos (no se ejecutan)
- Proporcionan contexto
- Se actualizan dinámicamente
- Tienen URI única

---

**Diferencia con Tools:**

| Aspecto | Tool | Resource |
|---------|------|----------|
| Acción | Se ejecuta | Se lee |
| Parámetros | Sí (inputSchema) | Sí (URI templates) |
| Modifica estado | Posible | No |
| Retorno | Resultado de acción | Contenido del recurso |

---

# Resources en FastMCP

## Definición básica

---

```python
from fastmcp import FastMCP

mcp = FastMCP("mi-servidor")

# Resource estático
@mcp.resource("config://app/settings")
def get_app_settings() -> str:
    """Configuración de la aplicación."""
    return json.dumps({
        "app_name": "Mi App",
        "version": "1.0.0",
        "features": ["chat", "search"]
    })

# Resource con parámetros (URI template)
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Perfil del usuario."""
    user = db.get_user(user_id)
    return json.dumps({
        "id": user.id,
        "name": user.name,
        "email": user.email
    })
```

---

# Tipos de Resources

## Categorización por contenido

---

### Estáticos

```python
@mcp.resource("docs://api/schema")
def get_api_schema() -> str:
    """Esquema de la API (cambia poco)."""
    return json.dumps(api_schema)

@mcp.resource("config://database/tables")
def get_db_tables() -> str:
    """Estructura de tablas de la DB."""
    return json.dumps(db.get_table_schema())
```

---

### Dinámicos

```python
@mcp.resource("system://status/live")
def get_system_status() -> str:
    """Estado actual del sistema."""
    return json.dumps({
        "cpu_usage": get_cpu_usage(),
        "memory": get_memory_usage(),
        "active_connections": get_connections(),
        "timestamp": datetime.now().isoformat()
    })
```

---

### Generados

```python
@mcp.resource("reports://{report_id}/summary")
def get_report_summary(report_id: str) -> str:
    """Resumen generado bajo demanda."""
    data = db.get_report_data(report_id)
    summary = generate_summary(data)
    return summary
```

---

# Resource URIs

## Identificación única

---

### Esquemas comunes

```python
# Archivos locales
@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """Lee un archivo."""
    with open(path, 'r') as f:
        return f.read()

# Base de datos
@mcp.resource("db://{table}/schema")
def get_table_schema(table: str) -> str:
    """Esquema de una tabla."""
    return json.dumps(db.get_schema(table))

# APIs externas
@mcp.resource("external://{service}/status")
def get_external_status(service: str) -> str:
    """Estado de un servicio externo."""
    response = requests.get(f"https://{service}/status")
    return response.text

# Memoria caché
@mcp.resource("cache://{key}")
def get_cached(key: str) -> str:
    """Valor cacheado."""
    return cache.get(key) or "null"
```

---

# URI Templates

## Parámetros en la URI

---

```python
# Un parámetro
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Perfil de usuario."""
    user = db.get_user(user_id)
    return json.dumps(user)

# Múltiples parámetros
@mcp.resource("repos://{owner}/{repo}/issues")
def get_repo_issues(owner: str, repo: str) -> str:
    """Issues de un repositorio."""
    issues = github.get_issues(owner, repo)
    return json.dumps(issues)

# Parámetros anidados
@mcp.resource("logs://{service}/{date}/{level}")
def get_logs(service: str, date: str, level: str) -> str:
    """Logs filtrados."""
    logs = get_filtered_logs(service, date, level)
    return "\n".join(logs)
```

---

# Resources con Tipos MIME

---

```python
@mcp.resource("users://{user_id}/avatar", 
              mime_type="image/png")
def get_user_avatar(user_id: str) -> bytes:
    """Avatar del usuario como imagen."""
    return db.get_user_avatar(user_id)

@mcp.resource("docs://{doc_id}/content",
              mime_type="text/markdown")
def get_doc_content(doc_id: str) -> str:
    """Contenido de documento en Markdown."""
    return db.get_document(doc_id).content

@mcp.resource("data://{dataset}/export",
              mime_type="application/csv")
def get_dataset_csv(dataset: str) -> str:
    """Dataset exportado como CSV."""
    data = db.get_dataset(dataset)
    return convert_to_csv(data)
```

---

# Resource Subscriptions

## Actualizaciones en tiempo real

---

```python
from fastmcp import FastMCP
import asyncio

mcp = FastMCP("mi-servidor")

@mcp.resource("logs://system/live")
async def get_live_logs() -> str:
    """Logs en tiempo real."""
    # Retornar últimos logs
    return "\n".join(get_recent_logs(100))

@mcp.resource("logs://system/stream")
async def stream_logs() -> AsyncIterator[str]:
    """Stream de logs en tiempo real."""
    while True:
        new_logs = await get_new_logs()
        if new_logs:
            yield "\n".join(new_logs)
        await asyncio.sleep(1)
```

---

# Resource Caching

## Optimizar lecturas

---

```python
from functools import lru_cache
from datetime import datetime, timedelta

# Caché simple con lru_cache
@lru_cache(maxsize=128)
@mcp.resource("config://app/settings")
def get_cached_settings() -> str:
    """Configuración cacheada."""
    return json.dumps(db.get_settings())

# Caché con TTL
cache_store = {}

def cached_resource(ttl_seconds: int = 60):
    """Decorador de caché con TTL."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            
            if cache_key in cache_store:
                cached, timestamp = cache_store[cache_key]
                if datetime.now() - timestamp < timedelta(seconds=ttl_seconds):
                    return cached
            
            result = await func(*args, **kwargs)
            cache_store[cache_key] = (result, datetime.now())
            return result
        
        return wrapper
    return decorator

@mcp.resource("data://{dataset}/summary")
@cached_resource(ttl_seconds=300)
async def get_dataset_summary(dataset: str) -> str:
    """Resumen de dataset con caché de 5 minutos."""
    return generate_summary(dataset)
```

---

# Resources vs Tools

## Cuándo usar cada uno

---

### Usar Resources cuando:

- El modelo necesita contexto para razonar
- Los datos cambian independientemente del modelo
- Quieres que el modelo "vea" información
- Múltiples herramientas pueden necesitar los mismos datos

---

### Usar Tools cuando:

- El modelo necesita realizar una acción
- La operación tiene efectos secundarios
- Necesitas validar o autorizar explícitamente
- La operación es específica y no de "lectura"

---

# Ejemplo: Sistema de Documentos

---

```python
from fastmcp import FastMCP

mcp = FastMCP("document-system")

# Resources - para lectura de contexto
@mcp.resource("docs://{doc_id}")
def read_document(doc_id: str) -> str:
    """Lee el contenido de un documento."""
    doc = db.get_document(doc_id)
    return doc.content

@mcp.resource("docs://{doc_id}/metadata")
def read_doc_metadata(doc_id: str) -> str:
    """Metadatos del documento."""
    doc = db.get_document(doc_id)
    return json.dumps({
        "id": doc.id,
        "title": doc.title,
        "created_at": doc.created_at,
        "author": doc.author
    })

# Tools - para acciones
@mcp.tool
def create_document(
    title: str,
    content: str,
    author: str
) -> dict:
    """Crea un nuevo documento."""
    doc = db.create_document(title, content, author)
    return {"success": True, "data": doc}

@mcp.tool
def update_document(
    doc_id: str,
    content: str
) -> dict:
    """Actualiza el contenido de un documento."""
    doc = db.update_document(doc_id, content=content)
    return {"success": True, "data": doc}
```

---

# PARTE 5: DISEÑO DE PROMPTS

---

# ¿Qué son los Prompts?

## Plantillas de interacción

---

**Definición:**

Un prompt es una plantilla predefinida que el modelo puede usar para establecer contexto, modo de operación o instrucciones específicas.

---

**Características:**

- Contenido estático o parametrizado
- Reutilizable
- Puede incluir recursos embebidos
- Facilita flujos de trabajo comunes

---

**Usos:**

- Modos de especialización ("actúa como experto en...")
- Flujos de trabajo recurrentes
- Contextos específicos por dominio
- Instrucciones complejas predefinidas

---

# Prompts en FastMCP

## Definición básica

---

```python
from fastmcp import FastMCP

mcp = FastMCP("mi-servidor")

@mcp.prompt
def code_review(language: str) -> str:
    """Revisa código fuente buscando errores y mejoras."""
    return f"""Por favor, revisa el siguiente código {language}:

1. Busca errores de lógica
2. Identifica problemas de rendimiento
3. Sugiere mejoras de estilo
4. Verifica seguridad

Código a revisir:
```{language}
{{code}}
```
"""

@mcp.prompt
def analyze_data(data_type: str, depth: str = "basic") -> str:
    """Analiza datos y genera insights."""
    return f"""Eres un analista de datos experto. 
Tu especialidad es {data_type}.

Analiza los siguientes datos con profundidad {depth}:

{data}

Proporciona:
1. Resumen ejecutivo
2. Patrones identificados
3. Anomalías detectadas
4. Recomendaciones
"""
```

---

# Prompts con Argumentos

---

```python
from fastmcp import FastMCP
from pydantic import BaseModel

class CodeReviewArgs(BaseModel):
    language: str
    focus: str = "general"  # security, performance, style
    severity_threshold: str = "medium"

@mcp.prompt
def code_review_advanced(args: CodeReviewArgs) -> str:
    """Revisión de código avanzada."""
    
    focus_instructions = {
        "security": "Prioriza vulnerabilidades OWASP Top 10",
        "performance": "Busca cuellos de botella y optimizaciones",
        "style": "Verifica convenciones y legibilidad",
        "general": "Revisión completa de todos los aspectos"
    }
    
    return f"""Eres un experto en revisión de código {args.language}.

Enfoque: {focus_instructions.get(args.focus, args.focus)}
Umbral de severidad: {args.severity_threshold}

Para cada problema encontrado, indica:
- Tipo de problema
- Severidad (low, medium, high, critical)
- Ubicación exacta (línea)
- Recomendación de corrección

Código a revisar:
```{args.language}
{{code}}
```
"""
```

---

# Prompts Especializados

## Modos de operación

---

### Modo Experto

```python
@mcp.prompt
def security_audit(severity: str = "medium") -> str:
    """Auditoría de seguridad de código."""
    return f"""Eres un experto en seguridad informática con 20 años de experiencia.

Tu especialidad es identificar vulnerabilidades en código.

Nivel mínimo de severidad: {severity}

Para cada problema encontrado, indica:
- Tipo de vulnerabilidad (OWASP Top 10)
- Severidad (low, medium, high, critical)
- Ubicación exacta
- Recomendación de corrección
- Referencias a CVEs si aplica
- Explotabilidad potencial

Código a auditar:
```
{{code}}
```
"""
```

---

### Modo Flujo de Trabajo

```python
@mcp.prompt
def deployment_workflow() -> str:
    """Guía el proceso de despliegue paso a paso."""
    return """Eres un ingeniero DevOps senior.

Guía al usuario a través del proceso de despliegue paso a paso.

Reglas:
1. No pases al siguiente paso hasta que el usuario confirme
2. Verifica cada paso antes de continuar
3. Si hay errores, ayuda a resolverlos antes de continuar
4. Proporciona comandos específicos cuando sea posible

Pasos del despliegue:
1. Preparación del entorno
2. Configuración de variables
3. Build de la aplicación
4. Tests de integración
5. Despliegue a staging
6. Verificación en staging
7. Despliegue a producción
8. Verificación final

¿Por dónde empezamos?
"""
```

---

# Prompts con Recursos Embebidos

---

```python
@mcp.prompt
def analyze_repository(repo_url: str, branch: str = "main") -> str:
    """Analiza un repositorio de código."""
    return f"""Eres un arquitecto de software.

Analiza el repositorio {repo_url} (rama: {branch}).

Para el análisis, consulta:
- resource:repo://{repo_url}/structure - Estructura del repositorio
- resource:repo://{repo_url}/{branch}/readme - README

Proporciona:
1. Resumen de arquitectura
2. Tecnologías utilizadas
3. Calidad del código (1-10)
4. Deuda técnica detectada
5. Recomendaciones de mejora

Repositorio: {repo_url}
Rama: {branch}
"""
```

---

# PARTE 6: MANEJO DE ERRORES

---

# Filosofía de Errores

## El modelo necesita información

---

**Principio:**

Los errores no son solo para humanos. El modelo necesita entender qué salió mal para poder recuperarse.

---

**Tipos de errores:**

1. **Validación** - Entrada inválida
2. **Autorización** - Sin permisos
3. **Recurso no encontrado** - El recurso no existe
4. **Conflicto** - Estado inconsistente
5. **Límites** - Rate limit, cuota
6. **Interno** - Error del sistema

---

# Estructura de Error

## Formato estándar

---

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class ErrorResponse:
    """Respuesta de error estándar."""
    success: bool = False
    error: dict[str, Any] = None
    
    @classmethod
    def create(
        cls,
        code: str,
        message: str,
        details: dict | None = None,
        suggestion: str | None = None,
        request_id: str | None = None
    ) -> dict:
        return {
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "details": details or {},
                "suggestion": suggestion,
                "request_id": request_id
            }
        }

# Uso
return ErrorResponse.create(
    code="VALIDATION_ERROR",
    message="El campo 'email' no tiene un formato válido",
    details={
        "field": "email",
        "value": "not-an-email",
        "expected": "Formato: usuario@dominio.com"
    },
    suggestion="Verifique el formato del email"
)
```

---

# Códigos de Error

## Taxonomía estándar

---

| Categoría | Código | HTTP equivalente |
|-----------|--------|------------------|
| Validación | `VALIDATION_ERROR` | 400 |
| Validación | `MISSING_PARAMETER` | 400 |
| Validación | `INVALID_FORMAT` | 400 |
| Autorización | `UNAUTHORIZED` | 401 |
| Autorización | `FORBIDDEN` | 403 |
| Recurso | `NOT_FOUND` | 404 |
| Recurso | `ALREADY_EXISTS` | 409 |
| Conflicto | `CONFLICT` | 409 |
| Conflicto | `PRECONDITION_FAILED` | 412 |
| Límites | `RATE_LIMIT_EXCEEDED` | 429 |
| Límites | `QUOTA_EXCEEDED` | 402 |
| Interno | `INTERNAL_ERROR` | 500 |
| Interno | `SERVICE_UNAVAILABLE` | 503 |

---

# Errores de Validación

## Entrada incorrecta

---

```python
from typing import Annotated
from pydantic import Field, ValidationError

@mcp.tool
def create_user(
    email: Annotated[str, Field(description="Email del usuario")],
    name: Annotated[str, Field(min_length=2, max_length=100)],
    age: Annotated[int | None, Field(ge=0, le=150)] = None
) -> dict:
    """Crea un nuevo usuario."""
    
    errors = []
    
    # Validar email
    if not email:
        errors.append({
            "field": "email",
            "code": "MISSING_PARAMETER",
            "message": "email es obligatorio"
        })
    elif not is_valid_email(email):
        errors.append({
            "field": "email",
            "code": "INVALID_FORMAT",
            "message": "email no tiene un formato válido",
            "value": email,
            "expected": "usuario@dominio.com"
        })
    
    # Validar edad
    if age is not None:
        if age < 0 or age > 150:
            errors.append({
                "field": "age",
                "code": "OUT_OF_RANGE",
                "message": "age debe estar entre 0 y 150",
                "value": age,
                "min": 0,
                "max": 150
            })
    
    if errors:
        return {
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Se encontraron errores de validación",
                "details": errors
            }
        }
    
    # Crear usuario...
```

---

# Errores de Autorización

## Permisos insuficientes

---

```python
from typing import Any

@mcp.tool
def delete_user(
    user_id: str,
    context: dict[str, Any] | None = None
) -> dict:
    """Elimina un usuario."""
    
    # Verificar autenticación
    if not context or not context.get("user"):
        return {
            "success": False,
            "error": {
                "code": "UNAUTHORIZED",
                "message": "Se requiere autenticación para esta operación",
                "suggestion": "Inicie sesión y vuelva a intentarlo"
            }
        }
    
    user = context["user"]
    
    # Verificar permisos específicos
    if "users:delete" not in user.get("permissions", []):
        return {
            "success": False,
            "error": {
                "code": "FORBIDDEN",
                "message": "No tiene permisos para eliminar usuarios",
                "details": {
                    "required_permission": "users:delete",
                    "current_permissions": user.get("permissions", [])
                },
                "suggestion": "Contacte con el administrador"
            }
        }
    
    # Verificar ownership
    if user_id != user["id"] and not user.get("is_admin"):
        return {
            "success": False,
            "error": {
                "code": "FORBIDDEN",
                "message": "Solo puede eliminar su propio usuario",
                "suggestion": "Especifique su propio ID de usuario"
            }
        }
    
    # Procesar eliminación...
```

---

# Errores de Recurso

## No encontrado o ya existe

---

### Not Found

```python
@mcp.tool
def get_order(order_id: str) -> dict:
    """Obtiene un pedido por ID."""
    order = db.get_order(order_id)
    
    if not order:
        return {
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": f"Pedido {order_id} no encontrado",
                "details": {
                    "resource": "order",
                    "identifier": order_id
                },
                "suggestion": (
                    "Verifique el ID o use list_orders "
                    "para ver pedidos disponibles"
                )
            }
        }
    
    return {"success": True, "data": order}
```

---

### Already Exists

```python
@mcp.tool
def create_user(email: str, name: str) -> dict:
    """Crea un nuevo usuario."""
    existing = db.get_user_by_email(email)
    
    if existing:
        return {
            "success": False,
            "error": {
                "code": "ALREADY_EXISTS",
                "message": f"Ya existe un usuario con el email {email}",
                "details": {
                    "resource": "user",
                    "identifier": email,
                    "existing_id": existing.id
                },
                "suggestion": (
                    "Use un email diferente o "
                    "recupere su cuenta existente"
                )
            }
        }
    
    # Crear nuevo usuario...
```

---

# Errores de Conflicto

## Estado inconsistente

---

```python
@mcp.tool
def update_order_status(
    order_id: str,
    new_status: str
) -> dict:
    """Actualiza el estado de un pedido."""
    order = db.get_order(order_id)
    
    if not order:
        return {
            "success": False,
            "error": {"code": "NOT_FOUND", "message": "Pedido no encontrado"}
        }
    
    # Verificar estado actual
    if order.status == "cancelled":
        return {
            "success": False,
            "error": {
                "code": "CONFLICT",
                "message": "No se puede modificar un pedido cancelado",
                "details": {
                    "current_state": order.status,
                    "attempted_action": "update"
                },
                "suggestion": "Cree un nuevo pedido si necesita realizar cambios"
            }
        }
    
    if order.status == "delivered" and new_status == "pending":
        return {
            "success": False,
            "error": {
                "code": "PRECONDITION_FAILED",
                "message": "No se puede revertir un pedido entregado a pendiente",
                "details": {
                    "current_state": order.status,
                    "attempted_state": new_status
                },
                "suggestion": "Use get_order para ver el estado actual"
            }
        }
    
    # Actualizar estado...
```

---

# Errores de Límites

## Rate limit y cuotas

---

```python
from utils.rate_limit import limiter

@mcp.tool
def search_users(
    query: str,
    context: dict | None = None
) -> dict:
    """Busca usuarios con rate limiting."""
    
    # Identificador
    identifier = (
        context.get("user", {}).get("id", "anonymous")
        if context else "anonymous"
    )
    
    # Verificar rate limit
    rate = limiter.check(identifier)
    
    if not rate["allowed"]:
        retry_after = int(
            (rate["reset_at"] - datetime.now()).total_seconds()
        )
        return {
            "success": False,
            "error": {
                "code": "RATE_LIMIT_EXCEEDED",
                "message": "Ha excedido el límite de peticiones",
                "details": {
                    "limit": 50,
                    "window": "1 minuto",
                    "retry_after": retry_after
                },
                "suggestion": "Espere antes de realizar más peticiones"
            }
        }
    
    # Verificar cuota
    if context and context.get("user"):
        quota = check_quota(context["user"]["id"])
        if quota["used"] >= quota["limit"]:
            return {
                "success": False,
                "error": {
                    "code": "QUOTA_EXCEEDED",
                    "message": "Ha excedido su cuota mensual",
                    "details": {
                        "quota_used": quota["used"],
                        "quota_limit": quota["limit"],
                        "quota_reset": quota["reset_date"]
                    },
                    "suggestion": "Actualice su plan o espere al próximo período"
                }
            }
    
    # Procesar búsqueda...
```

---

# Errores Internos

## Registrar sin exponer

---

```python
import logging
import uuid

logger = logging.getLogger(__name__)

@mcp.tool
def process_payment(
    amount: float,
    card_token: str
) -> dict:
    """Procesa un pago."""
    request_id = str(uuid.uuid4())[:8]
    
    try:
        result = payment_service.process(amount, card_token)
        return {"success": True, "data": result}
        
    except PaymentError as e:
        # Registrar con detalle
        logger.error(
            "Payment processing failed",
            extra={
                "request_id": request_id,
                "error": str(e),
                "amount": amount
            }
        )
        
        # Devolver error genérico
        return {
            "success": False,
            "error": {
                "code": "PAYMENT_ERROR",
                "message": "Error al procesar el pago",
                "request_id": request_id,
                "suggestion": (
                    "Si el problema persiste, contacte "
                    f"con soporte con el ID: {request_id}"
                )
            }
        }
        
    except Exception as e:
        # Error inesperado
        logger.exception(
            "Unexpected error in process_payment",
            extra={"request_id": request_id}
        )
        
        return {
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Ocurrió un error interno inesperado",
                "request_id": request_id
            }
        }
```

---

# Recuperación de Errores

## El modelo puede reintentar

---

```python
@mcp.tool
def send_notification(
    user_id: str,
    message: str
) -> dict:
    """Envía una notificación."""
    
    try:
        result = notification_service.send(user_id, message)
        return {"success": True, "data": result}
        
    except ServiceUnavailableError:
        return {
            "success": False,
            "error": {
                "code": "SERVICE_UNAVAILABLE",
                "message": "El servicio de notificaciones no está disponible",
                "retryable": True,
                "retry_after": 30,
                "alternative_actions": [
                    {
                        "action": "retry",
                        "description": "Reintentar en 30 segundos"
                    },
                    {
                        "action": "use_fallback",
                        "tool": "queue_notification",
                        "description": "Encolar para envío posterior"
                    }
                ]
            }
        }
```

---

# PARTE 7: SEGURIDAD

---

# Principios de Seguridad

## Límites de confianza

---

**Principio fundamental:**

Todo input que viene del modelo es potencialmente malicioso.

---

**Reglas:**

1. Nunca confíes en el modelo para validación de seguridad
2. Siempre valida en el servidor
3. Nunca expongas credenciales
4. Minimiza los privilegios de cada tool
5. Registra todas las operaciones sensibles

---

# Validación de Entrada

## Primera línea de defensa

---

```python
import re

@mcp.tool
def get_user(user_id: str) -> dict:
    """Obtiene un usuario por ID."""
    
    # ❌ Malo: usar directamente
    # query = f"SELECT * FROM users WHERE id = '{user_id}'"
    
    # ✅ Bueno: validar primero
    if not re.match(r"^usr_[a-zA-Z0-9]+$", user_id):
        return {
            "success": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "user_id tiene un formato inválido"
            }
        }
    
    # ✅ Mejor: usar parámetros
    query = "SELECT * FROM users WHERE id = ?"
    user = db.execute(query, (user_id,))
    
    return {"success": True, "data": user}
```

---

# SQL Injection

## Peligro clásico

---

**Entrada maliciosa:**

```json
{
  "user_id": "usr_123' OR '1'='1"
}
```

---

**Consulta vulnerable:**

```python
# ❌ PELIGROSO
query = f"SELECT * FROM users WHERE id = '{user_id}'"
# Resultado: SELECT * FROM users WHERE id = 'usr_123' OR '1'='1'
```

---

**Consulta segura:**

```python
# ✅ SEGURO - Usar parámetros
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

---

# Path Traversal

## Acceso a archivos no autorizados

---

**Entrada maliciosa:**

```json
{
  "filename": "../../../etc/passwd"
}
```

---

**Código vulnerable:**

```python
# ❌ PELIGROSO
@mcp.tool
def read_file(filename: str) -> dict:
    with open(f"./files/{filename}") as f:
        return {"content": f.read()}
```

---

**Código seguro:**

```python
import os
from pathlib import Path

BASE_DIR = Path("./files").resolve()

@mcp.tool
def read_file(filename: str) -> dict:
    """Lee un archivo de forma segura."""
    
    # Normalizar ruta
    file_path = (BASE_DIR / filename).resolve()
    
    # Verificar que está dentro del directorio permitido
    if not str(file_path).startswith(str(BASE_DIR)):
        return {
            "success": False,
            "error": {
                "code": "FORBIDDEN",
                "message": "Acceso denegado al archivo"
            }
        }
    
    try:
        content = file_path.read_text()
        return {"success": True, "data": {"content": content}}
    except FileNotFoundError:
        return {
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": f"Archivo {filename} no encontrado"
            }
        }
```

---

# Command Injection

## Ejecución de comandos

---

**Entrada maliciosa:**

```json
{
  "name": "file; rm -rf /"
}
```

---

**Código vulnerable:**

```python
# ❌ PELIGROSO
import os

@mcp.tool
def process_file(name: str) -> dict:
    result = os.popen(f"process-file {name}").read()
    return {"result": result}
```

---

**Código seguro:**

```python
import subprocess
import re

@mcp.tool
def process_file(name: str) -> dict:
    """Procesa un archivo de forma segura."""
    
    # Validar entrada
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        return {
            "success": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "name solo puede contener caracteres alfanuméricos"
            }
        }
    
    # Usar subprocess con lista de argumentos
    result = subprocess.run(
        ["process-file", name],
        capture_output=True,
        text=True
    )
    
    return {"success": True, "data": {"output": result.stdout}}
```

---

# Autorización

## Verificar permisos

---

```python
from typing import Any
import logging

logger = logging.getLogger(__name__)

def check_auth(context: dict | None) -> dict | None:
    """Verifica autenticación."""
    if not context or not context.get("user"):
        return {
            "success": False,
            "error": {
                "code": "UNAUTHORIZED",
                "message": "Requiere autenticación"
            }
        }
    return None

def check_permission(
    context: dict,
    permission: str
) -> dict | None:
    """Verifica permiso específico."""
    user = context.get("user", {})
    if permission not in user.get("permissions", []):
        return {
            "success": False,
            "error": {
                "code": "FORBIDDEN",
                "message": f"No tiene permiso: {permission}"
            }
        }
    return None

@mcp.tool
def delete_user(
    user_id: str,
    context: dict[str, Any] | None = None
) -> dict:
    """Elimina un usuario."""
    
    # 1. Verificar autenticación
    if error := check_auth(context):
        return error
    
    # 2. Verificar permisos
    if error := check_permission(context, "users:delete"):
        return error
    
    # 3. Verificar ownership
    user = context["user"]
    if user_id != user["id"] and not user.get("is_admin"):
        return {
            "success": False,
            "error": {
                "code": "FORBIDDEN",
                "message": "Solo puede eliminar su propio usuario"
            }
        }
    
    # 4. Registrar acceso
    logger.info(
        "User deletion",
        extra={
            "actor": user["id"],
            "target": user_id,
            "action": "delete"
        }
    )
    
    # 5. Procesar
    db.delete_user(user_id)
    return {"success": True}
```

---

# Auditoría y Logging

## Trazabilidad

---

```python
import logging
from datetime import datetime
from functools import wraps

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
audit_logger = logging.getLogger("audit")

def audit_log(action: str):
    """Decorador para logging de auditoría."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            context = kwargs.get("context", {})
            user_id = context.get("user", {}).get("id", "anonymous")
            
            # Registrar intento
            audit_logger.info(
                f"{action}_ATTEMPT",
                extra={
                    "user": user_id,
                    "action": action,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            try:
                result = func(*args, **kwargs)
                
                # Registrar éxito
                audit_logger.info(
                    f"{action}_SUCCESS",
                    extra={
                        "user": user_id,
                        "action": action
                    }
                )
                
                return result
                
            except Exception as e:
                # Registrar error
                audit_logger.error(
                    f"{action}_FAILED",
                    extra={
                        "user": user_id,
                        "action": action,
                        "error": str(e)
                    }
                )
                raise
        
        return wrapper
    return decorator

@mcp.tool
@audit_log("DELETE_USER")
def delete_user(user_id: str, context: dict | None = None) -> dict:
    """Elimina un usuario."""
    # Implementación...
```

---

# Secrets y Credenciales

## Nunca exponer

---

**❌ Nunca hacer:**

```python
@mcp.tool
def get_database_config() -> dict:
    """❌ PELIGROSO - Expone credenciales."""
    return {
        "success": True,
        "data": {
            "host": os.environ["DB_HOST"],
            "user": os.environ["DB_USER"],
            "password": os.environ["DB_PASSWORD"]  # NUNCA
        }
    }
```

---

**✅ Correcto:**

```python
@mcp.tool
def test_database_connection() -> dict:
    """Prueba la conexión a la base de datos."""
    try:
        db.ping()
        return {
            "success": True,
            "data": {
                "connected": True,
                "latency_ms": db.latency
            }
        }
    except Exception:
        return {
            "success": False,
            "error": {
                "code": "DB_CONNECTION_ERROR",
                "message": "No se pudo conectar a la base de datos"
            }
        }
```

---

# PARTE 8: RENDIMIENTO

---

# Optimización

## Minimizar tokens y latencia

---

**Principio:**

Cada token consume recursos del modelo. Cada operación añade latencia.

---

**Estrategias:**

1. Devolver solo datos necesarios
2. Usar paginación
3. Implementar caché
4. Paralelizar cuando sea posible
5. Comprimir respuestas

---

# Minimizar Tokens

## Devolver lo esencial

---

**❌ Innecesariamente verboso:**

```python
@mcp.tool
def get_user(user_id: str) -> dict:
    user = db.get_user(user_id)
    return {
        "success": True,
        "data": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "city": user.city,
            "country": user.country,
            "postal_code": user.postal_code,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "last_login": user.last_login,
            "preferences": user.preferences,
            "subscription": user.subscription
        }
    }
```

---

**✅ Solo lo necesario:**

```python
@mcp.tool
def get_user(user_id: str) -> dict:
    """Obtiene un usuario."""
    user = db.get_user(user_id)
    return {
        "success": True,
        "data": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }
```

---

# Selección de Campos

## Permitir elegir

---

```python
from typing import Literal

@mcp.tool
def get_user(
    user_id: str,
    fields: list[Literal[
        "id", "name", "email", "phone", "address"
    ]] | None = None
) -> dict:
    """Obtiene un usuario con campos opcionales."""
    user = db.get_user(user_id)
    
    # Campos por defecto
    default_fields = ["id", "name", "email"]
    selected_fields = fields or default_fields
    
    # Filtrar campos
    result = {
        field: getattr(user, field)
        for field in selected_fields
        if hasattr(user, field)
    }
    
    return {"success": True, "data": result}
```

---

# Caché Estratégico

## Implementación

---

```python
from functools import lru_cache
from datetime import datetime, timedelta
import hashlib

# Caché simple
@lru_cache(maxsize=128)
def get_cached_user(user_id: str) -> dict:
    """Usuario cacheado."""
    return db.get_user(user_id)

# Caché con TTL
cache_store: dict[str, tuple[any, datetime]] = {}

def get_with_ttl(key: str, ttl_seconds: int = 60):
    """Obtiene valor del caché con TTL."""
    if key in cache_store:
        value, timestamp = cache_store[key]
        if datetime.now() - timestamp < timedelta(seconds=ttl_seconds):
            return value
        del cache_store[key]
    return None

def set_with_ttl(key: str, value: any, ttl_seconds: int = 60):
    """Guarda valor en caché con TTL."""
    cache_store[key] = (value, datetime.now())

@mcp.tool
def get_user_cached(user_id: str) -> dict:
    """Obtiene usuario con caché."""
    cache_key = f"user:{user_id}"
    
    # Intentar caché
    cached = get_with_ttl(cache_key, ttl_seconds=60)
    if cached:
        return {
            "success": True,
            "data": cached,
            "from_cache": True
        }
    
    # Buscar en DB
    user = db.get_user(user_id)
    set_with_ttl(cache_key, user, ttl_seconds=60)
    
    return {
        "success": True,
        "data": user,
        "from_cache": False
    }
```

---

# Paralelización

## asyncio para operaciones paralelas

---

**Secuencial (lento):**

```python
@mcp.tool
def get_user_dashboard(user_id: str) -> dict:
    """Dashboard del usuario - secuencial."""
    user = db.get_user(user_id)        # 100ms
    orders = db.get_orders(user_id)    # 150ms
    payments = db.get_payments(user_id) # 100ms
    
    return {
        "success": True,
        "data": {"user": user, "orders": orders, "payments": payments}
    }
# Total: 350ms
```

---

**Paralelo (rápido):**

```python
import asyncio

@mcp.tool
async def get_user_dashboard_async(user_id: str) -> dict:
    """Dashboard del usuario - paralelo."""
    # Ejecutar en paralelo
    user, orders, payments = await asyncio.gather(
        db.get_user_async(user_id),
        db.get_orders_async(user_id),
        db.get_payments_async(user_id)
    )
    
    return {
        "success": True,
        "data": {"user": user, "orders": orders, "payments": payments}
    }
# Total: max(100, 150, 100) = 150ms
```

---

# Batching

## Reducir llamadas

---

**Sin batching:**

```python
@mcp.tool
def get_users_one_by_one(user_ids: list[str]) -> dict:
    """❌ Ineficiente - N consultas."""
    users = []
    for user_id in user_ids:
        user = db.get_user(user_id)  # 1 consulta por usuario
        users.append(user)
    return {"success": True, "data": users}
```

---

**Con batching:**

```python
@mcp.tool
def get_users_batch(user_ids: list[str]) -> dict:
    """✅ Eficiente - 1 consulta."""
    users = db.get_users(user_ids)  # 1 consulta para todos
    return {"success": True, "data": users}
```

---

# PARTE 9: TESTING

---

# Testing de Servicios MCP

## Estrategias

---

### Unit Tests

- Validar lógica de cada tool
- Probar validaciones
- Verificar respuestas de error

---

### Integration Tests

- Probar con el protocolo MCP real
- Verificar transporte
- Testear recursos y prompts

---

### End-to-End Tests

- Probar con clientes reales
- Verificar flujos completos
- Validar interacción con modelos

---

# Unit Tests

## Probar tools individualmente

---

```python
# tests/test_tools.py
import pytest
from unittest.mock import Mock, patch
from tools.users import get_user, create_user

class TestGetUser:
    """Tests para get_user."""
    
    @pytest.fixture
    def mock_db(self):
        with patch("tools.users.db") as mock:
            yield mock
    
    @pytest.mark.asyncio
    async def test_get_user_success(self, mock_db):
        """Debe retornar usuario cuando existe."""
        mock_db.get_user.return_value = {
            "id": "usr_123",
            "name": "Juan García",
            "email": "juan@example.com"
        }
        
        result = await get_user(user_id="usr_123")
        
        assert result["success"] is True
        assert result["data"]["id"] == "usr_123"
        assert result["data"]["name"] == "Juan García"
    
    @pytest.mark.asyncio
    async def test_get_user_not_found(self, mock_db):
        """Debe retornar error cuando no existe."""
        mock_db.get_user.return_value = None
        
        result = await get_user(user_id="usr_nonexistent")
        
        assert result["success"] is False
        assert result["error"]["code"] == "NOT_FOUND"
    
    @pytest.mark.asyncio
    async def test_get_user_invalid_id(self, mock_db):
        """Debe retornar error para ID inválido."""
        result = await get_user(user_id="invalid!")
        
        assert result["success"] is False
        assert result["error"]["code"] == "VALIDATION_ERROR"
```

---

# Probando Validación

---

```python
# tests/test_validation.py
import pytest
from pydantic import ValidationError
from models.user import UserCreate, UserUpdate

class TestUserValidation:
    """Tests de validación de usuario."""
    
    def test_valid_user_create(self):
        """Usuario válido debe pasar validación."""
        user = UserCreate(
            name="Juan García",
            email="juan@example.com"
        )
        assert user.name == "Juan García"
        assert user.email == "juan@example.com"
    
    def test_invalid_email(self):
        """Email inválido debe fallar."""
        with pytest.raises(ValidationError) as exc:
            UserCreate(name="Juan", email="not-an-email")
        
        errors = exc.value.errors()
        assert any("email" in str(e) for e in errors)
    
    def test_name_too_short(self):
        """Nombre muy corto debe fallar."""
        with pytest.raises(ValidationError) as exc:
            UserCreate(name="J", email="juan@example.com")
        
        errors = exc.value.errors()
        assert any("name" in str(e) for e in errors)
    
    def test_role_must_be_valid(self):
        """Rol debe ser válido."""
        with pytest.raises(ValidationError):
            UserCreate(name="Juan", email="juan@example.com", role="invalid")
```

---

# Probando Errores

---

```python
# tests/test_errors.py
import pytest
from unittest.mock import Mock, patch
from tools.users import delete_user
from errors.handlers import Errors, to_response

class TestErrorHandling:
    """Tests de manejo de errores."""
    
    @pytest.mark.asyncio
    async def test_database_error_graceful(self):
        """Error de DB debe ser manejado graciosamente."""
        with patch("tools.users.db") as mock_db:
            mock_db.get_user.side_effect = Exception("Connection refused")
            
            result = await get_user(user_id="usr_123")
            
            assert result["success"] is False
            assert result["error"]["code"] == "INTERNAL_ERROR"
            # No exponer detalles internos
            assert "Connection refused" not in str(result)
            # Incluir request_id para depuración
            assert result["error"].get("request_id") is not None
    
    @pytest.mark.asyncio
    async def test_authorization_error(self):
        """Error de autorización debe ser claro."""
        context = {
            "user": {
                "id": "usr_456",
                "role": "user"
            }
        }
        
        result = await delete_user(
            user_id="usr_123",
            context=context
        )
        
        assert result["success"] is False
        assert result["error"]["code"] == "FORBIDDEN"
```

---

# Integration Tests

## Probar con MCP Inspector

---

```python
# tests/test_integration.py
import pytest
import subprocess
import json
import time

class TestMCPIntegration:
    """Tests de integración con MCP."""
    
    @pytest.fixture(scope="class")
    def server_process(self):
        """Inicia servidor MCP para tests."""
        proc = subprocess.Popen(
            ["python", "-m", "my_mcp_server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)  # Esperar inicio
        yield proc
        proc.terminate()
    
    def test_list_tools(self, server_process):
        """Debe listar tools disponibles."""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 1
        }
        
        server_process.stdin.write(
            (json.dumps(request) + "\n").encode()
        )
        server_process.stdin.flush()
        
        response = server_process.stdout.readline()
        result = json.loads(response)
        
        assert "result" in result
        assert "tools" in result["result"]
        tool_names = [t["name"] for t in result["result"]["tools"]]
        assert "get_user" in tool_names
    
    def test_call_tool(self, server_process):
        """Debe ejecutar tool correctamente."""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "get_user",
                "arguments": {"user_id": "usr_123"}
            },
            "id": 2
        }
        
        server_process.stdin.write(
            (json.dumps(request) + "\n").encode()
        )
        server_process.stdin.flush()
        
        response = server_process.stdout.readline()
        result = json.loads(response)
        
        assert "result" in result
        assert result["result"]["success"] is True
```

---

# PARTE 10: CASOS DE ESTUDIO

---

# Caso 1: Servidor de Archivos

## Buenas prácticas aplicadas

---

**Requisito:**

Servidor MCP que permite leer y escribir archivos en un directorio específico.

---

```python
# file_server.py
from fastmcp import FastMCP
from pathlib import Path
import re

mcp = FastMCP("file-server")
BASE_DIR = Path("./data").resolve()

@mcp.tool(annotations={"readOnlyHint": True})
def read_file(
    filename: Annotated[str, Field(
        pattern=r"^[a-zA-Z0-9_.-]+$",
        description="Nombre del archivo (solo alfanuméricos, _, ., -)"
    )]
) -> dict:
    """Lee el contenido de un archivo del directorio de datos."""
    
    # Resolver ruta de forma segura
    file_path = (BASE_DIR / filename).resolve()
    
    # Verificar que está dentro del directorio permitido
    if not str(file_path).startswith(str(BASE_DIR)):
        return {
            "success": False,
            "error": {
                "code": "FORBIDDEN",
                "message": "Acceso denegado"
            }
        }
    
    try:
        content = file_path.read_text(encoding="utf-8")
        return {
            "success": True,
            "data": {
                "content": content,
                "filename": filename,
                "size": len(content)
            }
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": f"Archivo {filename} no encontrado"
            }
        }
    except PermissionError:
        return {
            "success": False,
            "error": {
                "code": "FORBIDDEN",
                "message": "Sin permisos para leer el archivo"
            }
        }

@mcp.tool(annotations={"destructiveHint": False})
def write_file(
    filename: str,
    content: str,
    mode: Literal["write", "append"] = "write"
) -> dict:
    """Escribe contenido en un archivo."""
    
    # Validar nombre
    if not re.match(r"^[a-zA-Z0-9_.-]+$", filename):
        return {
            "success": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "Nombre de archivo inválido"
            }
        }
    
    # Resolver ruta de forma segura
    file_path = (BASE_DIR / filename).resolve()
    
    if not str(file_path).startswith(str(BASE_DIR)):
        return {
            "success": False,
            "error": {"code": "FORBIDDEN", "message": "Acceso denegado"}
        }
    
    try:
        if mode == "append":
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(content)
        else:
            file_path.write_text(content, encoding="utf-8")
        
        return {
            "success": True,
            "data": {
                "filename": filename,
                "size": len(content),
                "mode": mode
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"Error al escribir: {str(e)}"
            }
        }

if __name__ == "__main__":
    mcp.run()
```

---

# Caso 2: Servidor de Base de Datos

## Constructor de consultas seguro

---

```python
# db_server.py
from fastmcp import FastMCP
from typing import Literal
from datetime import datetime

mcp = FastMCP("database-server")

@mcp.tool(annotations={"readOnlyHint": True})
def query_users(
    filters: dict | None = None,
    sort_by: Literal["created_at", "name", "email"] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
    limit: int = 20,
    offset: int = 0
) -> dict:
    """Busca usuarios con filtros y paginación."""
    
    # Construir query con filtros whitelist
    query = db.query("users")
    
    if filters:
        # Solo permitir campos específicos
        allowed_filters = ["status", "role", "created_after", "created_before"]
        
        for key, value in filters.items():
            if key not in allowed_filters:
                continue
            
            if key == "status" and value in ["active", "inactive", "pending"]:
                query = query.where("status", value)
            
            elif key == "role" and value in ["admin", "user", "guest"]:
                query = query.where("role", value)
            
            elif key == "created_after":
                query = query.where("created_at", ">=", value)
            
            elif key == "created_before":
                query = query.where("created_at", "<=", value)
    
    # Ordenamiento con whitelist
    query = query.order_by(sort_by, sort_order)
    
    # Paginación
    query = query.limit(limit).offset(offset)
    
    # Ejecutar
    users = query.execute()
    total = db.count("users")
    
    # Devolver solo campos necesarios
    return {
        "success": True,
        "data": {
            "items": [
                {
                    "id": u.id,
                    "name": u.name,
                    "email": u.email,
                    "status": u.status,
                    "role": u.role
                }
                for u in users
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total
        }
    }
```

---

# Caso 3: API Gateway

## Servidor que envuelve APIs externas

---

```python
# api_gateway.py
from fastmcp import FastMCP
import httpx
import asyncio

mcp = FastMCP("api-gateway")

# Cliente HTTP con timeout
client = httpx.AsyncClient(timeout=10.0)

@mcp.tool(annotations={
    "readOnlyHint": True,
    "openWorldHint": True
})
async def get_weather(
    city: str,
    units: Literal["celsius", "fahrenheit"] = "celsius"
) -> dict:
    """Obtiene el clima actual para una ciudad."""
    
    try:
        response = await client.get(
            "https://api.weather.com/current",
            params={"city": city, "units": units}
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": {
                    "temperature": data["temp"],
                    "conditions": data["conditions"],
                    "humidity": data["humidity"],
                    "city": city
                }
            }
        
        if response.status_code == 404:
            return {
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Ciudad '{city}' no encontrada"
                }
            }
        
        if response.status_code == 429:
            retry_after = response.headers.get("retry-after", "60")
            return {
                "success": False,
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "Límite de peticiones excedido",
                    "retry_after": int(retry_after)
                }
            }
        
        return {
            "success": False,
            "error": {
                "code": "EXTERNAL_SERVICE_ERROR",
                "message": f"Error del servicio: {response.status_code}"
            }
        }
        
    except httpx.TimeoutException:
        return {
            "success": False,
            "error": {
                "code": "TIMEOUT",
                "message": "Tiempo de espera agotado",
                "suggestion": "Inténtelo más tarde"
            }
        }
    
    except httpx.RequestError as e:
        return {
            "success": False,
            "error": {
                "code": "CONNECTION_ERROR",
                "message": "Error de conexión",
                "details": {"error": str(e)}
            }
        }

if __name__ == "__main__":
    mcp.run()
```

---

# Checklist de Buenas Prácticas

## Antes de publicar un servicio MCP

---

### Descripciones

- [ ] Todas las tools tienen docstrings claros
- [ ] Todos los parámetros tienen descripción con Field()
- [ ] Los valores de enum están documentados
- [ ] Se incluyen ejemplos para casos complejos

---

### Validación

- [ ] Se usan tipos Annotated con Field para validación
- [ ] Se validan rangos (ge, le)
- [ ] Se validan formatos (pattern, email)
- [ ] Se sanitizan strings antes de usar en consultas

---

### Seguridad

- [ ] No se exponen credenciales ni secrets
- [ ] Se previene path traversal con Path.resolve()
- [ ] Se previene SQL injection con parámetros
- [ ] Se verifican permisos en cada operación

---

### Errores

- [ ] Todos los errores tienen código
- [ ] Los errores incluyen sugerencias
- [ ] No se exponen detalles internos
- [ ] Se genera request_id para depuración

---

### Rendimiento

- [ ] Se usa paginación para listas grandes
- [ ] Se implementan cachés donde aplica
- [ ] Se minimizan los tokens en respuestas
- [ ] Se usa asyncio para operaciones paralelas

---

### Testing

- [ ] Unit tests para cada tool con pytest
- [ ] Tests de validación de entrada
- [ ] Tests de manejo de errores
- [ ] Integration tests con MCP Inspector

---

# PARTE 11: SAMPLING

---

# ¿Qué es Sampling?

## Solicitar generaciones de LLM desde el servidor

---

**Definición:**

**Sampling** es una característica de MCP que permite a un servidor solicitar al cliente que genere texto usando su modelo de lenguaje. Esto permite flujos de trabajo donde el servidor puede pedir al LLM que procese datos, genere contenido o tome decisiones.

---

**Casos de uso:**

- Generación de texto bajo demanda
- Análisis de contenido
- Resúmenes automáticos
- Traducción de textos
- Clasificación inteligente
- Toma de decisiones asistida por LLM

---

# Sampling en FastMCP

## Conceptos básicos

---

```python
from fastmcp import FastMCP
from fastmcp.server.sampling import SampleRequest, SampleResult

mcp = FastMCP("mi-servidor")

@mcp.tool
async def analyze_sentiment(text: str) -> dict:
 """Analiza el sentimiento de un texto usando el LLM del cliente."""
 
 # Crear solicitud de sampling
 request = SampleRequest(
 messages=[
 {"role": "user", "content": f"Analiza el sentimiento del siguiente texto. Responde SOLO con: positivo, negativo o neutral.\n\nTexto: {text}"}
 ],
 max_tokens=10,
 temperature=0.0  # Determinístico
 )
 
 # Solicitar sampling al cliente
 result: SampleResult = await mcp.sample(request)
 
 sentiment = result.content.strip().lower()
 
 return {
 "success": True,
 "data": {
 "sentiment": sentiment,
 "confidence": result.model.get("confidence", "unknown")
 }
 }
```

---

# Parámetros de SampleRequest

## Configuración de la generación

---

```python
from fastmcp.server.sampling import SampleRequest
from typing import Literal

request = SampleRequest(
 # Mensajes para el LLM (formato OpenAI-like)
 messages=[
 {"role": "system", "content": "Eres un asistente especializado en clasificación."},
 {"role": "user", "content": "Clasifica este texto..."}
 ],
 
 # Límite de tokens
 max_tokens=100,
 
 # Temperatura (0.0 = determinístico, 1.0 = creativo)
 temperature=0.3,
 
 # Modelo preferido (opcional)
 model_preferences=["claude-3-sonnet", "gpt-4o"],
 
 # Stop tokens (opcional)
 stop=["\n", "END"],
 
 # Top-p sampling (opcional)
 top_p=0.9,
 
 # Top-k sampling (opcional)
 top_k=50
)
```

---

# Ejemplo: Generación de Resúmenes

---

```python
from fastmcp import FastMCP
from fastmcp.server.sampling import SampleRequest

mcp = FastMCP("document-server")

@mcp.tool
async def summarize_document(
 doc_id: str,
 max_length: int = 200
) -> dict:
 """Genera un resumen de un documento usando el LLM del cliente."""
 
 # Obtener documento
 doc = db.get_document(doc_id)
 if not doc:
 return {"success": False, "error": {"code": "NOT_FOUND"}}
 
 # Verificar longitud
 if len(doc.content) < 100:
 return {
 "success": True,
 "data": {
 "summary": doc.content,
 "method": "original_too_short"
 }
 }
 
 # Solicitar resumen al LLM
 request = SampleRequest(
 messages=[
 {
 "role": "system",
 "content": "Eres un experto en resumir documentos. "
 "Genera resúmenes concisos y precisos."
 },
 {
 "role": "user",
 "content": f"Resume el siguiente documento en máximo {max_length} palabras:\n\n{doc.content[:5000]}"
 }
 ],
 max_tokens=max_length * 4, # ~4 tokens por palabra
 temperature=0.3
 )
 
 result = await mcp.sample(request)
 
 return {
 "success": True,
 "data": {
 "summary": result.content,
 "original_length": len(doc.content),
 "summary_length": len(result.content),
 "doc_id": doc_id
 }
 }
```

---

# Ejemplo: Clasificación Inteligente

---

```python
from fastmcp import FastMCP
from fastmcp.server.sampling import SampleRequest
import json

mcp = FastMCP("classifier-server")

@mcp.tool
async def classify_ticket(
 ticket_id: str,
 categories: list[str] = None
) -> dict:
 """Clasifica un ticket de soporte usando el LLM."""
 
 if not categories:
 categories = ["technical", "billing", "general", "urgent", "feature_request"]
 
 ticket = db.get_ticket(ticket_id)
 if not ticket:
 return {"success": False, "error": {"code": "NOT_FOUND"}}
 
 # Prompt de clasificación
 prompt = f"""Clasifica el siguiente ticket de soporte.

Categorías disponibles: {', '.join(categories)}

Responde SOLO con un JSON válido:
{{"category": "categoria", "confidence": 0.95, "reason": "breve explicación"}}

Ticket:
Asunto: {ticket.subject}
Descripción: {ticket.description}
"""

 request = SampleRequest(
 messages=[{"role": "user", "content": prompt}],
 max_tokens=150,
 temperature=0.0 # Determinístico
 )
 
 result = await mcp.sample(request)
 
 # Parsear respuesta
 try:
 classification = json.loads(result.content)
 return {
 "success": True,
 "data": {
 "ticket_id": ticket_id,
 "category": classification.get("category"),
 "confidence": classification.get("confidence"),
 "reason": classification.get("reason")
 }
 }
 except json.JSONDecodeError:
 return {
 "success": False,
 "error": {
 "code": "PARSE_ERROR",
 "message": "No se pudo parsear la clasificación"
 }
 }
```

---

# Sampling con Contexto de Conversación

---

```python
from fastmcp import FastMCP
from fastmcp.server.sampling import SampleRequest

mcp = FastMCP("chat-server")

@mcp.tool
async def suggest_response(
 conversation_id: str,
 context: str = ""
) -> dict:
 """Sugiere una respuesta para una conversación."""
 
 # Obtener historial
 messages = db.get_conversation_messages(conversation_id)
 
 # Construir contexto para el LLM
 llm_messages = [
 {
 "role": "system",
 "content": f"Eres un asistente útil. {context}"
 }
 ]
 
 # Añadir historial
 for msg in messages[-10:]: # Últimos 10 mensajes
 llm_messages.append({
 "role": msg.role,
 "content": msg.content
 })
 
 # Solicitar sugerencia
 llm_messages.append({
 "role": "user",
 "content": "Sugiere la próxima respuesta:"
 })
 
 request = SampleRequest(
 messages=llm_messages,
 max_tokens=500,
 temperature=0.7
 )
 
 result = await mcp.sample(request)
 
 return {
 "success": True,
 "data": {
 "suggestion": result.content,
 "conversation_id": conversation_id
 }
 }
```

---

# Buenas Prácticas para Sampling

---

### 1. Usar temperaturas bajas para tareas determinísticas

```python
# Clasificación, extracción, parsing
request = SampleRequest(temperature=0.0)
```

---

### 2. Limitar tokens apropiadamente

```python
# Solo lo necesario
request = SampleRequest(max_tokens=50) # Para respuestas cortas
```

---

### 3. Proporcionar contexto claro

```python
messages=[
 {"role": "system", "content": "Eres un experto en..."},
 {"role": "user", "content": "Instrucción específica..."}
]
```

---

### 4. Manejar errores de conexión

```python
try:
 result = await mcp.sample(request)
except SamplingError as e:
 return {
 "success": False,
 "error": {
 "code": "SAMPLING_UNAVAILABLE",
 "message": "El cliente no soporta sampling"
 }
 }
```

---

# PARTE 12: ELICITATION

---

# ¿Qué es Elicitation?

## Solicitar información al usuario desde el servidor

---

**Definición:**

**Elicitation** es una característica de MCP que permite al servidor solicitar información adicional al usuario durante la ejecución de una tool. Esto es útil cuando faltan parámetros o se necesita confirmación.

---

**Casos de uso:**

- Solicitar parámetros faltantes
- Pedir confirmación antes de acciones destructivas
- Clarificar ambigüedades
- Obtener preferencias del usuario
- Autenticación interactiva

---

# Elicitation en FastMCP

## Conceptos básicos

---

```python
from fastmcp import FastMCP
from fastmcp.server.elicitation import ElicitRequest, ElicitResult

mcp = FastMCP("mi-servidor")

@mcp.tool
async def delete_user(user_id: str) -> dict:
 """Elimina un usuario con confirmación."""
 
 # Verificar que existe
 user = db.get_user(user_id)
 if not user:
 return {"success": False, "error": {"code": "NOT_FOUND"}}
 
 # Solicitar confirmación
 request = ElicitRequest(
 message=f"¿Estás seguro de que deseas eliminar al usuario '{user.name}' ({user.email})? Esta acción es irreversible.",
 
 # Campos a solicitar
 fields={
 "confirm": {
 "type": "boolean",
 "description": "Confirmar eliminación",
 "required": True
 },
 "reason": {
 "type": "string",
 "description": "Razón de la eliminación (opcional)",
 "required": False
 }
 }
 )
 
 # Solicitar input al usuario
 result: ElicitResult = await mcp.elicit(request)
 
 if not result.values.get("confirm"):
 return {
 "success": False,
 "error": {
 "code": "CANCELLED",
 "message": "Eliminación cancelada por el usuario"
 }
 }
 
 # Proceder con eliminación
 db.delete_user(user_id)
 
 return {
 "success": True,
 "data": {
 "deleted": True,
 "reason": result.values.get("reason", "No especificada")
 }
 }
```

---

# Tipos de Campos en Elicitation

---

```python
from fastmcp.server.elicitation import ElicitRequest

request = ElicitRequest(
 message="Proporciona la información necesaria:",
 
 fields={
 # String simple
 "name": {
 "type": "string",
 "description": "Nombre del usuario",
 "required": True
 },
 
 # Email con validación
 "email": {
 "type": "string",
 "format": "email",
 "description": "Email del usuario",
 "required": True
 },
 
 # Número con restricciones
 "age": {
 "type": "integer",
 "description": "Edad del usuario",
 "minimum": 0,
 "maximum": 150,
 "required": False
 },
 
 # Booleano
 "newsletter": {
 "type": "boolean",
 "description": "¿Suscribirse al newsletter?",
 "default": False,
 "required": False
 },
 
 # Selección (enum)
 "role": {
 "type": "string",
 "enum": ["admin", "user", "guest"],
 "description": "Rol del usuario",
 "default": "user",
 "required": True
 },
 
 # Texto largo
 "bio": {
 "type": "string",
 "format": "textarea",
 "description": "Biografía del usuario",
 "maxLength": 500,
 "required": False
 }
 }
)
```

---

# Ejemplo: Formulario de Usuario

---

```python
from fastmcp import FastMCP
from fastmcp.server.elicitation import ElicitRequest, ElicitResult

mcp = FastMCP("user-management")

@mcp.tool
async def create_user_interactive() -> dict:
 """Crea un usuario interactuando con el usuario."""
 
 # Solicitar información
 request = ElicitRequest(
 message="Proporciona los datos del nuevo usuario:",
 
 fields={
 "name": {
 "type": "string",
 "description": "Nombre completo del usuario",
 "minLength": 2,
 "maxLength": 100,
 "required": True
 },
 
 "email": {
 "type": "string",
 "format": "email",
 "description": "Email del usuario",
 "required": True
 },
 
 "role": {
 "type": "string",
 "enum": ["admin", "user", "guest"],
 "description": "Rol del usuario",
 "default": "user",
 "required": True
 },
 
 "department": {
 "type": "string",
 "description": "Departamento (opcional)",
 "required": False
 },
 
 "send_welcome": {
 "type": "boolean",
 "description": "¿Enviar email de bienvenida?",
 "default": True,
 "required": False
 }
 }
 )
 
 result: ElicitResult = await mcp.elicit(request)
 
 # Validar email
 if not is_valid_email(result.values.get("email")):
 return {
 "success": False,
 "error": {
 "code": "INVALID_EMAIL",
 "message": "El email proporcionado no es válido"
 }
 }
 
 # Crear usuario
 user = db.create_user(
 name=result.values["name"],
 email=result.values["email"],
 role=result.values["role"],
 department=result.values.get("department"),
 send_welcome=result.values.get("send_welcome", True)
 )
 
 return {
 "success": True,
 "data": {
 "user_id": user.id,
 "name": user.name,
 "email": user.email,
 "role": user.role
 }
 }
```

---

# Ejemplo: Confirmación de Pago

---

```python
from fastmcp import FastMCP
from fastmcp.server.elicitation import ElicitRequest

mcp = FastMCP("payment-server")

@mcp.tool
async def process_payment(
 amount: float,
 currency: str = "EUR"
) -> dict:
 """Procesa un pago con confirmación del usuario."""
 
 # Validar monto
 if amount <= 0:
 return {
 "success": False,
 "error": {
 "code": "INVALID_AMOUNT",
 "message": "El monto debe ser mayor que 0"
 }
 }
 
 # Solicitar confirmación
 request = ElicitRequest(
 message=f"Confirma el pago de {amount:.2f} {currency}",
 
 fields={
 "confirm": {
 "type": "boolean",
 "description": "¿Confirmar el pago?",
 "required": True
 },
 
 "payment_method": {
 "type": "string",
 "enum": ["card", "bank_transfer", "paypal"],
 "description": "Método de pago",
 "required": True
 },
 
 "save_method": {
 "type": "boolean",
 "description": "¿Guardar método para futuros pagos?",
 "default": False,
 "required": False
 },
 
 "notes": {
 "type": "string",
 "description": "Notas (opcional)",
 "maxLength": 200,
 "required": False
 }
 }
 )
 
 result = await mcp.elicit(request)
 
 if not result.values.get("confirm"):
 return {
 "success": False,
 "error": {
 "code": "PAYMENT_CANCELLED",
 "message": "El usuario canceló el pago"
 }
 }
 
 # Procesar pago
 payment = payment_service.process(
 amount=amount,
 currency=currency,
 method=result.values["payment_method"],
 save_method=result.values.get("save_method", False),
 notes=result.values.get("notes")
 )
 
 return {
 "success": True,
 "data": {
 "payment_id": payment.id,
 "amount": amount,
 "currency": currency,
 "method": result.values["payment_method"],
 "status": payment.status
 }
 }
```

---

# Elicitation Múltiple (Wizard)

---

```python
from fastmcp import FastMCP
from fastmcp.server.elicitation import ElicitRequest

mcp = FastMCP("setup-wizard")

@mcp.tool
async def setup_project() -> dict:
 """Asistente de configuración de proyecto paso a paso."""
 
 # Paso 1: Información básica
 step1 = ElicitRequest(
 message="Paso 1/3: Información básica del proyecto",
 
 fields={
 "project_name": {
 "type": "string",
 "description": "Nombre del proyecto",
 "minLength": 3,
 "maxLength": 50,
 "required": True
 },
 
 "description": {
 "type": "string",
 "format": "textarea",
 "description": "Descripción del proyecto",
 "maxLength": 500,
 "required": False
 }
 }
 )
 
 result1 = await mcp.elicit(step1)
 
 # Paso 2: Tecnologías
 step2 = ElicitRequest(
 message=f"Paso 2/3: Tecnologías para '{result1.values['project_name']}'",
 
 fields={
 "language": {
 "type": "string",
 "enum": ["python", "javascript", "typescript", "go", "rust"],
 "description": "Lenguaje principal",
 "required": True
 },
 
 "framework": {
 "type": "string",
 "description": "Framework (opcional)",
 "required": False
 },
 
 "database": {
 "type": "string",
 "enum": ["postgresql", "mysql", "mongodb", "sqlite", "none"],
 "description": "Base de datos",
 "default": "postgresql",
 "required": True
 }
 }
 )
 
 result2 = await mcp.elicit(step2)
 
 # Paso 3: Confirmación
 step3 = ElicitRequest(
 message=f"Paso 3/3: Confirmar configuración",
 
 fields={
 "create_repo": {
 "type": "boolean",
 "description": "¿Crear repositorio Git?",
 "default": True,
 "required": True
 },
 
 "add_ci": {
 "type": "boolean",
 "description": "¿Añadir CI/CD?",
 "default": False,
 "required": False
 },
 
 "proceed": {
 "type": "boolean",
 "description": "¿Crear proyecto?",
 "required": True
 }
 }
 )
 
 result3 = await mcp.elicit(step3)
 
 if not result3.values.get("proceed"):
 return {
 "success": False,
 "error": {
 "code": "CANCELLED",
 "message": "Configuración cancelada"
 }
 }
 
 # Crear proyecto
 project = create_project(
 name=result1.values["project_name"],
 description=result1.values.get("description"),
 language=result2.values["language"],
 framework=result2.values.get("framework"),
 database=result2.values["database"],
 create_repo=result3.values.get("create_repo", True),
 add_ci=result3.values.get("add_ci", False)
 )
 
 return {
 "success": True,
 "data": {
 "project_id": project.id,
 "name": project.name,
 "path": project.path,
 "steps_completed": 3
 }
 }
```

---

# Combinar Sampling y Elicitation

---

```python
from fastmcp import FastMCP
from fastmcp.server.sampling import SampleRequest
from fastmcp.server.elicitation import ElicitRequest

mcp = FastMCP("smart-assistant")

@mcp.tool
async def smart_search(query: str) -> dict:
 """Búsqueda inteligente con clarificación."""
 
 # Usar sampling para entender la intención
 sample_req = SampleRequest(
 messages=[{
 "role": "user",
 "content": f"El usuario busca: '{query}'. ¿Qué tipo de búsqueda es? Responde SOLO: users, products, orders o unknown"
 }],
 max_tokens=10,
 temperature=0.0
 )
 
 sample_result = await mcp.sample(sample_req)
 intent = sample_result.content.strip().lower()
 
 if intent == "unknown":
 # Usar elicitation para clarificar
 elicit_req = ElicitRequest(
 message="No entendí tu búsqueda. ¿Qué buscas?",
 
 fields={
 "search_type": {
 "type": "string",
 "enum": ["users", "products", "orders"],
 "description": "Tipo de búsqueda",
 "required": True
 },
 
 "search_term": {
 "type": "string",
 "description": "Término de búsqueda",
 "required": True
 }
 }
 )
 
 elicit_result = await mcp.elicit(elicit_req)
 
 intent = elicit_result.values["search_type"]
 query = elicit_result.values["search_term"]
 
 # Realizar búsqueda
 if intent == "users":
 results = db.search_users(query)
 elif intent == "products":
 results = db.search_products(query)
 else:
 results = db.search_orders(query)
 
 return {
 "success": True,
 "data": {
 "type": intent,
 "query": query,
 "results": results
 }
 }
```

---

# Buenas Prácticas para Elicitation

---

### 1. Usar para interacciones necesarias, no opcionales

```python
# Correcto: Confirmar antes de eliminar
if is_destructive:
 await mcp.elicit(confirm_request)
```

---

### 2. Proporcionar defaults sensatos

```python
"newsletter": {
 "type": "boolean",
 "description": "¿Suscribirse al newsletter?",
 "default": False, # Default razonable
 "required": False
}
```

---

### 3. Validar después de recibir

```python
result = await mcp.elicit(request)

# Validar
if not is_valid_email(result.values.get("email")):
 return {"success": False, "error": {...}}
```

---

### 4. Manejar cancelaciones

```python
result = await mcp.elicit(request)

if result.cancelled:
 return {
 "success": False,
 "error": {
 "code": "CANCELLED",
 "message": "Operación cancelada por el usuario"
 }
 }
```

---

# Checklist de Sampling y Elicitation

---

### Sampling

- [ ] Usar temperatura baja para tareas determinísticas
- [ ] Limitar max_tokens apropiadamente
- [ ] Proporcionar contexto claro en system prompt
- [ ] Manejar errores de conexión
- [ ] Parsear respuestas con try/except

---

### Elicitation

- [ ] Usar para interacciones necesarias
- [ ] Proporcionar defaults sensatos
- [ ] Validar inputs después de recibir
- [ ] Manejar cancelaciones
- [ ] Limitar número de pasos en wizards

---

# Resumen Final

## Los 10 mandamientos del diseño MCP

---

### 1. Claridad ante todo

Las descripciones son tu API. Hazlas claras y completas.

---

### 2. Consistencia en patrones

Usa los mismos nombres, estructuras y convenciones en todas las tools.

---

### 3. Validación exhaustiva

Nunca confíes en la entrada. Valida todo con Pydantic.

---

### 4. Errores informativos

Los errores deben ayudar al modelo a recuperarse.

---

### 5. Seguridad por defecto

Toda entrada es potencialmente maliciosa.

---

### 6. Tokens mínimos

Devuelve solo lo necesario.

---

### 7. Paginación obligatoria

Las listas grandes deben paginarse.

---

### 8. Caché estratégico

Cachea lo que cambia poco.

---

### 9. Logging completo

Registra todo para poder depurar.

---

### 10. Tests exhaustivos

Un servicio sin tests no está completo.

---

# Cierre

---

## Diseño de Servicios MCP: Buenas Prácticas

### De los fundamentos a la implementación profesional

---

**Recursos:**

- Documentación MCP: https://modelcontextprotocol.io/
- FastMCP: https://gofastmcp.com/
- SDK Python: https://github.com/modelcontextprotocol/python-sdk

---

**Próximos pasos:**

1. Diseña tu primer servicio MCP con FastMCP
2. Implementa las validaciones con Pydantic
3. Añade manejo de errores estructurado
4. Escribe tests con pytest
5. Despliega y monitorea

---

**Preguntas y práctica:** ¡Ahora es tu turno!