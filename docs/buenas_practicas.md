# Diseño de Servicios MCP: Buenas Prácticas

## Presentación Extensa para Desarrolladores

---

# Portada

## Diseño de Servicios MCP

### Buenas Prácticas y Patrones de Arquitectura

---

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

```json
{
  "name": "process",
  "description": "Process the input"
}
```

*¿Qué hace? ¿Qué devuelve? ¿Cuándo usarla?*

---

**Buena descripción:**

```json
{
  "name": "processPayment",
  "description": "Procesa un pago con tarjeta. Recibe los datos de la tarjeta y el importe, devuelve el resultado de la transacción con ID de confirmación o mensaje de error."
}
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

**Ejemplo completo:**

```json
{
  "name": "searchUsers",
  "description": "Busca usuarios en el sistema por nombre o email. Devuelve una lista paginada de usuarios que coinciden con el criterio de búsqueda, ordenados por relevancia."
}
```

---

**Elementos:**

- Verbo de acción (busca, crea, elimina, actualiza)
- Objeto afectado (usuarios, pagos, pedidos)
- Parámetros clave (nombre o email)
- Tipo de respuesta (lista paginada)
- Ordenamiento (por relevancia)

---

# Claridad - inputSchema Descriptivo

## Cada campo explicado

---

**Malo:**

```json
{
  "properties": {
    "q": { "type": "string" },
    "n": { "type": "integer" }
  }
}
```

---

**Bueno:**

```json
{
  "properties": {
    "query": {
      "type": "string",
      "description": "Texto a buscar. Puede ser nombre completo, email parcial o nombre de usuario."
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "default": 20,
      "description": "Número máximo de resultados a devolver (1-100)."
    }
  },
  "required": ["query"]
}
```

---

# Claridad - Ejemplos en Descripción

## Cuando el esquema no es suficiente

---

**Añadir ejemplos para casos complejos:**

```json
{
  "name": "scheduleTask",
  "description": "Programa una tarea para ejecutarse en el futuro. El tiempo puede ser absoluto (ISO 8601) o relativo (ej: '5m', '2h', '1d').",
  "inputSchema": {
    "properties": {
      "time": {
        "type": "string",
        "description": "Tiempo de ejecución. Ejemplos: '2026-04-18T15:00:00Z', '30m', '2h', '1d'"
      }
    }
  }
}
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

```json
// Tool 1
{ "name": "getUser", "inputSchema": { "properties": { "userId": "string" } } }

// Tool 2
{ "name": "deleteUser", "inputSchema": { "properties": { "id": "string" } } }

// Tool 3
{ "name": "updateUser", "inputSchema": { "properties": { "user_id": "string" } } }
```

*¿userId, id o user_id?*

---

# Consistencia - Patrón de Nombres

## Nomenclatura estándar

---

**Convenciones recomendadas:**

| Acción | Patrón | Ejemplo |
|--------|--------|---------|
| Leer uno | `get<Entidad>` | `getUser`, `getOrder` |
| Leer varios | `list<Entidad>s` | `listUsers`, `listOrders` |
| Crear | `create<Entidad>` | `createUser`, `createOrder` |
| Actualizar | `update<Entidad>` | `updateUser`, `updateOrder` |
| Eliminar | `delete<Entidad>` | `deleteUser`, `deleteOrder` |
| Buscar | `search<Entidad>s` | `searchUsers`, `searchOrders` |

---

**Para parámetros:**

| Uso | Patrón | Ejemplo |
|-----|--------|---------|
| ID único | `<entidad>Id` | `userId`, `orderId` |
| Límite | `limit` | `limit` |
| Desplazamiento | `offset` | `offset` |
| Filtros | `<campo>Filter` | `statusFilter` |

---

# Consistencia - Estructura de Respuesta

## Respuestas predecibles

---

**Estructura estándar:**

```json
{
  "success": true,
  "data": { ... },
  "metadata": {
    "timestamp": "2026-04-18T15:00:00Z",
    "version": "1.0"
  }
}
```

---

**Para errores:**

```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "Usuario no encontrado",
    "details": {
      "userId": "123",
      "suggestion": "Verifique que el ID sea correcto"
    }
  }
}
```

---

# Consistencia - Paginación

## Patrón estándar para listas

---

**Entrada:**

```json
{
  "properties": {
    "limit": { "type": "integer", "default": 20, "maximum": 100 },
    "offset": { "type": "integer", "default": 0 },
    "cursor": { "type": "string", "description": "Token de paginación del resultado anterior" }
  }
}
```

---

**Salida:**

```json
{
  "success": true,
  "data": {
    "items": [...],
    "total": 150,
    "hasMore": true,
    "nextCursor": "eyJvZmZzZXQiOjIwfQ=="
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

```javascript
async function execute(input) {
  // Validación temprana
  if (!input.userId) {
    return {
      success: false,
      error: {
        code: "MISSING_PARAMETER",
        message: "userId es obligatorio",
        field: "userId"
      }
    };
  }

  if (!input.userId.match(/^usr_[a-zA-Z0-9]+$/)) {
    return {
      success: false,
      error: {
        code: "INVALID_FORMAT",
        message: "userId debe tener formato usr_xxx",
        field: "userId",
        received: input.userId
      }
    };
  }

  // Continuar con la lógica...
}
```

---

# Robustez - Manejo de Excepciones

## Nunca lanzar sin capturar

---

**Incorrecto:**

```javascript
async function execute(input) {
  const user = await db.getUser(input.userId);  // Puede lanzar
  return { success: true, data: user };
}
```

---

**Correcto:**

```javascript
async function execute(input) {
  try {
    const user = await db.getUser(input.userId);
    
    if (!user) {
      return {
        success: false,
        error: {
          code: "USER_NOT_FOUND",
          message: `Usuario ${input.userId} no encontrado`
        }
      };
    }
    
    return { success: true, data: user };
    
  } catch (dbError) {
    logger.error("Database error", { error: dbError, userId: input.userId });
    
    return {
      success: false,
      error: {
        code: "INTERNAL_ERROR",
        message: "Error interno. Por favor, inténtelo más tarde.",
        requestId: generateRequestId()
      }
    };
  }
}
```

---

# Robustez - Errores con Sugerencias

## Ayudar al modelo a recuperarse

---

**Error sin sugerencia:**

```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "No hay suficiente stock"
  }
}
```

---

**Error con sugerencia:**

```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "No hay suficiente stock del producto",
    "details": {
      "requested": 10,
      "available": 3,
      "suggestion": "Puede añadir 3 unidades ahora o esperar a que se reponga el stock"
    }
  }
}
```

---

**El modelo puede usar la sugerencia para proponer alternativas.**

---

# PARTE 2: ARQUITECTURA

---

# Arquitectura de un Servidor MCP

## Componentes principales

---

```
┌─────────────────────────────────────────────────┐
│                  MCP SERVER                      │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │   Router    │  │  Validator  │  │  Logger  │ │
│  └─────────────┘  └─────────────┘  └──────────┘ │
│                                                  │
│  ┌─────────────────────────────────────────────┐│
│  │              Tool Registry                   ││
│  │  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐   ││
│  │  │ Tool  │ │ Tool  │ │ Tool  │ │ Tool  │   ││
│  │  │   A   │ │   B   │ │   C   │ │   D   │   ││
│  │  └───────┘ └───────┘ └───────┘ └───────┘   ││
│  └─────────────────────────────────────────────┘│
│                                                  │
│  ┌─────────────────────────────────────────────┐│
│  │           Resource Registry                  ││
│  └─────────────────────────────────────────────┘│
│                                                  │
│  ┌─────────────────────────────────────────────┐│
│  │           Prompt Registry                    ││
│  └─────────────────────────────────────────────┘│
│                                                  │
├─────────────────────────────────────────────────┤
│              Transport Layer                     │
│         (STDIO / HTTP / WebSocket)              │
└─────────────────────────────────────────────────┘
```

---

# Transport Layer

## Opciones y consideraciones

---

### STDIO

**Uso:** Herramientas locales, CLIs

**Ventajas:**
- Simplicidad
- Sin configuración de red
- Ideal para desarrollo

**Desventajas:**
- Solo un cliente por proceso
- No apto para producción multi-cliente

---

### HTTP + SSE

**Uso:** Servicios remotos, producción

**Ventajas:**
- Múltiples clientes
- Depuración sencilla
- Compatible con proxies

**Desventajas:**
- Requiere servidor HTTP
- Más complejo

---

### WebSocket

**Uso:** Tiempo real, bidireccional

**Ventajas:**
- Comunicación bidireccional
- Menor latencia
- Ideal para notificaciones

**Desventajas:**
- Más complejo de implementar
- Requiere keepalive

---

# Patrón de Registro

## Cómo organizar las tools

---

**Opción 1: Registro directo**

```javascript
server.addTool({
  name: "getUser",
  // ... definición
});

server.addTool({
  name: "createUser",
  // ... definición
});
```

---

**Opción 2: Módulos organizados**

```javascript
// tools/users.js
export const userTools = [
  { name: "getUser", ... },
  { name: "createUser", ... },
  { name: "updateUser", ... },
  { name: "deleteUser", ... },
  { name: "listUsers", ... }
];

// tools/orders.js
export const orderTools = [
  { name: "getOrder", ... },
  { name: "createOrder", ... },
  // ...
];

// server.js
import { userTools } from "./tools/users.js";
import { orderTools } from "./tools/orders.js";

[...userTools, ...orderTools].forEach(tool => server.addTool(tool));
```

---

# Patrón de Validación

## Centralizar la lógica de validación

---

**Validador reutilizable:**

```javascript
// validators/common.js
export const validators = {
  required: (field, value) => {
    if (!value) {
      return { valid: false, error: `${field} es obligatorio` };
    }
    return { valid: true };
  },
  
  pattern: (field, value, regex, message) => {
    if (!regex.test(value)) {
      return { valid: false, error: message };
    }
    return { valid: true };
  },
  
  range: (field, value, min, max) => {
    if (value < min || value > max) {
      return { valid: false, error: `${field} debe estar entre ${min} y ${max}` };
    }
    return { valid: true };
  }
};
```

---

**Uso en tool:**

```javascript
import { validators } from "./validators/common.js";

async function execute(input) {
  // Validación
  const validations = [
    validators.required("userId", input.userId),
    validators.pattern("userId", input.userId, /^usr_/, "userId debe empezar por usr_"),
    validators.range("limit", input.limit, 1, 100)
  ];
  
  for (const v of validations) {
    if (!v.valid) {
      return { success: false, error: { code: "VALIDATION_ERROR", message: v.error } };
    }
  }
  
  // Procesar...
}
```

---

# Patrón de Error Handler

## Centralizar manejo de errores

---

```javascript
// errors/index.js
export class MCPError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.code = code;
    this.details = details;
  }
}

export const Errors = {
  NOT_FOUND: (resource, id) => new MCPError(
    "NOT_FOUND",
    `${resource} no encontrado`,
    { resource, id }
  ),
  
  INVALID_INPUT: (field, reason) => new MCPError(
    "INVALID_INPUT",
    `Campo ${field} inválido: ${reason}`,
    { field, reason }
  ),
  
  UNAUTHORIZED: (action) => new MCPError(
    "UNAUTHORIZED",
    `No autorizado para ${action}`,
    { action }
  ),
  
  INTERNAL: (requestId) => new MCPError(
    "INTERNAL_ERROR",
    "Error interno",
    { requestId }
  )
};

// Helper para convertir a respuesta
export const toErrorResponse = (error) => {
  if (error instanceof MCPError) {
    return {
      success: false,
      error: {
        code: error.code,
        message: error.message,
        details: error.details
      }
    };
  }
  return {
    success: false,
    error: {
      code: "INTERNAL_ERROR",
      message: "Error inesperado"
    }
  };
};
```

---

# Patrón de Error Handler - Uso

---

```javascript
import { Errors, toErrorResponse } from "./errors/index.js";

async function execute(input) {
  try {
    // Validar
    if (!input.userId) {
      throw Errors.INVALID_INPUT("userId", "es obligatorio");
    }
    
    // Buscar
    const user = await db.getUser(input.userId);
    if (!user) {
      throw Errors.NOT_FOUND("Usuario", input.userId);
    }
    
    // Autorizar
    if (!user.canAccess(input.resource)) {
      throw Errors.UNAUTHORIZED("acceder a este recurso");
    }
    
    return { success: true, data: user };
    
  } catch (error) {
    logger.error("Tool execution failed", { error, input });
    return toErrorResponse(error);
  }
}
```

---

# Patrón de Caché

## Optimizar lecturas frecuentes

---

```javascript
// cache/index.js
export class SimpleCache {
  constructor(ttlMs = 60000) {
    this.cache = new Map();
    this.ttl = ttlMs;
  }
  
  get(key) {
    const entry = this.cache.get(key);
    if (!entry) return null;
    
    if (Date.now() > entry.expires) {
      this.cache.delete(key);
      return null;
    }
    
    return entry.value;
  }
  
  set(key, value) {
    this.cache.set(key, {
      value,
      expires: Date.now() + this.ttl
    });
  }
  
  invalidate(pattern) {
    for (const key of this.cache.keys()) {
      if (key.includes(pattern)) {
        this.cache.delete(key);
      }
    }
  }
}
```

---

# Patrón de Caché - Uso

---

```javascript
const cache = new SimpleCache(5 * 60 * 1000); // 5 minutos

async function execute(input) {
  const cacheKey = `user:${input.userId}`;
  
  // Intentar caché
  const cached = cache.get(cacheKey);
  if (cached) {
    return { success: true, data: cached, fromCache: true };
  }
  
  // Buscar en DB
  const user = await db.getUser(input.userId);
  
  if (!user) {
    return { success: false, error: { code: "NOT_FOUND" } };
  }
  
  // Guardar en caché
  cache.set(cacheKey, user);
  
  return { success: true, data: user, fromCache: false };
}
```

---

# Patrón de Rate Limiting

## Proteger el servicio

---

```javascript
// ratelimit/index.js
export class RateLimiter {
  constructor(maxRequests = 100, windowMs = 60000) {
    this.limits = new Map();
    this.max = maxRequests;
    this.window = windowMs;
  }
  
  check(identifier) {
    const now = Date.now();
    const entry = this.limits.get(identifier);
    
    if (!entry) {
      this.limits.set(identifier, { count: 1, resetAt: now + this.window });
      return { allowed: true, remaining: this.max - 1 };
    }
    
    if (now > entry.resetAt) {
      entry.count = 1;
      entry.resetAt = now + this.window;
      return { allowed: true, remaining: this.max - 1 };
    }
    
    if (entry.count >= this.max) {
      return { 
        allowed: false, 
        remaining: 0,
        resetAt: entry.resetAt 
      };
    }
    
    entry.count++;
    return { allowed: true, remaining: this.max - entry.count };
  }
}
```

---

# Patrón de Rate Limiting - Uso

---

```javascript
const limiter = new RateLimiter(50, 60000); // 50 peticiones/min

server.addTool({
  name: "searchUsers",
  inputSchema: { ... },
  execute: async (input, context) => {
    // Obtener identificador (usuario o IP)
    const identifier = context.user?.id || context.clientIp;
    
    // Verificar rate limit
    const limit = limiter.check(identifier);
    
    if (!limit.allowed) {
      return {
        success: false,
        error: {
          code: "RATE_LIMIT_EXCEEDED",
          message: "Demasiadas peticiones. Inténtelo más tarde.",
          retryAfter: Math.ceil((limit.resetAt - Date.now()) / 1000)
        }
      };
    }
    
    // Procesar normalmente
    const users = await searchUsers(input);
    
    return {
      success: true,
      data: users,
      rateLimit: { remaining: limit.remaining }
    };
  }
});
```

---

# PARTE 3: DISEÑO DE TOOLS

---

# Anatomía de una Tool

## Estructura completa

---

```javascript
{
  name: "string",           // Identificador único
  description: "string",    // Explicación para la IA
  inputSchema: {            // JSON Schema
    type: "object",
    properties: { ... },
    required: [ ... ]
  },
  outputSchema: { ... },    // Opcional pero recomendado
  annotations: {            // Metadatos
    readOnlyHint: boolean,
    destructiveHint: boolean,
    idempotentHint: boolean,
    openWorldHint: boolean
  },
  execute: async (input, context) => {
    // Lógica de la herramienta
  }
}
```

---

# Convenciones de Nombres

## Nombres descriptivos y consistentes

---

### Verbos de Acción

| Verbo | Significado | Ejemplo |
|-------|-------------|---------|
| `get` | Obtener un recurso por ID | `getUser` |
| `list` | Obtener múltiples recursos | `listUsers` |
| `search` | Búsqueda por criterios | `searchUsers` |
| `create` | Crear nuevo recurso | `createUser` |
| `update` | Modificar recurso existente | `updateUser` |
| `delete` | Eliminar recurso | `deleteUser` |

---

### Evitar

| Malo | Por qué | Mejor |
|------|---------|-------|
| `process` | Vago | `processPayment` |
| `handle` | Vago | `handleWebhook` |
| `do` | Sin significado | `executeTask` |
| `run` | Ambiguo | `runReport` |
| `manage` | Demasiado amplio | `createUser`, `updateUser`, etc. |

---

# Descripción Efectiva

## La descripción es tu API

---

**Fórmula de descripción completa:**

```
[VERBO] [RECURSO]. [QUÉ HACE]. [PARÁMETROS CLAVE]. [RETORNO]. [EFECTOS].
```

---

**Ejemplo paso a paso:**

1. Verbo: "Elimina"
2. Recurso: "un usuario"
3. Qué hace: "del sistema permanentemente"
4. Parámetros: "Requiere el ID del usuario"
5. Retorno: "Devuelve confirmación o error si no existe"
6. Efectos: "Esta acción es irreversible"

---

**Resultado:**

```json
{
  "name": "deleteUser",
  "description": "Elimina un usuario del sistema permanentemente. Requiere el ID del usuario. Devuelve confirmación de eliminación o error si el usuario no existe. Esta acción es irreversible y no se puede deshacer.",
  "annotations": { "destructiveHint": true }
}
```

---

# inputSchema Detallado

## Validación y documentación

---

### Tipos de datos comunes

```javascript
// String con restricciones
{
  "type": "string",
  "minLength": 1,
  "maxLength": 100,
  "pattern": "^[a-zA-Z0-9_]+$",
  "description": "Nombre de usuario (solo alfanumérico y _)"
}

// Entero con rango
{
  "type": "integer",
  "minimum": 1,
  "maximum": 100,
  "default": 20,
  "description": "Número de resultados (1-100)"
}

// Enum
{
  "type": "string",
  "enum": ["pending", "active", "completed", "cancelled"],
  "description": "Estado del pedido"
}

// Fecha
{
  "type": "string",
  "format": "date-time",
  "description": "Fecha en formato ISO 8601"
}
```

---

# inputSchema - Objetos Anidados

---

```javascript
{
  "type": "object",
  "properties": {
    "user": {
      "type": "object",
      "description": "Datos del usuario a crear",
      "properties": {
        "name": {
          "type": "string",
          "minLength": 2,
          "maxLength": 100
        },
        "email": {
          "type": "string",
          "format": "email"
        },
        "role": {
          "type": "string",
          "enum": ["admin", "user", "guest"]
        }
      },
      "required": ["name", "email"]
    },
    "sendNotification": {
      "type": "boolean",
      "default": true,
      "description": "Enviar email de bienvenida"
    }
  },
  "required": ["user"]
}
```

---

# inputSchema - Arrays

---

```javascript
{
  "type": "object",
  "properties": {
    "userIds": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^usr_[a-zA-Z0-9]+$"
      },
      "minItems": 1,
      "maxItems": 50,
      "description": "Lista de IDs de usuarios (1-50)"
    },
    "options": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "key": { "type": "string" },
          "value": { "type": "string" }
        },
        "required": ["key", "value"]
      },
      "description": "Opciones adicionales como pares clave-valor"
    }
  },
  "required": ["userIds"]
}
```

---

# inputSchema - Condicionales

## Lógica compleja con JSON Schema

---

```javascript
{
  "type": "object",
  "properties": {
    "type": {
      "type": "string",
      "enum": ["email", "sms", "push"]
    },
    "recipient": { "type": "string" },
    "message": { "type": "string" }
  },
  "required": ["type", "recipient", "message"],
  "allOf": [
    {
      "if": { "properties": { "type": { "const": "email" } } },
      "then": {
        "properties": {
          "recipient": { "format": "email" }
        }
      }
    },
    {
      "if": { "properties": { "type": { "const": "sms" } } },
      "then": {
        "properties": {
          "recipient": { "pattern": "^\\+?[0-9]{10,15}$" }
        }
      }
    }
  ]
}
```

---

# outputSchema

## Documentar lo que devuelve

---

**¿Por qué outputSchema?**

- Permite al modelo entender la estructura de respuesta
- Facilita testing automatizado
- Mejora la depuración
- Herramientas pueden generar interfaces

---

```javascript
{
  "name": "getUser",
  "inputSchema": { ... },
  "outputSchema": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "data": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "email": { "type": "string" },
          "createdAt": { "type": "string", "format": "date-time" }
        }
      },
      "error": {
        "type": "object",
        "properties": {
          "code": { "type": "string" },
          "message": { "type": "string" }
        }
      }
    }
  }
}
```

---

# Annotations

## Metadatos importantes

---

### readOnlyHint

`true` si la tool no modifica estado.

```json
{ "name": "getUser", "annotations": { "readOnlyHint": true } }
```

**Uso:** Los clientes pueden ejecutar tools de solo lectura sin confirmación.

---

### destructiveHint

`true` si la tool tiene efectos destructivos irreversibles.

```json
{ "name": "deleteUser", "annotations": { "destructiveHint": true } }
```

**Uso:** Los clientes deben mostrar confirmación explícita.

---

### idempotentHint

`true` si llamar múltiples veces tiene el mismo efecto que una vez.

```json
{ "name": "setConfig", "annotations": { "idempotentHint": true } }
```

**Uso:** Los clientes pueden reintentar automáticamente.

---

### openWorldHint

`true` si la tool interactúa con sistemas externos.

```json
{ "name": "sendEmail", "annotations": { "openWorldHint": true } }
```

**Uso:** Los clientes deben considerar implicaciones de privacidad.

---

# Tool: Lectura vs Escritura

## Diferencias de diseño

---

### Read Tools (readOnlyHint: true)

**Características:**
- No modifican datos
- Seguras de ejecutar sin confirmación
- Pueden ser cacheadas
- Pueden ser paralelizadas

**Consideraciones:**
- Incluir paginación para listas grandes
- Documentar filtros disponibles
- Devolver solo datos necesarios (minimizar tokens)

---

### Write Tools (readOnlyHint: false)

**Características:**
- Modifican estado
- Requieren consideración del usuario
- No cacheables
- Deben ser serializadas si dependientes

**Consideraciones:**
- Incluir validación completa
- Devolver el estado resultante
- Documentar efectos secundarios
- Considerar idempotencia

---

# Idempotencia

## Diseñar para reintentos

---

**Principio:**

Una operación es idempotente si ejecutarla múltiples veces tiene el mismo efecto que ejecutarla una vez.

---

**¿Por qué importa?**

- Los clientes pueden reintentar errores de red
- El usuario puede hacer clic dos veces
- Sistemas distribuidos pueden duplicar mensajes

---

# Idempotencia - Patrón con ID

---

```javascript
{
  name: "createOrder",
  inputSchema: {
    properties: {
      idempotencyKey: {
        type: "string",
        description: "Clave única para evitar duplicados. Genere un UUID para cada operación nueva."
      },
      items: {
        type: "array",
        items: { ... }
      }
    },
    required: ["idempotencyKey", "items"]
  },
  annotations: { "idempotentHint": true },
  execute: async (input) => {
    // Verificar si ya existe
    const existing = await db.getOrderByKey(input.idempotencyKey);
    if (existing) {
      return { success: true, data: existing, idempotent: true };
    }
    
    // Crear nuevo
    const order = await db.createOrder(input);
    return { success: true, data: order, idempotent: false };
  }
}
```

---

# Paginación

## Manejar grandes conjuntos de datos

---

**Problema:**

Devolver 10.000 usuarios consume demasiados tokens y tiempo.

---

**Solución:**

Paginación con cursor o desplazamiento.

---

### Paginación por Desplazamiento

```javascript
{
  name: "listUsers",
  inputSchema: {
    properties: {
      limit: { type: "integer", minimum: 1, maximum: 100, default: 20 },
      offset: { type: "integer", minimum: 0, default: 0 }
    }
  },
  execute: async (input) => {
    const users = await db.getUsers(input.limit, input.offset);
    const total = await db.countUsers();
    
    return {
      success: true,
      data: {
        items: users,
        total,
        hasMore: (input.offset + input.limit) < total
      }
    };
  }
}
```

---

### Paginación por Cursor

```javascript
{
  name: "listUsers",
  inputSchema: {
    properties: {
      limit: { type: "integer", default: 20 },
      cursor: { type: "string", description: "Token de la página anterior" }
    }
  },
  execute: async (input) => {
    const decodedCursor = input.cursor 
      ? JSON.parse(Buffer.from(input.cursor, 'base64').toString())
      : { lastId: null };
    
    const users = await db.getUsersAfter(decodedCursor.lastId, input.limit);
    
    const nextCursor = users.length === input.limit
      ? Buffer.from(JSON.stringify({ lastId: users[users.length - 1].id })).toString('base64')
      : null;
    
    return {
      success: true,
      data: {
        items: users,
        nextCursor
      }
    };
  }
}
```

---

# Filtrado y Búsqueda

## Encontrar lo que se necesita

---

### Patrón de Filtros

```javascript
{
  name: "searchOrders",
  inputSchema: {
    properties: {
      query: { type: "string", description: "Texto a buscar" },
      status: {
        type: "array",
        items: { "enum": ["pending", "processing", "shipped", "delivered", "cancelled"] },
        description: "Filtrar por estados (puede ser múltiple)"
      },
      dateFrom: { type: "string", "format": "date-time" },
      dateTo: { type: "string", "format": "date-time" },
      minAmount: { type: "number", minimum: 0 },
      maxAmount: { type: "number", minimum: 0 },
      sortBy: { "enum": ["date", "amount", "status"] },
      sortOrder: { "enum": ["asc", "desc"] }
    }
  }
}
```

---

### Validación de Filtros

```javascript
execute: async (input) => {
  // Validar rangos
  if (input.minAmount && input.maxAmount && input.minAmount > input.maxAmount) {
    return {
      success: false,
      error: {
        code: "INVALID_RANGE",
        message: "minAmount no puede ser mayor que maxAmount"
      }
    };
  }
  
  if (input.dateFrom && input.dateTo && new Date(input.dateFrom) > new Date(input.dateTo)) {
    return {
      success: false,
      error: {
        code: "INVALID_RANGE",
        message: "dateFrom no puede ser posterior a dateTo"
      }
    };
  }
  
  // Construir query
  const filters = {};
  if (input.status) filters.status = { $in: input.status };
  if (input.minAmount) filters.amount = { $gte: input.minAmount };
  // ...
  
  return await searchOrders(filters, input);
}
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

# Tipos de Resources

## Categorización por contenido

---

### Estáticos

Contenido que no cambia frecuentemente.

- Documentación
- Configuración del sistema
- Esquemas de base de datos
- Versiones de API

---

### Dinámicos

Contenido que cambia con el tiempo.

- Estado actual del sistema
- Logs recientes
- Métricas en vivo
- Contenido del usuario

---

### Generados

Contenido creado bajo demanda.

- Informes
- Resúmenes
- Análisis
- Consultas complejas

---

# Resource URIs

## Identificación única

---

### Esquemas comunes

```
file:///path/to/file           - Archivos locales
postgres://host/db/table       - Tablas de base de datos
https://api.example.com/data   - APIs externas
memory://cache/key            - Memoria caché
app://internal/resource       - Recursos internos
```

---

### URI Templates

Permiten parámetros en la URI.

```
users://{userId}/profile
repos://{owner}/{repo}/issues
logs://{service}/{date}
```

---

# Definición de Resource

## Estructura completa

---

```javascript
{
  uri: "users://{userId}/profile",
  name: "Perfil de Usuario",
  description: "Información del perfil del usuario solicitado",
  mimeType: "application/json",
  template: {
    parameters: {
      userId: {
        type: "string",
        description: "ID del usuario",
        pattern: "^usr_[a-zA-Z0-9]+$"
      }
    }
  }
}
```

---

# Resource Handlers

## Lectura de recursos

---

```javascript
server.addResource({
  uri: "users://{userId}/profile",
  name: "Perfil de Usuario",
  description: "Información del perfil del usuario",
  mimeType: "application/json",
  
  read: async (uri, params, context) => {
    const { userId } = params;
    
    // Validar acceso
    if (!context.user || context.user.id !== userId) {
      throw new Error("UNAUTHORIZED");
    }
    
    // Obtener datos
    const user = await db.getUser(userId);
    
    if (!user) {
      throw new Error("NOT_FOUND");
    }
    
    // Devolver contenido
    return {
      contents: [{
        uri: `users://${userId}/profile`,
        mimeType: "application/json",
        text: JSON.stringify({
          id: user.id,
          name: user.name,
          email: user.email,
          createdAt: user.createdAt
        })
      }]
    };
  }
});
```

---

# Resource Subscriptions

## Actualizaciones en tiempo real

---

**Problema:**

El modelo lee un resource pero los datos pueden cambiar.

---

**Solución:**

Permitir suscripciones a cambios.

---

```javascript
server.addResource({
  uri: "logs://system/live",
  name: "Logs del Sistema",
  description: "Logs en tiempo real",
  mimeType: "text/plain",
  
  read: async (uri) => {
    return {
      contents: [{
        uri,
        mimeType: "text/plain",
        text: await getRecentLogs(100)
      }]
    };
  },
  
  subscribe: async (uri, context) => {
    // Enviar actualizaciones cuando hay nuevos logs
    const interval = setInterval(async () => {
      const newLogs = await getNewLogs();
      if (newLogs.length > 0) {
        context.send({
          uri,
          contents: [{
            uri,
            mimeType: "text/plain",
            text: newLogs.join('\n')
          }]
        });
      }
    }, 1000);
    
    return { unsubscribe: () => clearInterval(interval) };
  }
});
```

---

# Resource Caching

## Optimizar lecturas frecuentes

---

```javascript
const resourceCache = new Map();

server.addResource({
  uri: "config://app/settings",
  name: "Configuración de la Aplicación",
  
  read: async (uri) => {
    // Verificar caché
    const cached = resourceCache.get(uri);
    if (cached && Date.now() - cached.timestamp < 60000) {
      return cached.data;
    }
    
    // Obtener fresco
    const settings = await db.getSettings();
    const data = {
      contents: [{
        uri,
        mimeType: "application/json",
        text: JSON.stringify(settings)
      }]
    };
    
    // Guardar en caché
    resourceCache.set(uri, {
      data,
      timestamp: Date.now()
    });
    
    return data;
  }
});
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

```javascript
// Resources - para lectura de contexto
server.addResource({
  uri: "docs://{docId}",
  name: "Documento",
  read: async (uri, params) => {
    const doc = await getDocument(params.docId);
    return { contents: [{ uri, text: doc.content }] };
  }
});

// Tools - para acciones
server.addTool({
  name: "createDocument",
  inputSchema: { ... },
  execute: async (input) => {
    const doc = await createDocument(input);
    return { success: true, data: doc };
  }
});

server.addTool({
  name: "updateDocument",
  inputSchema: { ... },
  execute: async (input) => {
    const doc = await updateDocument(input);
    return { success: true, data: doc };
  }
});
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

# Definición de Prompt

## Estructura completa

---

```javascript
{
  name: "code-review",
  description: "Revisa código fuente buscando errores y mejoras",
  arguments: [
    {
      name: "language",
      description: "Lenguaje de programación",
      required: true
    },
    {
      name: "focus",
      description: "Área de enfoque (security, performance, style)",
      required: false
    }
  ],
  messages: [
    {
      role: "user",
      content: {
        type: "text",
        text: "Por favor, revisa el siguiente código {{language}}:\n\n{{code}}"
      }
    }
  ]
}
```

---

# Prompt Templates

## Parametrización

---

### Sintaxis de Template

```
{{parametro}}       - Valor del argumento
{{?parametro}}      - Condicional (solo si existe)
{{param:default}}    - Con valor por defecto
```

---

### Ejemplo Completo

```javascript
{
  name: "analyze-data",
  description: "Analiza datos y genera insights",
  arguments: [
    { name: "dataType", description: "Tipo de datos", required: true },
    { name: "depth", description: "Profundidad del análisis (basic, detailed)", required: false },
    { name: "format", description: "Formato de salida", required: false }
  ],
  messages: [
    {
      role: "system",
      content: {
        type: "text",
        text: "Eres un analista de datos experto. Tu especialidad es {{dataType}}."
      }
    },
    {
      role: "user",
      content: {
        type: "text",
        text: "Analiza los siguientes datos con profundidad {{depth:basic}}.{{?format}} Presenta los resultados en formato {{format}}.{{/format}}\n\n{{data}}"
      }
    }
  ]
}
```

---

# Prompts con Resources

## Composición

---

```javascript
{
  name: "analyze-repository",
  description: "Analiza un repositorio de código",
  arguments: [
    { name: "repo", description: "URL del repositorio", required: true },
    { name: "branch", description: "Rama a analizar", required: false }
  ],
  resources: [
    {
      uri: "repo://{{repo}}/structure",
      description: "Estructura del repositorio"
    },
    {
      uri: "repo://{{repo}}/{{branch:main}}/readme",
      description: "README del repositorio"
    }
  ],
  messages: [
    {
      role: "system",
      content: {
        type: "text",
        text: "Eres un arquitecto de software. Analiza el repositorio y proporciona recomendaciones."
      }
    },
    {
      role: "user",
      content: {
        type: "text",
        text: "Analiza el repositorio {{repo}} y proporciona:\n1. Resumen de arquitectura\n2. Tecnologías utilizadas\n3. Calidad del código\n4. Recomendaciones"
      }
    }
  ]
}
```

---

# Prompts Especializados

## Modos de operación

---

### Modo Experto

```javascript
{
  name: "security-audit",
  description: "Auditoría de seguridad de código",
  arguments: [
    { name: "severity", description: "Nivel mínimo de severidad (low, medium, high, critical)", required: false }
  ],
  messages: [
    {
      role: "system",
      content: {
        type: "text",
        text: "Eres un experto en seguridad informática con 20 años de experiencia. Tu especialidad es identificar vulnerabilidades en código. Para cada problema encontrado, indica:\n- Tipo de vulnerabilidad (OWASP Top 10)\n- Severidad (low, medium, high, critical)\n- Ubicación exacta\n- Recomendación de corrección\n- Referencias a CVEs si aplica"
      }
    }
  ]
}
```

---

### Modo Flujo de Trabajo

```javascript
{
  name: "deployment-workflow",
  description: "Guía el proceso de despliegue",
  arguments: [],
  messages: [
    {
      role: "system",
      content: {
        type: "text",
        text: "Eres un ingeniero DevOps. Guía al usuario a través del proceso de despliegue paso a paso. No pases al siguiente paso hasta que el usuario confirme que el paso anterior está completo."
      }
    },
    {
      role: "user",
      content: {
        type: "text",
        text: "Necesito hacer el despliegue de una aplicación Node.js a AWS. ¿Por dónde empiezo?"
      }
    }
  ]
}
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

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "El campo 'email' no tiene un formato válido",
    "details": {
      "field": "email",
      "value": "not-an-email",
      "expected": "Formato: usuario@dominio.com"
    },
    "suggestion": "Verifique el formato del email e inténtelo de nuevo",
    "requestId": "req_abc123"
  }
}
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

```javascript
async function execute(input) {
  const errors = [];
  
  // Validar campos obligatorios
  if (!input.email) {
    errors.push({
      field: "email",
      code: "MISSING_PARAMETER",
      message: "email es obligatorio"
    });
  }
  
  // Validar formato
  if (input.email && !isValidEmail(input.email)) {
    errors.push({
      field: "email",
      code: "INVALID_FORMAT",
      message: "email no tiene un formato válido",
      value: input.email,
      expected: "usuario@dominio.com"
    });
  }
  
  // Validar rango
  if (input.age && (input.age < 0 || input.age > 150)) {
    errors.push({
      field: "age",
      code: "OUT_OF_RANGE",
      message: "age debe estar entre 0 y 150",
      value: input.age,
      min: 0,
      max: 150
    });
  }
  
  if (errors.length > 0) {
    return {
      success: false,
      error: {
        code: "VALIDATION_ERROR",
        message: "Se encontraron errores de validación",
        details: errors
      }
    };
  }
  
  // Procesar...
}
```

---

# Errores de Autorización

## Permisos insuficientes

---

```javascript
async function execute(input, context) {
  // Verificar autenticación
  if (!context.user) {
    return {
      success: false,
      error: {
        code: "UNAUTHORIZED",
        message: "Se requiere autenticación para esta operación",
        suggestion: "Inicie sesión y vuelva a intentarlo"
      }
    };
  }
  
  // Verificar permisos específicos
  if (!context.user.permissions.includes("users:delete")) {
    return {
      success: false,
      error: {
        code: "FORBIDDEN",
        message: "No tiene permisos para eliminar usuarios",
        requiredPermission: "users:delete",
        currentPermissions: context.user.permissions,
        suggestion: "Contacte con el administrador para obtener el permiso necesario"
      }
    };
  }
  
  // Verificar ownership
  if (input.userId !== context.user.id && !context.user.isAdmin) {
    return {
      success: false,
      error: {
        code: "FORBIDDEN",
        message: "Solo puede eliminar su propio usuario",
        suggestion: "Especifique su propio ID de usuario"
      }
    };
  }
  
  // Procesar...
}
```

---

# Errores de Recurso

## No encontrado o ya existe

---

### Not Found

```javascript
async function execute(input) {
  const user = await db.getUser(input.userId);
  
  if (!user) {
    return {
      success: false,
      error: {
        code: "NOT_FOUND",
        message: `Usuario ${input.userId} no encontrado`,
        resource: "user",
        identifier: input.userId,
        suggestion: "Verifique que el ID sea correcto o use listUsers para ver usuarios disponibles"
      }
    };
  }
  
  // Procesar...
}
```

---

### Already Exists

```javascript
async function execute(input) {
  const existing = await db.getUserByEmail(input.email);
  
  if (existing) {
    return {
      success: false,
      error: {
        code: "ALREADY_EXISTS",
        message: `Ya existe un usuario con el email ${input.email}`,
        resource: "user",
        identifier: input.email,
        existingId: existing.id,
        suggestion: "Use un email diferente o recupere su cuenta existente"
      }
    };
  }
  
  // Crear nuevo...
}
```

---

# Errores de Conflicto

## Estado inconsistente

---

```javascript
async function execute(input) {
  const order = await db.getOrder(input.orderId);
  
  // Verificar estado
  if (order.status === "cancelled") {
    return {
      success: false,
      error: {
        code: "CONFLICT",
        message: "No se puede modificar un pedido cancelado",
        currentState: order.status,
        attemptedAction: "update",
        suggestion: "Cree un nuevo pedido si necesita realizar cambios"
      }
    };
  }
  
  if (order.status !== "pending") {
    return {
      success: false,
      error: {
        code: "PRECONDITION_FAILED",
        message: "El pedido ya fue procesado",
        currentState: order.status,
        expectedState: "pending",
        suggestion: "Use getOrder para ver el estado actual del pedido"
      }
    };
  }
  
  // Procesar...
}
```

---

# Errores de Límites

## Rate limit y cuotas

---

```javascript
const rateLimiter = new RateLimiter(100, 60000); // 100/min

async function execute(input, context) {
  const identifier = context.user?.id || context.ip;
  const limit = rateLimiter.check(identifier);
  
  if (!limit.allowed) {
    return {
      success: false,
      error: {
        code: "RATE_LIMIT_EXCEEDED",
        message: "Ha excedido el límite de peticiones",
        limit: 100,
        window: "1 minuto",
        retryAfter: Math.ceil((limit.resetAt - Date.now()) / 1000),
        suggestion: "Espere antes de realizar más peticiones"
      }
    };
  }
  
  // Verificar cuota
  const quota = await checkQuota(context.user);
  if (quota.used >= quota.limit) {
    return {
      success: false,
      error: {
        code: "QUOTA_EXCEEDED",
        message: "Ha excedido su cuota mensual",
        quotaUsed: quota.used,
        quotaLimit: quota.limit,
        quotaReset: quota.resetDate,
        suggestion: "Actualice su plan o espere al próximo período"
      }
    };
  }
  
  // Procesar...
}
```

---

# Errores Internos

## Registrar sin exponer

---

```javascript
async function execute(input, context) {
  const requestId = generateRequestId();
  
  try {
    // Operación
    const result = await someOperation(input);
    return { success: true, data: result };
    
  } catch (error) {
    // Registrar con detalle
    logger.error("Internal error in execute", {
      requestId,
      error: error.message,
      stack: error.stack,
      input: sanitizeForLog(input),
      context: {
        user: context.user?.id,
        ip: context.ip
      }
    });
    
    // Devolver error genérico
    return {
      success: false,
      error: {
        code: "INTERNAL_ERROR",
        message: "Ocurrió un error interno. Por favor, inténtelo más tarde.",
        requestId,
        suggestion: "Si el problema persiste, contacte con soporte con el ID de solicitud"
      }
    };
  }
}
```

---

# Recuperación de Errores

## El modelo puede reintentar

---

**Información para recuperación:**

```json
{
  "success": false,
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "El servicio de pagos no está disponible",
    "retryable": true,
    "retryAfter": 30,
    "alternativeActions": [
      {
        "action": "retry",
        "description": "Reintentar en 30 segundos"
      },
      {
        "action": "useFallback",
        "tool": "createOfflineOrder",
        "description": "Crear pedido pendiente de pago"
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

**Problema:**

El modelo puede enviar datos maliciosos o inesperados.

---

**Solución:**

Validación exhaustiva en cada tool.

---

```javascript
// Nunca confiar en el modelo
async function execute(input) {
  // ❌ Malo: usar directamente
  // const user = await db.query(`SELECT * FROM users WHERE id = '${input.userId}'`);
  
  // ✅ Bueno: validar primero
  if (!input.userId.match(/^usr_[a-zA-Z0-9]+$/)) {
    return {
      success: false,
      error: {
        code: "INVALID_INPUT",
        message: "userId tiene un formato inválido"
      }
    };
  }
  
  // ✅ Mejor: usar parámetros
  const user = await db.query(
    "SELECT * FROM users WHERE id = $1",
    [input.userId]
  );
}
```

---

# SQL Injection

## Peligro clásico

---

**Entrada maliciosa:**

```json
{
  "userId": "usr_123' OR '1'='1"
}
```

---

**Consulta vulnerable:**

```javascript
const query = `SELECT * FROM users WHERE id = '${input.userId}'`;
// SELECT * FROM users WHERE id = 'usr_123' OR '1'='1'
```

---

**Consulta segura:**

```javascript
const query = "SELECT * FROM users WHERE id = $1";
const result = await db.query(query, [input.userId]);
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

```javascript
async function execute(input) {
  const content = await fs.readFile(`./files/${input.filename}`);
  return { success: true, data: content };
}
```

---

**Código seguro:**

```javascript
import path from 'path';

async function execute(input) {
  // Normalizar ruta
  const basePath = path.resolve('./files');
  const filePath = path.resolve('./files', input.filename);
  
  // Verificar que está dentro del directorio permitido
  if (!filePath.startsWith(basePath)) {
    return {
      success: false,
      error: {
        code: "FORBIDDEN",
        message: "Acceso denegado al archivo"
      }
    };
  }
  
  const content = await fs.readFile(filePath);
  return { success: true, data: content };
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

```javascript
async function execute(input) {
  const result = execSync(`process-file ${input.name}`);
  return { success: true, data: result };
}
```

---

**Código seguro:**

```javascript
import { execFile } from 'child_process';
import { promisify } from 'util';

const execFileAsync = promisify(execFile);

async function execute(input) {
  // Validar entrada
  if (!input.name.match(/^[a-zA-Z0-9_-]+$/)) {
    return {
      success: false,
      error: {
        code: "INVALID_INPUT",
        message: "name solo puede contener caracteres alfanuméricos"
      }
    };
  }
  
  // Usar execFile en lugar de exec
  const result = await execFileAsync('process-file', [input.name]);
  return { success: true, data: result.stdout };
}
```

---

# Autorización

## Verificar permisos

---

```javascript
async function execute(input, context) {
  // 1. Verificar autenticación
  if (!context.user) {
    return {
      success: false,
      error: {
        code: "UNAUTHORIZED",
        message: "Requiere autenticación"
      }
    };
  }
  
  // 2. Verificar permisos
  if (!hasPermission(context.user, "users:read")) {
    return {
      success: false,
      error: {
        code: "FORBIDDEN",
        message: "No tiene permisos para leer usuarios"
      }
    };
  }
  
  // 3. Verificar ownership (si aplica)
  if (!canAccessResource(context.user, input.resourceId)) {
    return {
      success: false,
      error: {
        code: "FORBIDDEN",
        message: "No tiene acceso a este recurso"
      }
    };
  }
  
  // 4. Registrar acceso
  logger.info("Resource accessed", {
    user: context.user.id,
    resource: input.resourceId,
    action: "read"
  });
  
  // Procesar...
}
```

---

# Auditoría y Logging

## Trazabilidad

---

```javascript
const auditLogger = {
  log: (action, context, details) => {
    logger.info("AUDIT", {
      timestamp: new Date().toISOString(),
      action,
      user: context.user?.id || "anonymous",
      ip: context.ip,
      userAgent: context.userAgent,
      ...details
    });
  }
};

async function execute(input, context) {
  // Registrar intento
  auditLogger.log("DELETE_USER_ATTEMPT", context, {
    targetUser: input.userId
  });
  
  // Verificar permisos
  if (!context.user.isAdmin) {
    auditLogger.log("DELETE_USER_DENIED", context, {
      targetUser: input.userId,
      reason: "INSUFFICIENT_PERMISSIONS"
    });
    
    return {
      success: false,
      error: {
        code: "FORBIDDEN",
        message: "Solo administradores pueden eliminar usuarios"
      }
    };
  }
  
  // Ejecutar
  await db.deleteUser(input.userId);
  
  // Registrar éxito
  auditLogger.log("DELETE_USER_SUCCESS", context, {
    targetUser: input.userId
  });
  
  return { success: true };
}
```

---

# Secrets y Credenciales

## Nunca exponer

---

**❌ Nunca hacer:**

```javascript
{
  name: "getDatabaseConfig",
  execute: async () => {
    return {
      success: true,
      data: {
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD  // NUNCA
      }
    };
  }
}
```

---

**✅ Correcto:**

```javascript
{
  name: "testDatabaseConnection",
  description: "Prueba la conexión a la base de datos",
  execute: async () => {
    try {
      await db.ping();
      return { success: true, data: { connected: true } };
    } catch (error) {
      return { success: false, error: { code: "DB_CONNECTION_ERROR" } };
    }
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

```json
{
  "success": true,
  "data": {
    "user": {
      "id": "usr_abc123",
      "name": "Juan García",
      "email": "juan@example.com",
      "phone": "+34 123 456 789",
      "address": "Calle Principal 123",
      "city": "Madrid",
      "country": "Spain",
      "postalCode": "28001",
      "createdAt": "2024-01-15T10:30:00Z",
      "updatedAt": "2024-03-20T15:45:00Z",
      "lastLogin": "2024-04-18T08:00:00Z",
      "preferences": {
        "language": "es",
        "timezone": "Europe/Madrid",
        "notifications": {
          "email": true,
          "push": false,
          "sms": true
        }
      },
      "subscription": {
        "plan": "premium",
        "startDate": "2024-02-01",
        "endDate": "2024-08-01",
        "autoRenew": true
      }
    }
  }
}
```

---

**✅ Solo lo necesario:**

```json
{
  "success": true,
  "data": {
    "id": "usr_abc123",
    "name": "Juan García",
    "email": "juan@example.com"
  }
}
```

---

# Selección de Campos

## Permitir elegir

---

```javascript
{
  name: "getUser",
  inputSchema: {
    properties: {
      userId: { type: "string" },
      fields: {
        type: "array",
        items: { "enum": ["id", "name", "email", "phone", "address"] },
        description: "Campos a devolver (por defecto: id, name, email)"
      }
    }
  },
  execute: async (input) => {
    const user = await db.getUser(input.userId);
    
    const defaultFields = ["id", "name", "email"];
    const fields = input.fields || defaultFields;
    
    const result = {};
    for (const field of fields) {
      if (user[field] !== undefined) {
        result[field] = user[field];
      }
    }
    
    return { success: true, data: result };
  }
}
```

---

# Caché Estratégico

## Qué cachear

---

**Cacheable:**

- Datos estáticos (configuración)
- Datos que cambian poco (perfiles de usuario)
- Resultados de cálculos costosos
- Listas con baja frecuencia de actualización

---

**No cacheable:**

- Datos sensibles (tokens, sesiones)
- Datos que cambian frecuentemente (logs, métricas)
- Resultados de operaciones de escritura

---

**TTL recomendados:**

| Tipo de dato | TTL |
|--------------|-----|
| Configuración | 5-15 min |
| Perfil de usuario | 1-5 min |
| Listas | 30s - 2 min |
| Búsquedas | 30s - 1 min |

---

# Caché - Implementación

---

```javascript
import NodeCache from 'node-cache';

const cache = new NodeCache({ stdTTL: 60, checkperiod: 120 });

async function execute(input) {
  const cacheKey = `user:${input.userId}:${input.fields?.join(',') || 'default'}`;
  
  // Intentar caché
  const cached = cache.get(cacheKey);
  if (cached) {
    return { success: true, data: cached, cached: true };
  }
  
  // Obtener de DB
  const user = await db.getUser(input.userId);
  
  // Filtrar campos
  const fields = input.fields || ["id", "name", "email"];
  const result = {};
  for (const field of fields) {
    if (user[field] !== undefined) {
      result[field] = user[field];
    }
  }
  
  // Guardar en caché
  cache.set(cacheKey, result);
  
  return { success: true, data: result, cached: false };
}

// Invalidar caché cuando el usuario cambia
function invalidateUserCache(userId) {
  cache.delByPattern(`user:${userId}:*`);
}
```

---

# Paralelización

## Ejecutar en paralelo cuando sea posible

---

**Secuencial (lento):**

```javascript
async function execute(input) {
  const user = await db.getUser(input.userId);
  const orders = await db.getOrders(input.userId);
  const payments = await db.getPayments(input.userId);
  
  return {
    success: true,
    data: { user, orders, payments }
  };
}
// Tiempo: t1 + t2 + t3
```

---

**Paralelo (rápido):**

```javascript
async function execute(input) {
  const [user, orders, payments] = await Promise.all([
    db.getUser(input.userId),
    db.getOrders(input.userId),
    db.getPayments(input.userId)
  ]);
  
  return {
    success: true,
    data: { user, orders, payments }
  };
}
// Tiempo: max(t1, t2, t3)
```

---

# Batching

## Reducir llamadas

---

**Sin batching:**

```javascript
async function execute(input) {
  const results = [];
  for (const id of input.userIds) {
    const user = await db.getUser(id);  // N llamadas
    results.push(user);
  }
  return { success: true, data: results };
}
```

---

**Con batching:**

```javascript
async function execute(input) {
  const users = await db.getUsers(input.userIds);  // 1 llamada
  return { success: true, data: users };
}
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

```javascript
import { describe, it, expect } from 'vitest';
import { getUser } from './tools/users.js';

describe('getUser', () => {
  it('should return user when found', async () => {
    const result = await getUser({ userId: 'usr_123' });
    
    expect(result.success).toBe(true);
    expect(result.data.id).toBe('usr_123');
    expect(result.data.name).toBeDefined();
  });
  
  it('should return error when user not found', async () => {
    const result = await getUser({ userId: 'usr_nonexistent' });
    
    expect(result.success).toBe(false);
    expect(result.error.code).toBe('NOT_FOUND');
  });
  
  it('should return error for invalid userId format', async () => {
    const result = await getUser({ userId: 'invalid' });
    
    expect(result.success).toBe(false);
    expect(result.error.code).toBe('VALIDATION_ERROR');
  });
});
```

---

# Probando Validación

---

```javascript
describe('inputSchema validation', () => {
  const schema = getUserTool.inputSchema;
  
  it('should require userId', () => {
    const valid = validate(schema, {});
    expect(valid).toBe(false);
  });
  
  it('should accept valid userId', () => {
    const valid = validate(schema, { userId: 'usr_abc123' });
    expect(valid).toBe(true);
  });
  
  it('should reject invalid userId format', () => {
    const valid = validate(schema, { userId: 'invalid!' });
    expect(valid).toBe(false);
  });
  
  it('should accept optional fields parameter', () => {
    const valid = validate(schema, { 
      userId: 'usr_abc123',
      fields: ['id', 'name']
    });
    expect(valid).toBe(true);
  });
});
```

---

# Probando Errores

---

```javascript
describe('error handling', () => {
  it('should handle database errors gracefully', async () => {
    // Mock DB error
    vi.spyOn(db, 'getUser').mockRejectedValue(new Error('Connection refused'));
    
    const result = await getUser({ userId: 'usr_123' });
    
    expect(result.success).toBe(false);
    expect(result.error.code).toBe('INTERNAL_ERROR');
    expect(result.error.message).not.toContain('Connection refused'); // No exponer detalles
    expect(result.error.requestId).toBeDefined(); // Para depuración
  });
  
  it('should handle authorization errors', async () => {
    const context = { user: { id: 'usr_456', role: 'user' } };
    
    const result = await deleteUser({ userId: 'usr_123' }, context);
    
    expect(result.success).toBe(false);
    expect(result.error.code).toBe('FORBIDDEN');
  });
});
```

---

# Integration Tests

## Probar con MCP SDK

---

```javascript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { MCPServer } from '@modelcontextprotocol/sdk';
import { createServer } from './server.js';

describe('MCP Server Integration', () => {
  let server;
  let client;
  
  beforeAll(async () => {
    server = await createServer();
    await server.start();
    client = await server.connect();
  });
  
  afterAll(async () => {
    await server.stop();
  });
  
  it('should list tools', async () => {
    const tools = await client.listTools();
    
    expect(tools).toContainEqual(
      expect.objectContaining({ name: 'getUser' })
    );
  });
  
  it('should execute getUser tool', async () => {
    const result = await client.callTool('getUser', { userId: 'usr_123' });
    
    expect(result.success).toBe(true);
    expect(result.data.id).toBe('usr_123');
  });
  
  it('should list resources', async () => {
    const resources = await client.listResources();
    
    expect(resources).toContainEqual(
      expect.objectContaining({ uri: expect.stringContaining('users://') })
    );
  });
});
```

---

# Probando Recursos

---

```javascript
describe('resources', () => {
  it('should read user profile resource', async () => {
    const result = await client.readResource('users://usr_123/profile');
    
    expect(result.contents).toHaveLength(1);
    expect(result.contents[0].mimeType).toBe('application/json');
    
    const data = JSON.parse(result.contents[0].text);
    expect(data.id).toBe('usr_123');
  });
  
  it('should return error for non-existent resource', async () => {
    await expect(
      client.readResource('users://usr_nonexistent/profile')
    ).rejects.toThrow('NOT_FOUND');
  });
  
  it('should deny access to other users resources', async () => {
    const context = { user: { id: 'usr_456' } };
    
    await expect(
      client.readResource('users://usr_123/profile', context)
    ).rejects.toThrow('FORBIDDEN');
  });
});
```

---

# Probando Prompts

---

```javascript
describe('prompts', () => {
  it('should list available prompts', async () => {
    const prompts = await client.listPrompts();
    
    expect(prompts).toContainEqual(
      expect.objectContaining({ name: 'code-review' })
    );
  });
  
  it('should get prompt with arguments', async () => {
    const result = await client.getPrompt('code-review', {
      language: 'javascript'
    });
    
    expect(result.messages).toBeDefined();
    expect(result.messages[0].content.text).toContain('javascript');
  });
  
  it('should validate required arguments', async () => {
    await expect(
      client.getPrompt('code-review', {})
    ).rejects.toThrow('Falta argumento obligatorio');
  });
});
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

**Decisiones de diseño:**

1. **Seguridad:** Prevención de path traversal
2. **Validación:** Nombres de archivo seguros
3. **Autorización:** Directorio base restringido
4. **Errores:** Mensajes claros pero sin exponer rutas internas

---

```javascript
import path from 'path';
import fs from 'fs/promises';

const BASE_DIR = path.resolve('./data');

server.addTool({
  name: "readFile",
  description: "Lee el contenido de un archivo del directorio de datos",
  inputSchema: {
    properties: {
      filename: {
        type: "string",
        pattern: "^[a-zA-Z0-9_.-]+$",
        description: "Nombre del archivo (solo alfanuméricos, _, ., -)"
      }
    },
    required: ["filename"]
  },
  annotations: { readOnlyHint: true },
  
  execute: async (input) => {
    // Validar nombre
    if (!input.filename.match(/^[a-zA-Z0-9_.-]+$/)) {
      return {
        success: false,
        error: {
          code: "INVALID_INPUT",
          message: "Nombre de archivo inválido"
        }
      };
    }
    
    // Resolver ruta de forma segura
    const filePath = path.resolve(BASE_DIR, input.filename);
    
    // Verificar que está dentro del directorio permitido
    if (!filePath.startsWith(BASE_DIR)) {
      return {
        success: false,
        error: {
          code: "FORBIDDEN",
          message: "Acceso denegado"
        }
      };
    }
    
    try {
      const content = await fs.readFile(filePath, 'utf-8');
      return {
        success: true,
        data: { content, filename: input.filename }
      };
    } catch (error) {
      if (error.code === 'ENOENT') {
        return {
          success: false,
          error: {
            code: "NOT_FOUND",
            message: `Archivo ${input.filename} no encontrado`
          }
        };
      }
      
      return {
        success: false,
        error: {
          code: "INTERNAL_ERROR",
          message: "Error al leer el archivo"
        }
      };
    }
  }
});
```

---

# Caso 2: Servidor de Base de Datos

## Constructor de consultas seguro

---

**Requisito:**

Permitir consultas a base de datos con validación y paginación.

---

```javascript
server.addTool({
  name: "queryUsers",
  description: "Busca usuarios con filtros y paginación",
  inputSchema: {
    properties: {
      filters: {
        type: "object",
        properties: {
          status: { "enum": ["active", "inactive", "pending"] },
          role: { "enum": ["admin", "user", "guest"] },
          createdAfter: { type: "string", format: "date-time" },
          createdBefore: { type: "string", format: "date-time" }
        }
      },
      sort: {
        type: "object",
        properties: {
          field: { "enum": ["createdAt", "name", "email"] },
          order: { "enum": ["asc", "desc"] }
        }
      },
      limit: { type: "integer", minimum: 1, maximum: 100, default: 20 },
      offset: { type: "integer", minimum: 0, default: 0 }
    }
  },
  annotations: { readOnlyHint: true },
  
  execute: async (input) => {
    // Construir consulta segura
    const query = db('users');
    
    // Aplicar filtros con whitelist
    if (input.filters?.status) {
      query.where('status', input.filters.status);
    }
    if (input.filters?.role) {
      query.where('role', input.filters.role);
    }
    if (input.filters?.createdAfter) {
      query.where('createdAt', '>=', new Date(input.filters.createdAfter));
    }
    
    // Aplicar ordenamiento con whitelist
    if (input.sort) {
      query.orderBy(input.sort.field, input.sort.order || 'asc');
    }
    
    // Aplicar paginación
    query.limit(input.limit).offset(input.offset);
    
    // Ejecutar
    const users = await query;
    const total = await db('users').count('* as count').first();
    
    return {
      success: true,
      data: {
        items: users.map(u => ({
          id: u.id,
          name: u.name,
          email: u.email,
          status: u.status,
          role: u.role
        })),
        total: total.count,
        hasMore: (input.offset + input.limit) < total.count
      }
    };
  }
});
```

---

# Caso 3: API Gateway

## Servidor que envuelve APIs externas

---

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 10000
});

server.addTool({
  name: "getWeather",
  description: "Obtiene el clima actual para una ciudad",
  inputSchema: {
    properties: {
      city: {
        type: "string",
        description: "Nombre de la ciudad"
      },
      units: {
        type: "string",
        "enum": ["celsius", "fahrenheit"],
        default: "celsius"
      }
    },
    required: ["city"]
  },
  annotations: { readOnlyHint: true, openWorldHint: true },
  
  execute: async (input, context) => {
    try {
      const response = await api.get('/weather', {
        params: {
          city: input.city,
          units: input.units
        }
      });
      
      return {
        success: true,
        data: {
          temperature: response.data.temp,
          conditions: response.data.conditions,
          humidity: response.data.humidity
        }
      };
      
    } catch (error) {
      if (error.response?.status === 404) {
        return {
          success: false,
          error: {
            code: "NOT_FOUND",
            message: `Ciudad "${input.city}" no encontrada`
          }
        };
      }
      
      if (error.response?.status === 429) {
        return {
          success: false,
          error: {
            code: "RATE_LIMIT_EXCEEDED",
            message: "Límite de peticiones excedido",
            retryAfter: error.response.headers['retry-after']
          }
        };
      }
      
      return {
        success: false,
        error: {
          code: "EXTERNAL_SERVICE_ERROR",
          message: "Error al obtener información del clima"
        }
      };
    }
  }
});
```

---

# Checklist de Buenas Prácticas

## Antes de publicar un servicio MCP

---

### Descripciones

- [ ] Todas las tools tienen descripciones claras
- [ ] Todos los parámetros tienen descripción
- [ ] Los valores de enum están documentados
- [ ] Se incluyen ejemplos para casos complejos

---

### Validación

- [ ] Todas las entradas se validan contra el esquema
- [ ] Se validan rangos (min/max)
- [ ] Se validan formatos (email, fecha, etc.)
- [ ] Se sanitizan strings antes de usar en consultas

---

### Seguridad

- [ ] No se exponen credenciales
- [ ] Se previene path traversal
- [ ] Se previene SQL injection
- [ ] Se verifican permisos en cada operación

---

### Errores

- [ ] Todos los errores tienen código
- [ ] Los errores incluyen sugerencias
- [ ] No se exponen detalles internos
- [ ] Se genera requestId para depuración

---

### Rendimiento

- [ ] Se usa paginación para listas grandes
- [ ] Se implementan cachés donde aplica
- [ ] Se minimizan los tokens en respuestas
- [ ] Se paralelizan operaciones independientes

---

### Testing

- [ ] Unit tests para cada tool
- [ ] Tests de validación de entrada
- [ ] Tests de manejo de errores
- [ ] Integration tests con el protocolo

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

Nunca confíes en la entrada. Valida todo.

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
- SDK TypeScript: https://github.com/modelcontextprotocol/typescript-sdk
- SDK Python: https://github.com/modelcontextprotocol/python-sdk

---

**Próximos pasos:**

1. Diseña tu primer servicio MCP
2. Implementa las validaciones
3. Añade manejo de errores estructurado
4. Escribe tests
5. Despliega y monitorea

---

**Preguntas y práctica:** ¡Ahora es tu turno!