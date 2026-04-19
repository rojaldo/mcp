# Curso: Protocolo de Contexto de Modelos (MCP) y WebMCP

---

# Portada

## Model Context Protocol (MCP)

### El Estándar Universal para Conectar IAs con el Mundo

---

**Curso completo sobre MCP y WebMCP**

*De los fundamentos a la implementación práctica*

---

# ¿Por qué MCP?

## El Problema de la Integración

---

**Sin MCP:**

- Cada servicio necesita su propia integración
- El código se duplica para cada cliente de IA
- Las actualizaciones son manuales y costosas

---

**Con MCP:**

- Un solo servidor MCP funciona con todos los clientes
- Protocolo estándar y unificado
- Escribir una vez, usar en todas partes

---

# ¿Qué es MCP?

## Model Context Protocol

---

**Definición:**

MCP es un estándar abierto creado por Anthropic en noviembre de 2024.

---

**Propósito:**

Permitir que aplicaciones de IA se conecten de forma estandarizada con:

- Herramientas externas (tools)
- Fuentes de datos (resources)
- Plantillas de interacción (prompts)

---

# La Analogía del USB-C

## Antes vs Después

---

**Antes del USB-C:**

Cada dispositivo tenía su propio conector:

- Cargadores diferentes
- Cables incompatibles
- Adaptadores por todas partes

---

**Con USB-C:**

Un solo conector para todo:

- Carga
- Datos
- Vídeo
- Accesorios

---

**MCP hace lo mismo para las IAs:**

Un solo protocolo para todas las integraciones.

---

# Key Terminology

## Terminología Oficial del W3C

---

### Agent (Agente)

Un asistente autónomo basado en LLM que entiende los objetivos del usuario y realiza acciones en su nombre a través de interfaces de chat.

---

### Model Context Provider

Una pestaña del navegador navegada a una página que usa la API WebMCP para proporcionar herramientas a los agentes.

---

### Tool Definition

Una estructura con: name, description, inputSchema, execute steps, y readOnlyHint annotation.

---

### Actuation

Un agente interactuando con una página web simulando entrada de usuario: clicks, scroll, typing. WebMCP reemplaza esto.

---

# Key Terminology (continuación)

---

### Browser's Agent

Un agente proporcionado por o a través del navegador - integrado, o vía extensión/plug-in del navegador.

---

### Backend Integration

Una integración API donde una plataforma de IA habla directamente al backend de un servicio sin una UI en vivo. WebMCP complementa, no reemplaza, estas.

---

### Goals (Objetivos)

- **Human-in-the-loop**: usuarios retienen visibilidad y control
- **Simplify AI integration**: herramientas estructuradas vs UI scraping
- **Minimize dev burden**: reutilizar código JS existente
- **Improve accessibility**: acceso estandarizado para AT

---

### Non-Goals (No-Objetivos)

- **Headless browsing**: no para escenarios sin humano presente
- **Autonomous agents**: usar protocolo A2A en su lugar
- **Replacing backend MCP**: WebMCP es complementario
- **Replacing human UI**: las herramientas del agente aumentan, no reemplazan

---

# Arquitectura de MCP

## Los Tres Roles

---

### Cliente (Client)

La aplicación de IA que quiere usar herramientas externas.

*Ejemplos: Claude, ChatGPT, Cursor, Continue*

---

### Servidor (Server)

El servicio que proporciona herramientas, recursos y prompts.

*Ejemplos: Google Drive, PostgreSQL, GitHub*

---

### Host

El entorno donde corre el cliente.

*Ejemplos: IDE, navegador, aplicación desktop*

---

# Diagrama de Arquitectura

## Cómo se conectan

---

```
         ┌─────────────────┐
         │   CLIENTE IA   │
         │ (Claude, GPT)   │
         └────────┬────────┘
                  │
      ┌───────────┼───────────┐
      │           │           │
      ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ SERVIDOR│ │ SERVIDOR│ │ SERVIDOR│
│ Drive   │ │ GitHub  │ │ Postgres│
└─────────┘ └─────────┘ └─────────┘
```

---

**Cada servidor:**

- Se conecta una vez
- Funciona con cualquier cliente compatible
- Implementa el protocolo MCP

---

# Métodos de Transporte

## Cómo se comunican cliente y servidor

---

### STDIO (Standard Input/Output)

El servidor corre como proceso hijo del cliente.

- Comunicación por entrada/salida estándar
- Ideal para herramientas locales
- Más simple de implementar

---

### HTTP + SSE (Server-Sent Events)

El servidor corre como servicio HTTP.

- Comunicación por HTTP con eventos
- Ideal para servicios remotos
- Permite múltiples clientes

---

### WebSocket

Comunicación bidireccional en tiempo real.

- Ideal para aplicaciones interactivas
- Menor latencia
- Más complejo de implementar

---

# Las Tres Primitivas

## Bloques de construcción de MCP

---

### 1. Tools (Herramientas)

Funciones que el modelo puede ejecutar.

- El modelo decide cuándo llamarlas
- Tienen parámetros definidos
- Retornan resultados

---

### 2. Resources (Recursos)

Datos que el modelo puede leer.

- Son pasivos, no se ejecutan
- Proporcionan contexto
- Se actualizan dinámicamente

---

### 3. Prompts (Plantillas)

Plantillas predefinidas para interacciones comunes.

- Modos de especialización
- Flujos recurrentes
- Contextos específicos

---

# Tools - Estructura JSON

## Definición de una herramienta

---

```json
{
  "name": "search_products",
  "description": "Busca productos en el catálogo",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" },
      "category": { "type": "string" }
    },
    "required": ["query"]
  }
}
```

---

**El modelo lee esto y entiende:**

- Qué hace la tool
- Qué parámetros necesita
- Cuáles son obligatorios

---

# Resources - Concepto Detallado

## ¿Qué es un Resource?

---

**Un resource es:**

Un dato que el modelo puede leer para obtener contexto.

---

**Ejemplos:**

- Contenido de un archivo
- Registros de una base de datos
- Respuesta de una API
- Logs del sistema
- Estado de una aplicación

---

**Diferencia con Tools:**

- Tools se **ejecutan** (acción)
- Resources se **leen** (información)

---

# Resources - Estructura JSON

## Definición de un recurso

---

```json
{
  "uri": "file:///proyectos/notas.md",
  "name": "Notas del proyecto",
  "mimeType": "text/markdown",
  "description": "Archivo de notas del proyecto actual"
}
```

---

**Campos importantes:**

- `uri`: Identificador único del recurso
- `name`: Nombre legible
- `mimeType`: Tipo de contenido
- `description`: Descripción opcional

---

# Resources - Tipos de URI

## Esquemas comunes

---

**file://** - Archivos locales

`file:///home/user/documento.txt`

---

**http://** y **https://** - Recursos web

`https://api.example.com/data`

---

**custom://** - Esquemas personalizados

`postgres://localhost/mi_base/tabla`

---

# Prompts - Concepto Detallado

## ¿Qué es un Prompt?

---

**Un prompt es:**

Una plantilla predefinida que el modelo puede usar.

---

**Para qué sirve:**

- Modos de especialización ("actúa como experto en X")
- Flujos de trabajo recurrentes
- Contextos específicos
- Instrucciones complejas predefinidas

---

**Ventaja:**

El usuario no tiene que escribir las instrucciones cada vez.

---

# Prompts - Estructura JSON

## Definición de un prompt

---

```json
{
  "name": "code-review",
  "description": "Revisa código fuente buscando errores",
  "arguments": [
    {
      "name": "language",
      "description": "Lenguaje de programación",
      "required": true
    }
  ]
}
```

---

**El modelo puede llamar:**

`use_prompt("code-review", { language: "python" })`

---

# Flujo de Comunicación

## Secuencia de interacción

---

**Paso 1: Conexión**

El cliente se conecta al servidor y negocia capacidades.

---

**Paso 2: Descubrimiento**

El cliente pregunta qué tools, resources y prompts están disponibles.

---

**Paso 3: Petición**

El modelo decide usar una tool o leer un resource.

---

**Paso 4: Ejecución**

El servidor ejecuta la acción y devuelve el resultado.

---

# Diagrama de Secuencia

## Flujo completo

---

```
CLIENTE                 SERVIDOR
   │                       │
   │ initialize            │
   │──────────────────────►│
   │                       │
   │ initialized           │
   │◄──────────────────────│
   │                       │
   │ tools/list            │
   │──────────────────────►│
   │                       │
   │ tools/list (response) │
   │◄──────────────────────│
   │                       │
   │ tools/call            │
   │──────────────────────►│
   │                       │
   │ tool/result           │
   │◄──────────────────────│
```

---

# Clientes Compatibles

## ¿Quiénes usan MCP?

---

**Aplicaciones de IA:**

- Claude Desktop
- ChatGPT
- Cursor
- Continue
- Windsurf
- Zed

---

**IDEs:**

- VS Code (con extensión)
- JetBrains (con plugin)
- Neovim (con configuración)

---

**La lista crece cada mes.**

---

# Servidores MCP Populares

## ¿Qué puedes conectar?

---

**Fuentes de datos:**

- Google Drive
- PostgreSQL
- SQLite
- Filesystem
- Slack

---

**Herramientas:**

- GitHub
- Git
- Puppeteer
- Brave Search

---

**Servicios:**

- Memory (memoria persistente)
- Sequential Thinking (razonamiento)

---

# WebMCP - Introducción

## MCP en el Navegador

---

**WebMCP** es una especificación del W3C Community Group.

---

**Propósito:**

Llevar MCP al navegador para que las páginas web actúen como servidores MCP.

---

**Idea clave:**

Registra funciones JavaScript como herramientas invocables por IA, reutilizando la lógica frontend existente sin necesidad de backend.

---

# El Problema que WebMCP Resuelve

---

### Enfoque 1: Screenshots (UI Actuation)

El agente toma capturas de pantalla y las analiza.

**Problemas:**

- ~2,000 tokens por captura
- Frágil a cambios de layout
- El agente adivina qué hacer

---

### Enfoque 2: Backend-only MCP

El agente se conecta a un servidor MCP backend.

**Problemas:**

- Sin contexto compartido con el usuario
- Auth separado
- No puede reutilizar lógica frontend

---

### La Solución WebMCP

- Ejecuta JavaScript client-side
- Reutiliza lógica frontend existente
- Comparte página en vivo con usuario
- Sesión/auth natural

---

# WebMCP - Comparación de Enfoques

## Tabla comparativa

---

| Enfoque | Tokens | Precisión | Auth |
|---------|--------|-----------|------|
| Screenshots | ~2000 | Baja | Manual |
| Backend MCP | ~100 | Alta | Separada |
| UI Scraping | ~500 | Media | Manual |
| **WebMCP** | **~100** | **Alta** | **Automática** |

---

**WebMCP consume 20 veces menos tokens que screenshots.**

---

# API de WebMCP - Navigator Extension

---

WebMCP extiende el objeto `navigator` del navegador:

---

```javascript
// API de producción - usada por tu app
navigator.modelContext.registerTool({
  name: "searchProducts",
  description: "Search the product catalog by keyword",
  inputSchema: { 
    type: "object", 
    properties: { 
      query: { type: "string" } 
    } 
  },
  execute: async (input) => await searchCatalog(input.query)
});
```

---

**SecureContext:** Solo disponible en páginas HTTPS.

---

# API - ModelContext Interface

## Métodos disponibles

---

### registerTool(tool)

Registra una herramienta con el navegador.

```javascript
navigator.modelContext.registerTool({
  name: "myTool",
  description: "Description of what the tool does",
  inputSchema: { /* JSON Schema */ },
  execute: async (input) => { /* logic */ }
});
```

---

**Lanza InvalidStateError si:**

- Ya existe una tool con el mismo nombre
- El inputSchema es inválido
- El name o description están vacíos

---

### unregisterTool(name)

Elimina una herramienta por su nombre.

```javascript
navigator.modelContext.unregisterTool("myTool");
```

---

**Lanza InvalidStateError si la tool no existe.**

---

# API - Complete IDL

## Especificación oficial W3C

---

```javascript
// Navigator extension
partial interface Navigator {
  [SecureContext, SameObject] 
  readonly attribute ModelContext modelContext;
};

[Exposed=Window, SecureContext]
interface ModelContext {
  undefined registerTool(ModelContextTool tool);
  undefined unregisterTool(DOMString name);
};

dictionary ModelContextTool {
  required DOMString name;
  required DOMString description;
  object inputSchema;
  required ToolExecuteCallback execute;
  ToolAnnotations annotations;
};

dictionary ToolAnnotations {
  boolean readOnlyHint = false;
};

callback ToolExecuteCallback = 
  Promise<object> (object input, ModelContextClient client);
```

---

# API - ModelContextClient

## Interacción con el usuario

---

```javascript
[Exposed=Window, SecureContext]
interface ModelContextClient {
  Promise<any> requestUserInteraction(
    UserInteractionCallback callback
  );
};

callback UserInteractionCallback = Promise<any> ();
```

---

### requestUserInteraction

Pausa la ejecución de la tool para mostrar al usuario un diálogo, confirmación, u otra interacción. El agente espera a que el usuario responda antes de que la tool continúe.

---

# Tool Definition - Todos los Campos

---

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| name | DOMString | Sí | Identificador único usado por agentes |
| description | DOMString | Sí | Descripción en lenguaje natural |
| inputSchema | object | No | JSON Schema de parámetros esperados |
| execute | ToolExecuteCallback | Sí | Callback invocado cuando el agente llama la tool |
| annotations | ToolAnnotations | No | Metadatos opcionales (readOnlyHint) |

---

# inputSchema - Ejemplos Detallados

---

### Parámetro string simple

```javascript
inputSchema: {
  type: "object",
  properties: {
    query: {
      type: "string",
      description: "Search term"
    }
  },
  required: ["query"]
}
```

---

### Múltiples parámetros tipados

```javascript
inputSchema: {
  type: "object",
  properties: {
    productId: { type: "string" },
    quantity: { type: "integer", minimum: 1 },
    size: {
      type: "string",
      enum: ["S", "M", "L", "XL"]
    }
  },
  required: ["productId", "quantity"]
}
```

---

# inputSchema - Arrays

## Listas de valores

---

**Array simple:**

```javascript
{
  type: "array",
  items: { type: "string" },
  minItems: 1,
  maxItems: 10
}
```

---

**Array de objetos:**

```javascript
{
  type: "array",
  items: {
    type: "object",
    properties: {
      name: { type: "string" },
      price: { type: "number" }
    }
  }
}
```

---

# execute y annotations

## La función principal

---

### execute callback signature

```javascript
// input = parámetros del agente (matchean inputSchema)
// client = ModelContextClient para interacción usuario
async (input, client) => {
  // Hacer el trabajo...
  return { result: "data" }; // debe retornar object
}
```

---

### ToolAnnotations - readOnlyHint

```javascript
annotations: { readOnlyHint: true }
```

**Cuando readOnlyHint: true**, el agente sabe que la tool no modificará estado. El navegador/agente puede llamarla sin prompts de confirmación.

---

**Cuando readOnlyHint: false** (omitir), la tool puede modificar estado y puede requerir confirmación del usuario.

---

# Code Example 1: Basic Tool Registration

## Herramienta de solo lectura

---

```javascript
// Requiere HTTPS (SecureContext)
navigator.modelContext.registerTool({
  name: "searchProducts",
  description: "Search the product catalog by keyword. Returns a list of matching products with name, price, and availability.",
  inputSchema: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "The search keyword or phrase"
      },
      category: {
        type: "string",
        enum: ["all", "clothing", "electronics", "books"],
        description: "Product category to filter by"
      }
    },
    required: ["query"]
  },
  execute: async (input) => {
    // ¡Reutiliza tu lógica de búsqueda frontend existente!
    const results = await productStore.search(input.query, input.category);
    return { products: results, total: results.length };
  },
  annotations: { readOnlyHint: true } // No modifica estado
});
```

---

**Explicación:**

- `name`: Identificador único para el agente
- `description`: Explica QUÉ hace y QUÉ retorna
- `inputSchema`: Valida los parámetros de entrada
- `execute`: La función que se ejecuta, puede reutilizar código existente
- `readOnlyHint: true`: Indica que es segura de ejecutar sin confirmación

---

# Code Example 2: State-Modifying Tool

## Herramienta que modifica estado

---

```javascript
navigator.modelContext.registerTool({
  name: "addToCart",
  description: "Add a product to the user's shopping cart",
  inputSchema: {
    type: "object",
    properties: {
      productId: { type: "string" },
      quantity: { type: "integer", minimum: 1 }
    },
    required: ["productId", "quantity"]
  },
  execute: async (input) => {
    await cart.add(input.productId, input.quantity);
    return { success: true, cartTotal: cart.total };
  }
  // readOnlyHint omitido → por defecto false
});
```

---

**Explicación:**

- No tiene `readOnlyHint` porque modifica el carrito
- `minimum: 1` valida que la cantidad sea al menos 1
- Retorna información útil: estado del carrito después del cambio
- El agente puede mostrar confirmación antes de ejecutar

---

# Code Example 3: User Interaction (Confirmation)

## Pedir confirmación al usuario

---

```javascript
execute: async (input, client) => {
  // Pausar y pedir confirmación al usuario
  const confirmed = await client.requestUserInteraction(
    async () => {
      // Mostrar tu diálogo de confirmación UI
      return await showConfirmDialog(
        `Delete ${input.filename}?`
      );
    }
  );

  if (!confirmed) {
    return { cancelled: true };
  }

  await deleteFile(input.filename);
  return { deleted: true };
}
```

---

**Explicación:**

- `client` es el segundo parámetro de `execute`
- `requestUserInteraction` pausa la ejecución
- El callback muestra UI y retorna true/false
- Si el usuario cancela, retornamos `{ cancelled: true }`
- Solo ejecutamos la acción destructiva si confirma

---

# Code Example 4: Dynamic Registration

## Registrar herramientas según estado

---

```javascript
// Registrar cuando el usuario hace login
function onUserLogin(user) {
  navigator.modelContext.registerTool({
    name: "getUserOrders",
    description: "Get the current user's order history",
    execute: async () => ({
      orders: await api.getOrders(user.id)
    }),
    annotations: { readOnlyHint: true }
  });
}

// Eliminar cuando el usuario hace logout
function onUserLogout() {
  navigator.modelContext.unregisterTool("getUserOrders");
}
```

---

**Explicación:**

- Las tools se registran/eliminan dinámicamente según el contexto
- Solo exponer herramientas relevantes al estado actual
- `getUserOrders` solo está disponible si el usuario está autenticado
- Evita errores de "usuario no autenticado" proactivamente

---

# Code Example 5: Updating a Tool

## Patrón correcto para actualizar

---

```javascript
// ❌ ERROR: Lanza InvalidStateError - nombre ya existe
navigator.modelContext.registerTool({ name: "myTool", ... });
navigator.modelContext.registerTool({ name: "myTool", ... });

// ✅ CORRECTO: Unregister primero, luego re-register
navigator.modelContext.unregisterTool("myTool");
navigator.modelContext.registerTool({ name: "myTool", ...newVersion });
```

---

**Explicación:**

- No se puede registrar una tool con el mismo nombre dos veces
- Debes eliminar la existente antes de registrar la nueva versión
- Esto permite actualizar la funcionalidad sin recargar la página

---

# Code Example 6: Registering Multiple Tools

## Registro masivo al cargar la página

---

```javascript
const tools = [
  { 
    name: "getProducts", 
    description: "List all products", 
    execute: getProducts, 
    annotations: { readOnlyHint: true } 
  },
  { 
    name: "addToCart", 
    description: "Add product to cart", 
    execute: addToCart 
  },
  { 
    name: "checkout", 
    description: "Start checkout process", 
    execute: startCheckout 
  },
];

tools.forEach(tool =>
  navigator.modelContext.registerTool(tool)
);
```

---

**Explicación:**

- Definir todas las tools en un array mejora la legibilidad
- Registrarlas de una vez al cargar la página
- Fácil de mantener: añadir/eliminar tools del array

---

# Caso de Uso - E-commerce

## Herramientas para tienda online

---

**Tools de solo lectura:**

- `searchProducts` - Busca productos
- `getProductDetails` - Obtiene detalles
- `getOrderStatus` - Estado del pedido

---

**Tools que modifican estado:**

- `addToCart` - Añade al carrito
- `removeFromCart` - Quita del carrito
- `checkout` - Inicia compra

---

**Flujo típico:**

1. Usuario busca productos
2. Añade al carrito
3. Confirma pedido

---

# Caso de Uso - E-commerce Código

## Implementación completa

---

```javascript
// Herramientas de solo lectura
navigator.modelContext.registerTool({
  name: "searchProducts",
  description: "Busca productos por nombre o categoría",
  inputSchema: {
    type: "object",
    properties: {
      query: { 
        type: "string",
        description: "Palabra clave para buscar"
      },
      category: { 
        type: "string",
        description: "Categoría para filtrar"
      }
    },
    required: ["query"]
  },
  execute: async (input) => {
    return { products: await productStore.search(input) };
  },
  annotations: { readOnlyHint: true }
});

// Herramienta que modifica estado
navigator.modelContext.registerTool({
  name: "addToCart",
  description: "Añade producto al carrito",
  inputSchema: {
    type: "object",
    properties: {
      productId: { type: "string" },
      quantity: { type: "integer", minimum: 1 }
    },
    required: ["productId", "quantity"]
  },
  execute: async (input) => {
    await cart.add(input.productId, input.quantity);
    return { success: true, cartTotal: cart.total };
  }
});
```

---

# Caso de Uso - Aplicación de Notas

## Herramientas para productividad

---

**Tools disponibles:**

- `createNote` - Crea una nueva nota
- `searchNotes` - Busca notas
- `updateNote` - Actualiza una nota
- `deleteNote` - Elimina una nota (con confirmación)

---

**readOnlyHint:**

- searchNotes → true
- createNote → false
- updateNote → false
- deleteNote → false (con confirmación)

---

# Caso de Uso - Notas Código

## Implementación

---

```javascript
navigator.modelContext.registerTool({
  name: "createNote",
  description: "Crea una nueva nota",
  inputSchema: {
    type: "object",
    properties: {
      title: { type: "string" },
      content: { type: "string" },
      tags: { type: "array", items: { type: "string" } }
    },
    required: ["title", "content"]
  },
  execute: async (input) => {
    const note = await notes.create(input);
    return { id: note.id, created: true };
  }
});

navigator.modelContext.registerTool({
  name: "searchNotes",
  description: "Busca notas por contenido o etiquetas",
  inputSchema: {
    type: "object",
    properties: {
      query: { type: "string" }
    }
  },
  execute: async (input) => {
    return { notes: await notes.search(input.query) };
  },
  annotations: { readOnlyHint: true }
});
```

---

# WebMCP vs. Backend MCP Integration

## Tabla comparativa

---

| Aspecto | WebMCP | Backend MCP |
|---------|--------|-------------|
| **Dónde corre el código** | Client-side JavaScript en el navegador | Server-side (Python, Node.js, etc.) |
| **Requiere navegación** | Sí - la página debe estar abierta | No - siempre disponible si el servidor corre |
| **Contexto UI compartido** | Sí - usuario y agente comparten la misma página | No - el agente interactúa sin UI |
| **Auth / sesión** | Naturalmente compartida con la sesión del navegador | Debe gestionarse separadamente |
| **Mejor para** | Escenarios colaborativos, human-in-the-loop | Flujos autónomos, headless, server-to-server |

---

**Conclusión: Son complementarios, no competidores.**

Muchas aplicaciones usarán ambos.

---

# WebMCP vs. UI Actuation

---

| Aspecto | WebMCP | UI Actuation |
|---------|--------|--------------|
| **Fiabilidad** | Alta | Baja - frágil a cambios de UI |
| **Velocidad** | Rápida - llamadas directas | Lenta - múltiples pasos |
| **Control del desarrollador** | Total - defines las tools | Ninguno - el agente adivina |
| **Costo en tokens** | Bajo - JSON compacto | ~2,000 tokens/screenshot |

---

# WebMCP vs. OpenAPI & A2A

## Otros enfoques

---

### vs. OpenAPI

OpenAPI describe APIs HTTP para function-calling (ChatGPT Actions, Gemini Function Calling).

WebMCP corre en el navegador usando JavaScript, no HTTP. Las tools ejecutan client-side.

**Relación: complementarios - OpenAPI para server-side, WebMCP para client-side.**

---

### vs. Agent2Agent (A2A)

A2A conecta agentes de IA entre sí, con advertisement de capacidades, interacciones de larga duración, y I/O multimodal.

WebMCP es para conectar agentes de IA a aplicaciones web con un humano en el loop.

**Relación: problemas diferentes - A2A para agent mesh, WebMCP para workflows web humano+agente.**

---

# Which Approach to Use?

## Guía de decisión

---

### Usa WebMCP cuando...

- El usuario está activamente presente en la pestaña
- Quieres reutilizar código frontend
- Se requiere supervisión humana
- El contexto UI compartido importa

---

### Usa Backend MCP cuando...

- No se necesita pestaña de navegador
- Workflows server-to-server
- Pipelines totalmente autónomos
- Herramientas siempre disponibles

---

### Usa OpenAPI cuando...

- Exponiendo APIs HTTP REST
- Integración ChatGPT/Gemini
- Consumidores estándar de APIs web
- Sin acceso al código frontend

---

### Usa A2A cuando...

- Comunicación agent-to-agent
- Tareas de agentes de larga duración
- I/O multimodal de agentes
- Sin humano en el loop

---

# Canonical Use Cases

## Tres ejemplos oficiales del W3C

---

### Creative Applications

**Scenario:** Un usuario colabora con un agente del navegador en una plataforma de diseño gráfico. El agente ayuda a encontrar plantillas y hacer cambios de diseño mientras el usuario retiene revisión y control completos.

**Example Tools:**

- `filterTemplates(description)`
- `editDesign(instructions)`
- `orderPrint(designId, format)`

**Benefit:** El agente descubre features que el usuario no sabía que existían.

---

# Canonical Use Cases (continuación)

---

### E-Commerce / Shopping

**Scenario:** Un usuario navega una tienda de ropa. El agente llama `getDresses(size)` para recibir una lista JSON estructurada con descripciones e imágenes, filtra por criterios, luego llama `showDresses(product_ids)` para actualizar la UI.

**Example Tools:**

- `getDresses(size, color?, priceMax?)`
- `showDresses(productIds)`
- `addToCart(productId, size)`

**Benefit:** Respuesta JSON estructurada vs miles de tokens de screenshots.

---

### Developer Tooling (Code Review)

**Scenario:** En una plataforma de code review como Gerrit, herramientas específicas permiten al agente recuperar datos de fallos de test y aplicar sugerencias de código de forma estructurada.

**Example Tools:**

- `getTryRunStatuses(patchsetId)` - Retorna datos de fallos de CI
- `addSuggestedEdit(filename, patch)` - Aplica sugerencia al review
- `getOpenComments()` - Lista comentarios sin resolver

**Benefit:** El agente maneja trabajo repetitivo; el humano revisa y aprueba.

---

# Accessibility Benefits

---

### Problema tradicional

Los accessibility trees tradicionales no están ampliamente implementados. Las tecnologías de asistencia tienen dificultades para interactuar con aplicaciones web complejas vía interacciones a nivel de DOM.

---

### Lo que WebMCP proporciona

Acciones de aplicación de alto nivel estandarizadas mapeadas a operaciones significativas (ej: "añadir item de todo") en lugar de interacciones DOM de bajo nivel.

---

### Unified Surface

Las mismas tools disponibles para agentes de IA están disponibles para herramientas de accesibilidad - una implementación sirve para ambas audiencias sin trabajo extra.

---

# Testing & Debugging API

## inspector.modelContextTesting

---

**Disponible en Chrome 146+ con flag**

`#enable-webmcp-for-testing` en chrome://flags

---

### Qué es

Un companion de testing para `navigator.modelContextTesting`. Puede leer y reemplazar todas las tools registradas en la página actual.

---

### Quién lo usa

Extensiones de navegador, paneles de DevTools, y scripts de test automatizados que necesitan inspeccionar o hacer stub de tools sin modificar el código fuente.

---

**Solo desarrollo - no disponible en producción.**

---

# Testing API - Feature Detection

---

```javascript
// Check production API
if ('modelContext' in navigator) {
  // Safe to call registerTool / unregisterTool
  navigator.modelContext.registerTool({ ... });
}

// Check testing API (dev environments only)
if ('modelContextTesting' in navigator) {
  // Safe to call getTools / provideContext / clearContext
  const tools = await navigator.modelContextTesting.getTools();
}
```

---

**Importante:** Siempre verificar existencia antes de usar.

---

# Testing API - getTools()

## Listar herramientas registradas

---

```javascript
// Listar todas las tools registradas en la página
const tools = await navigator.modelContextTesting.getTools();
console.log(tools.map(t => t.name));
// → ["searchProducts", "addToCart", "checkout"]
```

---

# Testing API - provideContext()

## Reemplazar herramientas en una llamada atómica

---

```javascript
// Reemplaza TODAS las tools actualmente registradas
await navigator.modelContextTesting.provideContext({
  tools: [
    {
      name: "stubSearch",
      description: "Returns mock search results",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string" }
        }
      },
      execute: async () => ({ results: ["mock-item-1"] })
    }
  ]
});
```

---

**Benefit:** Atómico - no hay estado intermedio visible para los agentes.

---

# Testing API - clearContext()

## Limpiar todas las herramientas

---

```javascript
// Tear down después de cada test
afterEach(async () => {
  if ('modelContextTesting' in navigator) {
    await navigator.modelContextTesting.clearContext();
  }
});

// O resetear antes de cada escenario
beforeEach(async () => {
  await navigator.modelContextTesting.clearContext();
  // Luego registrar exactamente las tools que este test necesita
  navigator.modelContext.registerTool({ name: "myTool", ... });
});
```

---

# Testing API - executeTool()

## Ejecutar herramientas directamente

---

```javascript
// Listar tools primero
const tools = await navigator.modelContextTesting.getTools();
console.log(tools.map(t => t.name));
// → ["searchProducts", "addToCart", "checkout"]

// Ejecutar una tool específica con input de test
const result = await navigator.modelContextTesting
  .executeTool("searchProducts", { query: "shoes" });
console.log(result);
// → { products: [...], total: 12 }
```

---

# Testing API - IDL Summary

---

```javascript
partial interface Navigator {
  [SecureContext] 
  readonly attribute ModelContextTesting modelContextTesting;
};

[Exposed=Window, SecureContext]
interface ModelContextTesting {
  // Leer todas las tools registradas en esta página
  Promise<FrozenArray<ModelContextToolInfo>> getTools();

  // Reemplazar todo el conjunto de tools atómicamente
  undefined provideContext(ModelContextInit init);

  // Eliminar todas las tools registradas
  undefined clearContext();

  // Invocar una tool por nombre con JSON input
  Promise<object> executeTool(DOMString name, object input);
};
```

---

# Security & Privacy

## Dos Trust Boundaries

---

### Boundary 1: Site → Browser

Cuando un sitio web registra tools vía WebMCP, expone información sobre sus capacidades al navegador.

**El navegador debe:**

- Pedir permiso al usuario
- Proporcionar visibilidad sobre qué tools están expuestas

---

### Boundary 2: Agent → Site (via Browser)

Cuando un agente quiere usar esas tools, el sitio recibe input no confiable en parámetros y las salidas pueden contener datos sensibles del usuario.

**El navegador media este límite.**

**Usuarios pueden "always allow" tool calls para pares sitio+agente confiables.

---

# Security - HTTPS Required

---

`navigator.modelContext` tiene `[SecureContext]` - solo existe en páginas HTTPS.

---

```javascript
// En HTTP - undefined
console.log(navigator.modelContext); // undefined

// En HTTPS - funciona
navigator.modelContext.registerTool(...);
```

---

**Verificar antes de llamar:**

```javascript
if (window.isSecureContext) {
  navigator.modelContext.registerTool(...);
}
```

---

# Security - Top-Level Browsing Contexts Only

---

Solo un contexto de navegación de nivel superior (una pestaña del navegador) puede ser un Model Context Provider.

**iframes están excluidos.**

---

### Por qué iframes están excluidos

- Mantiene un límite de seguridad claro
- Previene que contenido embebido exponga tools sin conocimiento de la página padre
- Los embedders gestionan capacidades de contextos embebidos

---

# Security - Model Poisoning Risk

---

### El Riesgo

Desarrolladores web maliciosos podrían crear tools para exponer contenido que el usuario normalmente no vería, o manipular comportamiento del agente a través de descripciones y respuestas de tools cuidadosamente diseñadas.

---

**Esto es una pregunta abierta en el spec - activamente bajo investigación por el W3C community group.**

---

# Security - Cross-Origin Isolation

---

### La Preocupación

Data output de las tools de una app podría pasarse como input a las tools de otra app. Aunque workflows cross-origin legítimos existen, esto requiere mediación cuidadosa del navegador.

---

### Browser Responsibility

El navegador debe indicar claramente qué aplicaciones web están siendo invocadas y con qué datos, para que los usuarios puedan intervenir en cadenas de tools cross-origin.

---

# Security - Developer Checklist

---

### Input Validation

- Siempre validar inputs del agente contra tu inputSchema
- Tratar input como no confiable (como input de usuario de un formulario)
- Sanitizar strings antes de usar en queries o HTML

---

### Sensitive Data

- Solo retornar datos que el usuario tiene permiso de ver
- No exponer PII en respuestas de tools innecesariamente
- Usar `requestUserInteraction` para operaciones destructivas

---

### Auth & State

- Verificar que el usuario está autenticado antes de registrar tools sensibles
- Eliminar tools cuando el usuario hace logout
- Marcar tools de solo lectura con `readOnlyHint: true`

---

# Future Roadmap

## Extensiones planificadas y preguntas abiertas

---

### Declarative WebMCP

**Status:** TODO en spec - deferred

**Concepto:** Registrar tools vía elementos HTML en lugar de llamadas JavaScript `registerTool()`. Las tools se derivarían de formularios HTML y sus elementos asociados.

---

```html
<!-- Conceptual future syntax -->
<form webmcp-tool="searchProducts"
      webmcp-description="Search for products">
  <input name="query" type="text">
</form>
```

---

Un algoritmo "synthesize a declarative JSON Schema" derivaría el inputSchema de los elementos del formulario automáticamente.

---

# Future Roadmap (continuación)

---

### Progressive Web Apps (PWAs)

**Status:** Future exploration

**Concepto:** Una PWA con manifest podría declarar tools disponibles "offline" - antes de que la PWA se lance. Cuando un agente llama la tool, el sistema host auto-lanza la PWA y navega a la página apropiada.

---

**Esto cerraría la brecha entre WebMCP (tab debe estar abierta) y backend MCP (siempre disponible).**

---

### Background Model Context Providers

**Status:** Future exploration

**Concepto:** Algunas tools pueden no requerir UI de navegador. Una app de to-do podría exponer una tool "add item" que corre sin mostrar ventana - mostrando solo una notificación cuando se trigger.

---

**Punto de integración:** Podría combinarse con la web app launch handler API para ejecución de tools en background seamless.

---

# Future Roadmap - Tool Discovery

---

### Current Limitation

Las tools solo son descubribles una vez que se navega a una página. Un agente no puede saber qué tools ofrece un sitio sin cargarlo primero.

---

### Future: Manifest-Based Discovery

Definiciones de tools declarativas en el app manifest permitirían a agentes descubrir capacidades de un sitio vía un simple HTTP GET - sin navegación completa de página.

**Los agentes seguirían necesitando navegar para usar las tools.**

---

# Future Roadmap - Open Design Questions

---

### Main Thread Performance

Las llamadas a tools corren en el main thread. Cuando los agentes solicitan muchas llamadas en secuencia o las tools son computacionalmente costosas, esto puede causar problemas de rendimiento.

**Status:** Under investigation.

---

### Permission Model Details

El UX exacto para los prompts de permiso del navegador - cuándo preguntar, cómo formularlo, qué granularidad de "always allow" - necesita más input de la comunidad y coordinación con browser vendors.

---

### iframe Capabilities

¿Cómo deberían los embedders (páginas padre) gestionar las capacidades proporcionadas a iframes embebidos? La propuesta actual limita esto a contextos de nivel superior, pero trabajo futuro puede definir modelos de delegación.

---

# Spec Status & Governance

---

### Current Status

Draft Community Group Report - 9 March 2026

**NOT a W3C Standard, nor on the W3C Standards Track. Under incubation.**

---

### Editors

- Brandon Walderman - Microsoft
- Khushal Sagar - Google
- Dominic Farolino - Google

---

### Governing Body

W3C Web Machine Learning Community Group

License: W3C Community Contributor License Agreement (CLA)

First published: August 13, 2025

---

# Resources & Tools

---

### WebMCP Inspector

Inspect & augment WebMCP tools on any page. Browse, test, and debug tools registered via navigator.modelContext directly in your browser.

**URL:** webmcpinspector.com/inspect/

---

### Model Context Tool Inspector

A Chrome extension built on `navigator.modelContextTesting` that provides a visual UI:

- Lists all tools registered on the current page with full schema
- Execute any tool with a JSON input editor
- View execution output in real time
- Optionally chain calls through Gemini for agent-style testing

**Source:** github.com/beaufortfrancois/model-context-tool-inspector

---

# Prior Art & Related Projects

---

### MCP-B (WebMCP by MiguelsPizza)

Open-source project with similar motivation. Extends MCP with tab transports for in-page communication and extension transports for cross-extension communication. Enables tool caching and cross-site tool composition.

**Acknowledged as directly related prior art by the W3C spec.**

github.com/MiguelsPizza/WebMCP

---

### OpenAPI

Standard for describing HTTP APIs. Used by ChatGPT Actions and Gemini Function Calling. Unlike WebMCP, OpenAPI tools are backend HTTP services - no browser required.

**Relationship:** Complementary - OpenAPI for server-side, WebMCP for client-side.

---

### Agent2Agent (A2A)

Protocol for AI agent-to-agent communication. Provides capability advertisement, long-running interactions, and multimodal I/O.

**Relationship:** Different problem - A2A for agent mesh, WebMCP for human+agent web workflows.

---

# Key Design Rationale

---

### Why Align with MCP?

- Cualquier agente compatible con MCP funciona con traducción mínima
- Desarrolladores pueden reutilizar código entre WebMCP y backend MCP
- El navegador puede evolucionar compatibilidad MCP independientemente
- Políticas de seguridad web-platform pueden aplicarse

---

### Why Not Static Manifests?

- Limitaría WebMCP a PWAs instalados solo
- Un nuevo formato de manifest aún necesita implementación
- No puede ejecutar código o actualizar tools dinámicamente
- El registro dinámico es una capability crítica para desarrolladores

---

### Why Top-Level Only?

- Límite de seguridad claro y entendible
- Previene leakage de capacidades basado en iframes
- Embedders gestionan capacidades de iframes
- Modelo mental más simple para usuarios y desarrolladores

---

# Mejores Prácticas - Descripción

## Escribir descripciones claras

---

**La descripción es lo más importante.**

La IA la usa para decidir si llamar a la tool.

---

**❌ Malo:**

```javascript
description: "Busca productos"
```

Demasiado vago. La IA no sabe bien qué hace.

---

**✅ Bueno:**

```javascript
description: "Busca productos en el catálogo por palabra clave. Retorna una lista de productos con nombre, precio y disponibilidad."
```

---

**Regla:**

Escribe como si le explicaras a otra persona.

---

# Mejores Prácticas - inputSchema

## Ser específico con los tipos

---

**Cada campo debe tener:**

- Tipo de dato
- Descripción
- Restricciones (si aplica)
- Si es obligatorio

---

**❌ Débil:**

```javascript
properties: { id: { type: "string" } }
```

---

**✅ Preciso:**

```javascript
properties: {
  productId: { 
    type: "string",
    description: "UUID del producto (formato: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)"
  },
  quantity: { 
    type: "integer",
    minimum: 1,
    maximum: 99,
    description: "Cantidad a añadir (1-99)"
  }
}
```

---

# Mejores Prácticas - readOnlyHint

## Indicar correctamente el tipo

---

**Regla simple:**

- Si la tool solo lee datos → `readOnlyHint: true`
- Si la tool modifica datos → omitir o `false`

---

**Por qué importa:**

- Los clientes pueden priorizar tools de solo lectura
- Herramientas de escritura pueden requerir confirmación
- Mejor experiencia de usuario

---

# Mejores Prácticas - Errores

## Retornar siempre errores estructurados

---

**❌ Nunca hacer:**

```javascript
try {
  return await operation();
} catch {
  return null; // Pierde información
}
```

---

**✅ Siempre hacer:**

```javascript
try {
  return { success: true, data: await operation() };
} catch (error) {
  return { 
    success: false, 
    error: error.message,
    code: error.code 
  };
}
```

---

# Anti-Patrones - Descripción Vaga

## Lo que NO hacer

---

**Demasiado corta:**

```javascript
description: "Hace algo"
```

---

**Sin contexto:**

```javascript
description: "Función helper"
```

---

**Técnica sin explicar:**

```javascript
description: "POST /api/v2/products"
```

---

**Nombres crípticos:**

```javascript
name: "fn1"
name: "process"
name: "helper"
```

---

# Anti-Patrones - inputSchema Débil

## Validación insuficiente

---

**Sin validación:**

```javascript
inputSchema: { type: "object" }
```

El modelo no sabe qué enviar.

---

**Sin required:**

```javascript
properties: { id: { type: "string" } }
```

¿El id es obligatorio o opcional?

---

**Sin límites:**

```javascript
quantity: { type: "integer" }
```

¿Puede ser 0? ¿Negativo? ¿Mil millones?

---

# Anti-Patrones - Errores Silenciosos

## No ocultar errores

---

**Ignorar errores:**

```javascript
try {
  return await operation();
} catch {
  return null; // ❌ Pierde información
}
```

---

**Lanzar excepción sin manejar:**

```javascript
execute: async (input) => {
  // Si falla, rompe todo
  return await riskyOperation(input);
}
```

---

**Correcto:**

```javascript
execute: async (input) => {
  try {
    return { success: true, data: await operation(input) };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

---

# Ejercicios - Introducción

## Práctica

---

A continuación, tres ejercicios:

1. Implementar herramienta de búsqueda
2. Implementar herramienta con confirmación
3. Implementar registro dinámico

---

# Ejercicio 1 - Búsqueda

## Implementar búsqueda de productos

---

**Objetivo:**

Crear una tool que busque productos en un array.

---

**Requisitos:**

- Nombre: `searchProducts`
- Parámetro obligatorio: `query` (string)
- Parámetro opcional: `category` (string)
- Retornar lista de productos que coincidan
- `readOnlyHint: true`

---

**Datos de prueba:**

```javascript
const productos = [
  { id: 1, nombre: "Laptop", categoria: "tech" },
  { id: 2, nombre: "Camiseta", categoria: "ropa" },
  { id: 3, nombre: "Libro", categoria: "libros" }
];
```

---

# Ejercicio 1 - Solución

## Implementación

---

```javascript
navigator.modelContext.registerTool({
  name: "searchProducts",
  description: "Busca productos por nombre o categoría",
  inputSchema: {
    type: "object",
    properties: {
      query: { 
        type: "string",
        description: "Palabra clave para buscar"
      },
      category: { 
        type: "string",
        description: "Categoría para filtrar"
      }
    },
    required: ["query"]
  },
  execute: async (input) => {
    let results = productos.filter(p =>
      p.nombre.toLowerCase().includes(input.query.toLowerCase())
    );
    if (input.category) {
      results = results.filter(p => p.categoria === input.category);
    }
    return { products: results, total: results.length };
  },
  annotations: { readOnlyHint: true }
});
```

---

# Ejercicio 2 - Confirmación

## Eliminar archivo con confirmación

---

**Objetivo:**

Crear una tool que elimine un archivo, pidiendo confirmación.

---

**Requisitos:**

- Nombre: `deleteFile`
- Parámetro obligatorio: `filename` (string)
- Mostrar diálogo de confirmación
- Si confirma, eliminar
- Retornar resultado

---

# Ejercicio 2 - Solución

## Implementación

---

```javascript
navigator.modelContext.registerTool({
  name: "deleteFile",
  description: "Elimina un archivo con confirmación del usuario",
  inputSchema: {
    type: "object",
    properties: {
      filename: { 
        type: "string",
        description: "Nombre del archivo a eliminar"
      }
    },
    required: ["filename"]
  },
  execute: async (input, client) => {
    const confirmed = await client.requestUserInteraction(
      async () => confirm(`¿Eliminar ${input.filename}?`)
    );
    if (!confirmed) {
      return { cancelled: true };
    }
    await fs.unlink(input.filename);
    return { deleted: true, filename: input.filename };
  }
});
```

---

# Ejercicio 3 - Registro Dinámico

## Herramientas según estado

---

**Objetivo:**

Implementar registro y eliminación de tools según login/logout.

---

**Requisitos:**

- Al hacer login: registrar `getUserOrders`
- Al hacer logout: eliminar `getUserOrders`

---

# Ejercicio 3 - Solución

## Implementación

---

```javascript
let currentUser = null;

function onUserLogin(user) {
  currentUser = user;
  
  navigator.modelContext.registerTool({
    name: "getUserOrders",
    description: "Obtiene el historial de pedidos del usuario actual",
    inputSchema: {
      type: "object",
      properties: {
        limit: { 
          type: "integer",
          description: "Número máximo de pedidos a retornar"
        }
      }
    },
    execute: async (input) => {
      const limit = input.limit || 10;
      return { 
        orders: await api.getOrders(currentUser.id, limit) 
      };
    },
    annotations: { readOnlyHint: true }
  });
}

function onUserLogout() {
  currentUser = null;
  navigator.modelContext.unregisterTool("getUserOrders");
}
```

---

# Resumen - Puntos Clave

## Lo más importante

---

1. **MCP** es un estándar abierto para conectar IAs con herramientas

2. **WebMCP** lleva MCP al navegador - registra funciones JS como tools

3. **Tres primitivas**: Tools, Resources, Prompts

4. **readOnlyHint** indica si la tool modifica estado

5. **requestUserInteraction** permite pedir confirmación

---

6. **Testing API** para depurar en desarrollo

7. **Reutiliza lógica frontend** sin backend extra

8. **HTTPS requerido** (SecureContext)

9. **Solo top-level contexts** - no iframes

10. **WebMCP y Backend MCP son complementarios**

---

# Resumen - Continuación

## Más puntos clave

---

11. **Key Terminology**: Agent, Model Context Provider, Tool Definition, Actuation

12. **Security Boundaries**: Site→Browser y Agent→Site

13. **Model Poisoning Risk**: pregunta abierta en el spec

14. **Future Roadmap**: Declarative WebMCP, PWAs, Background Providers

15. **Spec Status**: Draft Community Group Report, no W3C Standard aún

---

# Próximos Pasos

---

1. Habilitar flag WebMCP en Chrome (chrome://flags)

2. Probar con WebMCP Inspector

3. Implementar tools en tu app

4. Combinar con Backend MCP según necesites

5. Contribuir al spec W3C

---

# Cierre

---

**Model Context Protocol (MCP)**

*Conectando IAs con el mundo, un estándar a la vez.*

---

**Referencia oficial:**

W3C Community Group Report - 9 March 2026

webfuse.com/webmcp-cheat-sheet

---

**Preguntas y práctica:** ¡Ahora es tu turno!