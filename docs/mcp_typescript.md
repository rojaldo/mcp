# MCP TypeScript SDK - Guía Completa

## Del Fundamento a la Implementación Profesional

---

# Portada

## MCP TypeScript SDK

### Guía Completa para Desarrolladores

---

**Basado en el repositorio oficial:**  
https://github.com/modelcontextprotocol/typescript-sdk

---

**Duración estimada: 2 horas**

---

# Agenda

## Contenido del curso

---

1. **Introducción** (15 min) - ¿Qué es MCP TypeScript SDK?

2. **Instalación y Configuración** (10 min) - Setup del entorno

3. **McpServer: Conceptos Básicos** (20 min) - El servidor MCP

4. **Tools: Creando Herramientas** (25 min) - La primitiva más importante

5. **Resources: Exponiendo Datos** (15 min) - Contexto para el modelo

6. **Prompts: Plantillas Predefinidas** (10 min) - Interacciones reutilizables

7. **Context: Capacidades Avanzadas** (15 min) - Logging, progreso, sampling

8. **Transports: stdio, Streamable HTTP** (15 min) - Modos de comunicación

9. **Cliente MCP** (20 min) - Conectando a servidores

10. **Despliegue y Producción** (15 min) - Seguridad, OAuth, patterns

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

# MCP TypeScript SDK

## Implementación oficial en TypeScript

---

El SDK de TypeScript implementa el protocolo MCP completo, facilitando:

---

✅ Crear servidores que exponen resources, prompts y tools

✅ Crear clientes que se conectan a cualquier servidor

✅ Usar transports estándar: stdio, SSE, Streamable HTTP

✅ Manejar todos los mensajes del protocolo MCP

---

# ¿Por qué usar el SDK de TypeScript?

---

### Ventajas principales

---

**1. McpServer** - API fluida con métodos de registro

```typescript
import { McpServer } from '@modelcontextprotocol/server';

const server = new McpServer({ name: 'mi-servidor', version: '1.0.0' });

server.registerTool('mi-tool', { ... }, async (args) => { ... });
```

---

**2. Zod para validación** - Schemas tipados con validación automática

---

**3. Múltiples transports** - stdio para local, HTTP para remoto

---

**4. Bidireccional** - Servidor puede hacer requests al cliente

---

**5. Autenticación OAuth** - Soporte completo para auth

---

# Arquitectura del SDK

## Paquetes principales

---

```
@modelcontextprotocol/server   → Servidor MCP (McpServer)
@modelcontextprotocol/client    → Cliente MCP (Client)
@modelcontextprotocol/node      → Transport para Node.js
@modelcontextprotocol/express   → Integración Express
@modelcontextprotocol/hono      → Integración Hono
```

---

# PARTE 2

## Instalación y Configuración

---

# Requisitos Previos

---

### Necesitas:

- Node.js 18+ o Bun
- npm, yarn, pnpm o bun

---

# Instalación

## Dependencias principales

---

### Para servidores

```bash
npm install @modelcontextprotocol/server
npm install @modelcontextprotocol/node  # Transport Node.js
npm install zod                          # Validación
```

---

### Para clientes

```bash
npm install @modelcontextprotocol/client
```

---

### Para integración Express

```bash
npm install @modelcontextprotocol/express
```

---

# Imports necesarios

## Configuración base

---

```typescript
import { randomUUID } from 'node:crypto';

import { createMcpExpressApp } from '@modelcontextprotocol/express';
import { NodeStreamableHTTPServerTransport } from '@modelcontextprotocol/node';
import type { CallToolResult, ResourceLink } from '@modelcontextprotocol/server';
import { 
  completable, 
  McpServer, 
  ResourceTemplate, 
  StdioServerTransport 
} from '@modelcontextprotocol/server';
import * as z from 'zod/v4';
```

---

# PARTE 3

## McpServer: Conceptos Básicos

---

# Crear un servidor

## Pasos fundamentales

---

Construir un servidor MCP requiere 3 pasos:

---

**1.** Crear un `McpServer` y registrar tools, resources, prompts

**2.** Crear un transport (stdio o HTTP)

**3.** Conectar servidor con `server.connect(transport)`

---

# Crear McpServer

## Inicialización básica

---

```typescript
import { McpServer } from '@modelcontextprotocol/server';

const server = new McpServer({ 
  name: 'mi-servidor', 
  version: '1.0.0' 
});
```

---

**Con opciones:**

```typescript
const server = new McpServer(
  { name: 'db-server', version: '1.0.0' },
  {
    instructions: 'Siempre llama a list_tables antes de ejecutar queries.',
    capabilities: { 
      logging: {},
      sampling: {}
    }
  }
);
```

---

# Instructions

## Guías para el cliente

---

Las instructions describen cómo usar el servidor:

- Relaciones entre tools
- Patrones de workflow
- Restricciones importantes

---

```typescript
const server = new McpServer(
  { name: 'db-server', version: '1.0.0' },
  {
    instructions: `
      Siempre llama a list_tables antes de ejecutar queries.
      Usa validate_schema antes de migrate_schema.
      Resultados limitados a 1000 filas.
    `
  }
);
```

---

# PARTE 4

## Tools: Creando Herramientas

---

# ¿Qué son las Tools?

## Funciones que el LLM puede ejecutar

---

Las tools son la forma principal en que los LLMs interactúan con tu aplicación:

---

✅ Realizar cálculos

✅ Consultar APIs externas

✅ Modificar datos

✅ Generar efectos

---

# Registrar una Tool

## Con Zod schema

---

```typescript
import * as z from 'zod/v4';

server.registerTool(
  'calculate-bmi',
  {
    title: 'BMI Calculator',
    description: 'Calcula el índice de masa corporal',
    inputSchema: z.object({
      weightKg: z.number(),
      heightM: z.number()
    }),
    outputSchema: z.object({ 
      bmi: z.number() 
    })
  },
  async ({ weightKg, heightM }) => {
    const bmi = weightKg / (heightM * heightM);
    return {
      content: [{ 
        type: 'text', 
        text: JSON.stringify({ bmi }) 
      }],
      structuredContent: { bmi }
    };
  }
);
```

---

# Input Schema con Zod

## Validación automática

---

Zod genera el JSON Schema automáticamente y valida los inputs:

---

```typescript
server.registerTool(
  'create-user',
  {
    description: 'Crea un nuevo usuario',
    inputSchema: z.object({
      name: z.string().min(1).max(100),
      email: z.string().email(),
      age: z.number().int().min(0).max(150).optional(),
      role: z.enum(['user', 'admin', 'moderator']).default('user')
    })
  },
  async ({ name, email, age, role }) => {
    // Los argumentos ya están validados
    return { content: [{ type: 'text', text: `Usuario ${name} creado` }] };
  }
);
```

---

# Output Schema

## Structured output

---

Define el schema de salida para resultados estructurados:

---

```typescript
server.registerTool(
  'get-weather',
  {
    description: 'Obtiene el clima de una ciudad',
    inputSchema: z.object({ city: z.string() }),
    outputSchema: z.object({
      temperature: z.number(),
      humidity: z.number(),
      condition: z.string()
    })
  },
  async ({ city }) => {
    const data = await fetchWeather(city);
    return {
      content: [{ 
        type: 'text', 
        text: JSON.stringify(data) 
      }],
      structuredContent: data
    };
  }
);
```

---

**Nota:** Usa `type` en lugar de `interface` para structuredContent.

---

# ResourceLink Outputs

## Referencias sin embed

---

Para recursos grandes, devuelve links en lugar de contenido:

---

```typescript
import type { ResourceLink } from '@modelcontextprotocol/server';

server.registerTool(
  'list-files',
  {
    description: 'Lista archivos como resource links'
  },
  async (): Promise<CallToolResult> => {
    const links: ResourceLink[] = [
      {
        type: 'resource_link',
        uri: 'file:///projects/readme.md',
        name: 'README',
        mimeType: 'text/markdown'
      },
      {
        type: 'resource_link',
        uri: 'file:///projects/config.json',
        name: 'Config',
        mimeType: 'application/json'
      }
    ];
    return { content: links };
  }
);
```

---

# Tool Annotations

## Metadatos de comportamiento

---

Las annotations indican el comportamiento de la tool:

---

```typescript
server.registerTool(
  'delete-file',
  {
    description: 'Elimina un archivo del proyecto',
    inputSchema: z.object({ path: z.string() }),
    annotations: {
      title: 'Delete File',
      destructiveHint: true,    // Puede destruir datos
      idempotentHint: true      // Múltiples llamadas = mismo resultado
    }
  },
  async ({ path }) => {
    // ... eliminar archivo
    return { content: [{ type: 'text', text: `Deleted ${path}` }] };
  }
);
```

---

**Annotations disponibles:**

| Annotation | Significado |
|------------|-------------|
| `readOnlyHint` | Solo lectura, sin efectos |
| `destructiveHint` | Puede destruir datos |
| `idempotentHint` | Idempotente |
| `openWorldHint` | Accede a recursos externos |

---

# Error Handling

## Manejo de errores

---

Devuelve `isError: true` para errores que el LLM puede ver:

---

```typescript
server.registerTool(
  'fetch-data',
  {
    description: 'Obtiene datos de una URL',
    inputSchema: z.object({ url: z.string() })
  },
  async ({ url }): Promise<CallToolResult> => {
    try {
      const res = await fetch(url);
      if (!res.ok) {
        return {
          content: [{ 
            type: 'text', 
            text: `HTTP ${res.status}: ${res.statusText}` 
          }],
          isError: true  // El LLM ve este error
        };
      }
      const text = await res.text();
      return { content: [{ type: 'text', text }] };
    } catch (error) {
      return {
        content: [{ 
          type: 'text', 
          text: `Failed: ${error instanceof Error ? error.message : String(error)}` 
        }],
        isError: true
      };
    }
  }
);
```

---

# PARTE 5

## Resources: Exponiendo Datos

---

# ¿Qué son los Resources?

## Datos de solo lectura

---

Los resources exponen datos que la aplicación puede adjuntar como contexto:

---

- Archivos
- Schemas de base de datos
- Configuración
- Documentación

---

**A diferencia de tools:**

- Solo lectura
- Controlados por la aplicación (no el LLM)
- Como endpoints GET

---

# Resource Estático

## URI fija

---

```typescript
server.registerResource(
  'config',
  'config://app',
  {
    title: 'Application Config',
    description: 'Configuración de la aplicación',
    mimeType: 'application/json'
  },
  async (uri) => ({
    contents: [{ 
      uri: uri.href, 
      text: JSON.stringify({ theme: 'dark', lang: 'es' }) 
    }]
  })
);
```

---

# Resource Template

## URI dinámica con parámetros

---

```typescript
import { ResourceTemplate } from '@modelcontextprotocol/server';

server.registerResource(
  'user-profile',
  new ResourceTemplate('user://{userId}/profile', {
    list: async () => ({
      resources: [
        { uri: 'user://123/profile', name: 'Alice' },
        { uri: 'user://456/profile', name: 'Bob' }
      ]
    })
  }),
  {
    title: 'User Profile',
    description: 'Datos del perfil de usuario',
    mimeType: 'application/json'
  },
  async (uri, { userId }) => ({
    contents: [{
      uri: uri.href,
      text: JSON.stringify({ userId, name: 'Example User' })
    }]
  })
);
```

---

# ResourceTemplate

## Patrones de URI

---

| Template | Ejemplo URI |
|----------|-------------|
| `user://{userId}/profile` | `user://123/profile` |
| `file://{path}` | `file:///docs/readme.md` |
| `repo://{owner}/{repo}/issues` | `repo://microsoft/vscode/issues` |

---

El callback recibe los parámetros extraídos automáticamente.

---

# PARTE 6

## Prompts: Plantillas Predefinidas

---

# ¿Qué son los Prompts?

## Templates reutilizables

---

Los prompts son plantillas de mensajes que:

- Estructuran interacciones comunes
- El usuario las invoca explícitamente
- Pueden tener argumentos

---

```typescript
server.registerPrompt(
  'review-code',
  {
    title: 'Code Review',
    description: 'Revisa código buscando mejores prácticas',
    argsSchema: z.object({
      code: z.string()
    })
  },
  ({ code }) => ({
    messages: [{
      role: 'user' as const,
      content: {
        type: 'text' as const,
        text: `Por favor revisa este código:\n\n${code}`
      }
    }]
  })
);
```

---

# Prompts con múltiples mensajes

---

```typescript
server.registerPrompt(
  'debug-error',
  {
    title: 'Debug Assistant',
    description: 'Ayuda a debuggear errores',
    argsSchema: z.object({ error: z.string() })
  },
  ({ error }) => ({
    messages: [
      { 
        role: 'user' as const, 
        content: { type: 'text' as const, text: 'Estoy viendo este error:' } 
      },
      { 
        role: 'user' as const, 
        content: { type: 'text' as const, text: error } 
      },
      { 
        role: 'assistant' as const, 
        content: { type: 'text' as const, text: 'Te ayudo a debuggear. ¿Qué has intentado?' } 
      }
    ]
  })
);
```

---

# Completions

## Autocompletado de argumentos

---

Usa `completable()` para ofrecer autocompletado:

---

```typescript
import { completable } from '@modelcontextprotocol/server';

server.registerPrompt(
  'review-code',
  {
    title: 'Code Review',
    description: 'Revisa código',
    argsSchema: z.object({
      language: completable(
        z.string().describe('Lenguaje de programación'),
        (value) => ['typescript', 'javascript', 'python', 'rust', 'go']
          .filter(lang => lang.startsWith(value))
      )
    })
  },
  ({ language }) => ({
    messages: [{
      role: 'user' as const,
      content: { 
        type: 'text' as const, 
        text: `Revisa este código ${language} buscando mejores prácticas.` 
      }
    }]
  })
);
```

---

# PARTE 7

## Context: Capacidades Avanzadas

---

# El objeto Context

## Acceso a capacidades MCP

---

El contexto se pasa como segundo argumento al handler:

---

```typescript
server.registerTool(
  'my-tool',
  { 
    description: 'Tool con contexto',
    inputSchema: z.object({ data: z.string() })
  },
  async ({ data }, ctx) => {
    // ctx proporciona acceso a capacidades MCP
    await ctx.mcpReq.log('info', `Procesando: ${data}`);
    return { content: [{ type: 'text', text: 'Procesado' }] };
  }
);
```

---

# Logging

## Enviar mensajes de log

---

Primero declara la capability:

---

```typescript
const server = new McpServer(
  { name: 'my-server', version: '1.0.0' },
  { capabilities: { logging: {} } }
);
```

---

Luego usa el logging en cualquier handler:

---

```typescript
server.registerTool(
  'fetch-data',
  {
    description: 'Obtiene datos de una API',
    inputSchema: z.object({ url: z.string() })
  },
  async ({ url }, ctx): Promise<CallToolResult> => {
    await ctx.mcpReq.log('info', `Fetching ${url}`);
    
    const res = await fetch(url);
    await ctx.mcpReq.log('debug', `Response status: ${res.status}`);
    
    const text = await res.text();
    return { content: [{ type: 'text', text }] };
  }
);
```

---

# Progress Reporting

## Actualizaciones de progreso

---

Reporta progreso en operaciones largas:

---

```typescript
server.registerTool(
  'process-files',
  {
    description: 'Procesa archivos con actualizaciones',
    inputSchema: z.object({ files: z.array(z.string()) })
  },
  async ({ files }, ctx): Promise<CallToolResult> => {
    const progressToken = ctx.mcpReq._meta?.progressToken;

    for (let i = 0; i < files.length; i++) {
      // ... procesar files[i] ...

      if (progressToken !== undefined) {
        await ctx.mcpReq.notify({
          method: 'notifications/progress',
          params: {
            progressToken,
            progress: i + 1,
            total: files.length,
            message: `Processed ${files[i]}`
          }
        });
      }
    }

    return { content: [{ type: 'text', text: `Processed ${files.length} files` }] };
  }
);
```

---

# Sampling

## Pedir al LLM que genere texto

---

El servidor puede pedir al cliente que genere texto:

---

```typescript
server.registerTool(
  'summarize',
  {
    description: 'Resume texto usando el LLM del cliente',
    inputSchema: z.object({ text: z.string() })
  },
  async ({ text }, ctx): Promise<CallToolResult> => {
    const response = await ctx.mcpReq.requestSampling({
      messages: [{
        role: 'user',
        content: {
          type: 'text',
          text: `Por favor resume:\n\n${text}`
        }
      }],
      maxTokens: 500
    });
    
    return {
      content: [{
        type: 'text',
        text: `Model (${response.model}): ${JSON.stringify(response.content)}`
      }]
    };
  }
);
```

---

# Elicitation

## Pedir input al usuario

---

Pide datos directamente al usuario:

---

```typescript
server.registerTool(
  'collect-feedback',
  {
    description: 'Recopila feedback del usuario',
    inputSchema: z.object({})
  },
  async (_args, ctx): Promise<CallToolResult> => {
    const result = await ctx.mcpReq.elicitInput({
      mode: 'form',
      message: 'Por favor comparte tu feedback:',
      requestedSchema: {
        type: 'object',
        properties: {
          rating: {
            type: 'number',
            title: 'Rating (1-5)',
            minimum: 1,
            maximum: 5
          },
          comment: { 
            type: 'string', 
            title: 'Comentario' 
          }
        },
        required: ['rating']
      }
    });
    
    if (result.action === 'accept') {
      return {
        content: [{ 
          type: 'text', 
          text: `Gracias! ${JSON.stringify(result.content)}` 
        }]
      };
    }
    return { content: [{ type: 'text', text: 'Feedback declined.' }] };
  }
);
```

---

# Roots

## Directorios del workspace

---

Descubre los directorios del workspace del cliente:

---

```typescript
server.registerTool(
  'list-workspace-files',
  {
    description: 'Lista archivos en todos los roots',
    inputSchema: z.object({})
  },
  async (_args, _ctx): Promise<CallToolResult> => {
    const { roots } = await server.server.listRoots();
    const summary = roots.map(r => `${r.name ?? r.uri}: ${r.uri}`).join('\n');
    return { content: [{ type: 'text', text: summary }] };
  }
);
```

---

# PARTE 8

## Transports: Modos de Comunicación

---

# ¿Qué son los Transports?

## Mecanismos de conexión

---

MCP soporta dos transport mechanisms:

---

| Transport | Uso | Características |
|-----------|-----|-----------------|
| **stdio** | Claude Desktop | Simple, bidireccional |
| **Streamable HTTP** | Servidores remotos | HTTP moderno, escalable |

---

# stdio Transport

## Para Claude Desktop

---

Comunicación via stdin/stdout:

---

```typescript
import { StdioServerTransport } from '@modelcontextprotocol/server';

const server = new McpServer({ name: 'my-server', version: '1.0.0' });

const transport = new StdioServerTransport();
await server.connect(transport);
```

---

**Configuración en Claude Desktop:**

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/server.js"]
    }
  }
}
```

---

# Streamable HTTP Transport

## Para servidores remotos

---

HTTP moderno con sesiones:

---

```typescript
import { NodeStreamableHTTPServerTransport } from '@modelcontextprotocol/node';
import { randomUUID } from 'node:crypto';

const server = new McpServer({ name: 'my-server', version: '1.0.0' });

const transport = new NodeStreamableHTTPServerTransport({
  sessionIdGenerator: () => randomUUID()  // Con estado
  // sessionIdGenerator: undefined         // Sin estado
});

await server.connect(transport);
```

---

# Express Integration

## createMcpExpressApp

---

La forma más fácil de crear un servidor HTTP:

---

```typescript
import { createMcpExpressApp } from '@modelcontextprotocol/express';

// Con protección DNS rebinding automática
const app = createMcpExpressApp({
  host: '127.0.0.1',  // localhost con protección
  port: 3000
});

// Montar servidor MCP
app.mcp.mount(server);

app.listen(3000, () => {
  console.log('MCP server running on port 3000');
});
```

---

# Configuración HTTP

---

```typescript
// Stateless (más simple, sin resumabilidad)
const transport = new NodeStreamableHTTPServerTransport({
  sessionIdGenerator: undefined,
  enableJsonResponse: true  // JSON en lugar de SSE
});

// Stateful (con sesiones)
const transport = new NodeStreamableHTTPServerTransport({
  sessionIdGenerator: () => randomUUID()
});
```

---

# CORS para browsers

---

```typescript
import { createMcpExpressApp } from '@modelcontextprotocol/express';

const app = createMcpExpressApp();

// CORS ya está configurado por defecto
// Expone headers: Mcp-Session-Id, etc.
```

---

# Shutdown

## Cierre graceful

---

Para servidores HTTP con sesiones:

---

```typescript
const httpServer = app.listen(3000);

process.on('SIGINT', async () => {
  httpServer.close();  // No aceptar más conexiones
  
  // Cerrar todos los transports
  for (const [sessionId, transport] of transports) {
    await transport.close();
    transports.delete(sessionId);
  }
  
  process.exit(0);
});
```

---

Para stdio es más simple:

---

```typescript
process.on('SIGINT', async () => {
  await server.close();
  process.exit(0);
});
```

---

# PARTE 9

## Cliente MCP

---

# ¿Qué es el Cliente?

## Conectando a servidores MCP

---

El cliente MCP permite:

- Conectarse a servidores MCP
- Descubrir tools, resources, prompts
- Invocar tools y leer resources
- Manejar autenticación

---

# Conexión Streamable HTTP

---

```typescript
import { Client, StreamableHTTPClientTransport } from '@modelcontextprotocol/client';

const client = new Client({ name: 'my-client', version: '1.0.0' });

const transport = new StreamableHTTPClientTransport(
  new URL('http://localhost:3000/mcp')
);

await client.connect(transport);
```

---

# Conexión stdio

---

```typescript
import { Client, StdioClientTransport } from '@modelcontextprotocol/client';

const client = new Client({ name: 'my-client', version: '1.0.0' });

const transport = new StdioClientTransport({
  command: 'node',
  args: ['server.js']
});

await client.connect(transport);
```

---

# SSE Fallback

## Para servidores legacy

---

```typescript
const baseUrl = new URL(url);

try {
  // Intentar Streamable HTTP primero
  const client = new Client({ name: 'my-client', version: '1.0.0' });
  const transport = new StreamableHTTPClientTransport(baseUrl);
  await client.connect(transport);
  return { client, transport };
} catch {
  // Fallback a SSE
  const client = new Client({ name: 'my-client', version: '1.0.0' });
  const transport = new SSEClientTransport(baseUrl);
  await client.connect(transport);
  return { client, transport };
}
```

---

# Listar Tools

---

```typescript
const allTools: Tool[] = [];
let cursor: string | undefined;

do {
  const { tools, nextCursor } = await client.listTools({ cursor });
  allTools.push(...tools);
  cursor = nextCursor;
} while (cursor);

console.log('Tools disponibles:', allTools.map(t => t.name));
```

---

# Invocar una Tool

---

```typescript
const result = await client.callTool({
  name: 'calculate-bmi',
  arguments: { weightKg: 70, heightM: 1.75 }
});

// Verificar errores
if (result.isError) {
  console.error('Tool error:', result.content);
  return;
}

// Usar structured output si está disponible
if (result.structuredContent) {
  console.log(result.structuredContent);  // { bmi: 22.86 }
}

console.log(result.content);
```

---

# Progress Tracking

---

```typescript
const result = await client.callTool(
  { name: 'long-operation', arguments: {} },
  {
    onprogress: ({ progress, total }) => {
      console.log(`Progress: ${progress}/${total ?? '?'}`);
    },
    resetTimeoutOnProgress: true,  // Mantener vivo mientras progresa
    maxTotalTimeout: 600_000        // Timeout máximo absoluto
  }
);
```

---

# Listar y Leer Resources

---

```typescript
// Listar resources
const allResources: Resource[] = [];
let cursor: string | undefined;

do {
  const { resources, nextCursor } = await client.listResources({ cursor });
  allResources.push(...resources);
  cursor = nextCursor;
} while (cursor);

// Leer un resource
const { contents } = await client.readResource({ 
  uri: 'config://app' 
});

for (const item of contents) {
  console.log(item);
}
```

---

# Subscribirse a cambios

---

```typescript
await client.subscribeResource({ uri: 'config://app' });

client.setNotificationHandler(
  'notifications/resources/updated', 
  async (notification) => {
    if (notification.params.uri === 'config://app') {
      const { contents } = await client.readResource({ uri: 'config://app' });
      console.log('Config updated:', contents);
    }
  }
);

// Después: dejar de recibir updates
await client.unsubscribeResource({ uri: 'config://app' });
```

---

# Obtener Prompts

---

```typescript
// Listar prompts
const { prompts } = await client.listPrompts();

// Obtener un prompt con argumentos
const { messages } = await client.getPrompt({
  name: 'review-code',
  arguments: { 
    code: 'console.log("hello")',
    language: 'typescript'
  }
});

console.log(messages);
```

---

# Completions

## Autocompletado

---

```typescript
const { completion } = await client.complete({
  ref: {
    type: 'ref/prompt',
    name: 'review-code'
  },
  argument: {
    name: 'language',
    value: 'type'
  }
});

console.log(completion.values);  // ['typescript']
```

---

# Manejo de Errores

---

```typescript
import { ProtocolError, SdkError, SdkErrorCode } from '@modelcontextprotocol/client';

try {
  const result = await client.callTool({
    name: 'fetch-data',
    arguments: { url: 'https://example.com' }
  });

  // Error de tool (el LLM puede verlo)
  if (result.isError) {
    console.error('Tool error:', result.content);
    return;
  }

  console.log('Success:', result.content);
} catch (error) {
  // Error de protocolo (del servidor)
  if (error instanceof ProtocolError) {
    console.error(`Protocol error ${error.code}: ${error.message}`);
  } 
  // Error del SDK (timeout, conexión cerrada, etc.)
  else if (error instanceof SdkError) {
    console.error(`SDK error [${error.code}]: ${error.message}`);
  } else {
    throw error;
  }
}
```

---

# PARTE 10

## Despliegue y Producción

---

# DNS Rebinding Protection

## Seguridad crítica

---

Todos los servidores MCP en localhost deben usar protección DNS rebinding:

---

```typescript
import { createMcpExpressApp } from '@modelcontextprotocol/express';

// Protección automática para localhost
const app = createMcpExpressApp();  // 127.0.0.1 por defecto

// También protegido para localhost
const appLocal = createMcpExpressApp({ host: 'localhost' });

// Sin protección automática para 0.0.0.0
const appOpen = createMcpExpressApp({ 
  host: '0.0.0.0',
  allowedHosts: ['localhost', '127.0.0.1', 'myhost.local']
});
```

---

# Autenticación

## AuthProvider

---

Para servidores que requieren autenticación:

---

### Bearer Token simple

```typescript
import type { AuthProvider } from '@modelcontextprotocol/client';

const authProvider: AuthProvider = { 
  token: async () => getStoredToken() 
};

const transport = new StreamableHTTPClientTransport(
  new URL('http://localhost:3000/mcp'), 
  { authProvider }
);
```

---

### Client Credentials

```typescript
import { ClientCredentialsProvider } from '@modelcontextprotocol/client';

const authProvider = new ClientCredentialsProvider({
  clientId: 'my-service',
  clientSecret: 'my-secret'
});

const transport = new StreamableHTTPClientTransport(
  new URL('http://localhost:3000/mcp'), 
  { authProvider }
);
```

---

### Private Key JWT

```typescript
import { PrivateKeyJwtProvider } from '@modelcontextprotocol/client';

const authProvider = new PrivateKeyJwtProvider({
  clientId: 'my-service',
  privateKey: pemEncodedKey,
  algorithm: 'RS256'
});

const transport = new StreamableHTTPClientTransport(
  new URL('http://localhost:3000/mcp'), 
  { authProvider }
);
```

---

# Capabilities del Cliente

## Declarar capacidades

---

Para responder a requests del servidor:

---

```typescript
const client = new Client(
  { name: 'my-client', version: '1.0.0' },
  {
    capabilities: {
      sampling: {},        // Puede generar texto
      elicitation: { form: {} },  // Puede pedir input
      roots: {}            // Puede exponer directorios
    }
  }
);
```

---

# Sampling Handler

## Responder a sampling requests

---

```typescript
client.setRequestHandler('sampling/createMessage', async (request) => {
  const lastMessage = request.params.messages.at(-1);
  console.log('Sampling request:', lastMessage);

  // En producción, enviar a tu LLM aquí
  return {
    model: 'my-model',
    role: 'assistant' as const,
    content: {
      type: 'text' as const,
      text: 'Respuesta del modelo'
    }
  };
});
```

---

# Elicitation Handler

## Responder a input requests

---

```typescript
client.setRequestHandler('elicitation/create', async (request) => {
  console.log('Server asks:', request.params.message);

  if (request.params.mode === 'form') {
    // Mostrar formulario al usuario
    console.log('Schema:', request.params.requestedSchema);
    return { action: 'accept', content: { confirm: true } };
  }

  return { action: 'decline' };
});
```

---

# Roots Handler

## Exponer directorios

---

```typescript
client.setRequestHandler('roots/list', async () => ({
  roots: [
    { uri: 'file:///home/user/projects/my-app', name: 'My App' },
    { uri: 'file:///home/user/data', name: 'Data' }
  ]
}));

// Notificar cuando cambian los roots
await client.sendRootsListChanged();
```

---

# Notifications

## Manejar notificaciones

---

```typescript
// Logs del servidor
client.setNotificationHandler('notifications/message', (notification) => {
  const { level, data } = notification.params;
  console.log(`[${level}]`, data);
});

// Lista de resources cambió
client.setNotificationHandler('notifications/resources/list_changed', async () => {
  const { resources } = await client.listResources();
  console.log('Resources changed:', resources.length);
});

// Cambiar nivel de log
await client.setLoggingLevel('warning');
```

---

# listChanged

## Tracking automático

---

Opción para mantener cache sincronizado:

---

```typescript
const client = new Client(
  { name: 'my-client', version: '1.0.0' },
  {
    listChanged: {
      tools: {
        onChanged: (error, tools) => {
          if (error) {
            console.error('Failed to refresh tools:', error);
            return;
          }
          console.log('Tools updated:', tools);
        }
      },
      prompts: {
        onChanged: (error, prompts) => {
          console.log('Prompts updated:', prompts);
        }
      },
      resources: {
        onChanged: (error, resources) => {
          console.log('Resources updated:', resources);
        }
      }
    }
  }
);
```

---

# Timeouts

---

```typescript
try {
  const result = await client.callTool(
    { name: 'slow-task', arguments: {} },
    { timeout: 120_000 }  // 2 minutos en lugar de 60 segundos
  );
} catch (error) {
  if (error instanceof SdkError && error.code === SdkErrorCode.RequestTimeout) {
    console.error('Request timed out');
  }
}
```

---

# Middleware

## Interceptación de fetch

---

```typescript
import { createMiddleware, applyMiddlewares } from '@modelcontextprotocol/client';

const authMiddleware = createMiddleware(async (next, input, init) => {
  const headers = new Headers(init?.headers);
  headers.set('X-Custom-Header', 'my-value');
  return next(input, { ...init, headers });
});

const transport = new StreamableHTTPClientTransport(
  new URL('http://localhost:3000/mcp'),
  { fetch: applyMiddlewares(authMiddleware)(fetch) }
);
```

---

# Ejemplo Completo

## Servidor con todo

---

```typescript
import { randomUUID } from 'node:crypto';
import { createMcpExpressApp } from '@modelcontextprotocol/express';
import { 
  McpServer, 
  ResourceTemplate, 
  completable 
} from '@modelcontextprotocol/server';
import * as z from 'zod/v4';

// Crear servidor
const server = new McpServer(
  { name: 'complete-server', version: '1.0.0' },
  { 
    capabilities: { logging: {} },
    instructions: 'Usa list_items antes de crear nuevos items.'
  }
);

// Tool
server.registerTool(
  'create-item',
  {
    description: 'Crea un nuevo item',
    inputSchema: z.object({
      name: z.string(),
      quantity: z.number().int().positive()
    })
  },
  async ({ name, quantity }) => ({
    content: [{ type: 'text', text: `Created ${name} x${quantity}` }]
  })
);

// Resource
server.registerResource(
  'items',
  new ResourceTemplate('items://{category}', {
    list: async () => ({
      resources: [
        { uri: 'items://electronics', name: 'Electronics' },
        { uri: 'items://books', name: 'Books' }
      ]
    })
  }),
  { mimeType: 'application/json' },
  async (uri, { category }) => ({
    contents: [{ uri: uri.href, text: JSON.stringify({ category, items: [] }) }]
  })
);

// Prompt
server.registerPrompt(
  'summarize-items',
  {
    description: 'Resume items de una categoría',
    argsSchema: z.object({
      category: completable(z.string(), (v) => 
        ['electronics', 'books'].filter(c => c.startsWith(v))
      )
    })
  },
  ({ category }) => ({
    messages: [{
      role: 'user' as const,
      content: { type: 'text' as const, text: `Resume items de ${category}` }
    }]
  })
);

// Crear app Express
const app = createMcpExpressApp({ port: 3000 });
app.mcp.mount(server);

app.listen(3000, () => {
  console.log('MCP server running on http://localhost:3000');
});
```

---

# Recursos

## Documentación oficial

---

- **SDK TypeScript:** https://github.com/modelcontextprotocol/typescript-sdk
- **Protocolo MCP:** https://modelcontextprotocol.io
- **Especificación:** https://spec.modelcontextprotocol.io
- **Claude Code:** https://docs.anthropic.com/en/docs/claude-code

---

# Resumen

## Lo que aprendimos

---

✅ McpServer para crear servidores con tools, resources, prompts

✅ Zod para schemas de validación automáticos

✅ Context para logging, progreso, sampling, elicitation

✅ stdio para Claude Desktop, HTTP para servidores remotos

✅ Cliente MCP para conectar a cualquier servidor

✅ Autenticación OAuth y protección DNS rebinding

---

# ¡Gracias!

## Preguntas

---

**Próximos pasos:**

1. Instalar el SDK: `npm install @modelcontextprotocol/server`

2. Crear tu primer servidor con McpServer

3. Probar con diferentes transports

4. Conectar clientes y explorar

5. ¡Construir herramientas útiles!

---

**Código fuente de esta presentación:**

Basado en https://github.com/modelcontextprotocol/typescript-sdk

---