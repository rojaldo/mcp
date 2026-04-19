# Servidores MCP: Ecosistema y Proyectos Destacados

## Guía Completa de Official y Community Servers

---

# Portada

## Servidores MCP

### El Ecosistema de Herramientas para Model Context Protocol

---

**Duración estimada: 2 horas**

*De los servidores oficiales a los proyectos más populares de la comunidad*

---

# Agenda

## Contenido del curso

---

1. **Introducción** (10 min) - ¿Qué es awesome-mcp-servers?

2. **Servidores Oficiales** (30 min) - El ecosistema de modelcontextprotocol

3. **Filesystem & Database** (20 min) - Almacenamiento y datos

4. **Developer Tools** (20 min) - Herramientas de desarrollo

5. **Web & Browser** (15 min) - Automatización web

6. **AI & Knowledge** (15 min) - Memoria y conocimiento

7. **Cloud Services** (15 min) - Integraciones cloud

8. **Comunicación** (10 min) - Slack, Discord, Email

9. **Casos de Uso Prácticos** (15 min) - Ejemplos reales

10. **Resumen y Recursos** (10 min) - Cómo seguir

---

# PARTE 1: INTRODUCCIÓN

---

# ¿Qué es awesome-mcp-servers?

## La lista curada de servidores MCP

---

**awesome-mcp-servers** es un repositorio que recopila servidores MCP ordenados por popularidad y funcionalidad.

---

**Categorías principales:**

- 🏢 Servidores oficiales (modelcontextprotocol)
- 📁 Filesystem & Database
- 🔧 Developer Tools
- 🌐 Web & Browser
- 🤖 AI & Knowledge
- ☁️ Cloud Services
- 💬 Communication

---

**Métricas de popularidad:**

- Estrellas de GitHub
- Número de forks
- Actividad reciente
- Documentación

---

# Cómo Usar Esta Presentación

## Estructura de cada servidor

---

Para cada servidor presentaremos:

1. **Nombre y descripción** - Qué hace
2. **Estrellas** - Popularidad en GitHub
3. **Categoría** - Área de aplicación
4. **Instalación** - Cómo instalarlo
5. **Uso básico** - Ejemplo de configuración
6. **Casos de uso** - Cuándo usarlo

---

# PARTE 2: SERVIDORES OFICIALES

---

# El Ecosistema Oficial

## modelcontextprotocol en GitHub

---

**La organización `modelcontextprotocol` mantiene los servidores oficiales.**

---

**Características:**

- Mantenidos por el equipo de Anthropic
- Documentación completa
- Actualizaciones frecuentes
- Integración nativa con Claude

---

**Servidores oficiales principales:**

| Servidor | Función | Estrellas |
|----------|---------|-----------|
| filesystem | Acceso a archivos | ~3.5k |
| github | Integración GitHub | ~3.2k |
| postgresql | Base de datos PostgreSQL | ~2.8k |
| sqlite | Base de datos SQLite | ~2.5k |
| brave-search | Búsqueda web | ~2.2k |
| puppeteer | Automatización browser | ~2.0k |
| slack | Integración Slack | ~1.8k |
| google-drive | Google Drive | ~1.5k |
| memory | Memoria persistente | ~2.0k |

---

# Filesystem Server

## Acceso a archivos locales

---

**Repositorio:** `modelcontextprotocol/servers`

**Estrellas:** ~3,500+ ⭐

---

**Descripción:**

Permite a los modelos de IA leer, escribir y navegar sistemas de archivos locales.

---

**Funcionalidades:**

- Leer archivos de texto
- Escribir y crear archivos
- Listar directorios
- Buscar archivos por patrón
- Mover y copiar archivos

---

**Instalación:**

```bash
# Con Claude Desktop
# Añadir a claude_desktop_config.json:

{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/directory"
      ]
    }
  }
}
```

---

**Ejemplo de uso:**

```
Usuario: "Lee el archivo config.json y dime qué configuraciones hay"

Claude: [Usa la tool read_file del servidor filesystem]
        "He leído el archivo config.json. Contiene las siguientes configuraciones..."
```

---

**Casos de uso:**

- Análisis de código fuente
- Edición de archivos de configuración
- Gestión de documentos
- Logs del sistema
- Proyectos de desarrollo

---

# GitHub Server

## Integración con GitHub

---

**Repositorio:** `modelcontextprotocol/servers`

**Estrellas:** ~3,200+ ⭐

---

**Descripción:**

Permite interactuar con la API de GitHub para repositorios, issues, pull requests y más.

---

**Funcionalidades:**

- Crear y listar issues
- Crear y revisar pull requests
- Buscar repositorios
- Leer contenido de archivos
- Gestionar branches
- Ver commits

---

**Instalación:**

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "tu-personal-access-token"
      }
    }
  }
}
```

---

**Ejemplo de uso:**

```
Usuario: "Crea un issue en mi repo sobre el bug de autenticación"

Claude: [Usa create_issue]
        "He creado el issue #42 en tu repositorio con el título..."
```

---

**Casos de uso:**

- Gestión de proyectos
- Code review automatizado
- Seguimiento de bugs
- Documentación de repositorios
- Automatización de CI/CD

---

# PostgreSQL Server

## Base de datos PostgreSQL

---

**Repositorio:** `modelcontextprotocol/servers`

**Estrellas:** ~2,800+ ⭐

---

**Descripción:**

Conexión a bases de datos PostgreSQL para consultas y operaciones.

---

**Funcionalidades:**

- Ejecutar consultas SQL
- Listar tablas y esquemas
- Describir estructura de tablas
- Insertar y actualizar datos
- Crear y modificar tablas

---

**Instalación:**

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@host:5432/db"
      }
    }
  }
}
```

---

**Ejemplo de uso:**

```
Usuario: "¿Cuántos usuarios se registraron esta semana?"

Claude: [Usa query tool]
        "Se registraron 847 usuarios esta semana. El día con más registros..."
```

---

**Casos de uso:**

- Análisis de datos
- Reporting automatizado
- Migración de datos
- Auditoría de bases de datos
- Generación de informes

---

# SQLite Server

## Base de datos SQLite

---

**Repositorio:** `modelcontextprotocol/servers`

**Estrellas:** ~2,500+ ⭐

---

**Descripción:**

Conexión a bases de datos SQLite para consultas y operaciones locales.

---

**Funcionalidades:**

- Consultas SQL completas
- Creación de tablas
- Inserción masiva de datos
- Análisis de datos locales
- Exportación a otros formatos

---

**Instalación:**

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sqlite",
        "/path/to/database.db"
      ]
    }
  }
}
```

---

**Ventajas sobre PostgreSQL:**

- Sin servidor de base de datos
- Archivo único portable
- Ideal para desarrollo local
- Menor overhead

---

**Casos de uso:**

- Prototipado rápido
- Análisis de datos locales
- Aplicaciones offline
- Testing y desarrollo
- Archivos de configuración estructurados

---

# Brave Search Server

## Búsqueda web con Brave

---

**Repositorio:** `modelcontextprotocol/servers`

**Estrellas:** ~2,200+ ⭐

---

**Descripción:**

Permite realizar búsquedas web usando la API de Brave Search.

---

**Funcionalidades:**

- Búsqueda web con resultados orgánicos
- Filtrado por fecha, región
- Búsqueda de noticias
- Búsqueda de imágenes
- Resultados estructurados

---

**Instalación:**

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "tu-api-key"
      }
    }
  }
}
```

---

**Ejemplo de uso:**

```
Usuario: "Busca las últimas noticias sobre inteligencia artificial"

Claude: [Usa brave_search]
        "He encontrado las siguientes noticias sobre IA..."
```

---

**Casos de uso:**

- Investigación de temas
- Seguimiento de noticias
- Análisis de tendencias
- Verificación de hechos
- Recopilación de información

---

# Puppeteer Server

## Automatización de navegador

---

**Repositorio:** `modelcontextprotocol/servers`

**Estrellas:** ~2,000+ ⭐

---

**Descripción:**

Automatización de navegador web usando Puppeteer para navegación, capturas y scraping.

---

**Funcionalidades:**

- Navegar a URLs
- Capturar pantallazos
- Extraer contenido de páginas
- Interactuar con elementos
- Rellenar formularios
- Click y scroll

---

**Instalación:**

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    }
  }
}
```

---

**Ejemplo de uso:**

```
Usuario: "Haz una captura de pantalla de example.com"

Claude: [Usa puppeteer_navigate y puppeteer_screenshot]
        "He capturado la página. La imagen muestra..."
```

---

**Casos de uso:**

- Testing de aplicaciones web
- Scraping de datos
- Generación de PDFs
- Monitoreo de sitios web
- Automatización de tareas web

---

# Memory Server

## Memoria persistente

---

**Repositorio:** `modelcontextprotocol/servers`

**Estrellas:** ~2,000+ ⭐

---

**Descripción:**

Sistema de memoria persistente para que el modelo recuerde información entre sesiones.

---

**Funcionalidades:**

- Almacenar hechos y relaciones
- Recuperar información relevante
- Búsqueda semántica
- Grafos de conocimiento
- Persistencia entre sesiones

---

**Instalación:**

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

---

**Ejemplo de uso:**

```
Usuario: "Recuerda que mi proyecto se llama Aurora y usa PostgreSQL"

Claude: [Usa add_memory]
        "He guardado esa información. En futuras sesiones podré recordar..."

[En otra sesión]

Usuario: "¿Qué base de datos usa mi proyecto?"

Claude: [Usa read_memory]
        "Tu proyecto Aurora usa PostgreSQL, según lo que me contaste..."
```

---

**Casos de uso:**

- Preferencias de usuario
- Contexto de proyectos
- Información de contactos
- Historial de conversaciones
- Base de conocimiento personal

---

# Slack Server

## Integración con Slack

---

**Repositorio:** `modelcontextprotocol/servers`

**Estrellas:** ~1,800+ ⭐

---

**Descripción:**

Interactuar con Slack: enviar mensajes, leer canales, gestionar hilos.

---

**Funcionalidades:**

- Enviar mensajes a canales
- Leer mensajes de canales
- Responder a hilos
- Listar canales
- Buscar mensajes

---

**Instalación:**

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-tu-bot-token"
      }
    }
  }
}
```

---

**Ejemplo de uso:**

```
Usuario: "Envía un mensaje al canal #general diciendo que el deploy está listo"

Claude: [Usa send_message]
        "He enviado el mensaje al canal #general..."
```

---

**Casos de uso:**

- Notificaciones automatizadas
- Resumen de conversaciones
- Gestión de equipos
- Alertas del sistema
- Integración con workflows

---

# Google Drive Server

## Integración con Google Drive

---

**Repositorio:** `modelcontextprotocol/servers`

**Estrellas:** ~1,500+ ⭐

---

**Descripción:**

Leer y gestionar archivos en Google Drive.

---

**Funcionalidades:**

- Listar archivos y carpetas
- Leer contenido de archivos
- Buscar archivos
- Crear y subir archivos
- Compartir archivos

---

**Instalación:**

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "...",
        "GOOGLE_OAUTH_CLIENT_SECRET": "...",
        "GOOGLE_OAUTH_REDIRECT_URI": "..."
      }
    }
  }
}
```

---

**Ejemplo de uso:**

```
Usuario: "Busca el documento de requisitos del proyecto Aurora"

Claude: [Usa search_files]
        "He encontrado el documento 'Requisitos Aurora v2.docx'. ¿Quieres que lo lea?"
```

---

**Casos de uso:**

- Gestión documental
- Colaboración en equipo
- Backup de archivos
- Análisis de documentos
- Organización de proyectos

---

# PARTE 3: FILESYSTEM & DATABASE

---

# Filesystem Servers Populares

## Proyectos de la comunidad

---

### Filesystem Server (oficial)

Ya cubierto en la sección de oficiales.

---

### Desktop Commander

**Repositorio:** `wonderwhy-er/desktop-commander`

**Estrellas:** ~1,800+ ⭐

**Descripción:**

Control de aplicaciones de escritorio con interfaz gráfica.

---

**Funcionalidades:**

- Lanzar aplicaciones
- Control de ventanas
- Capturas de pantalla
- Automatización de tareas

---

### Everything Search

**Repositorio:** `modelcontextprotocol/servers`

**Estrellas:** ~1,200+ ⭐

**Descripción:**

Búsqueda rápida de archivos usando Everything (Windows).

---

**Ventaja:**

Búsqueda instantánea de archivos por nombre en Windows.

---

# Database Servers Populares

## Más allá de PostgreSQL y SQLite

---

### MongoDB Server

**Repositorio:** Varios implementaciones

**Estrellas:** ~800-1200+ ⭐ (varía por implementación)

**Descripción:**

Conexión a bases de datos MongoDB para operaciones CRUD y consultas.

---

**Funcionalidades:**

- Consultas con filtros
- Agregaciones
- Inserción y actualización
- Creación de índices
- Análisis de esquemas

---

### Redis Server

**Repositorio:** Varios implementaciones

**Estrellas:** ~600-900+ ⭐ (varía por implementación)

**Descripción:**

Operaciones en Redis: caché, colas, pub/sub.

---

**Funcionalidades:**

- GET/SET de claves
- Listas y conjuntos
- Pub/sub
- Transacciones
- Streams

---

# PARTE 4: DEVELOPER TOOLS

---

# Git Server

## Operaciones de Git

---

**Repositorio:** `modelcontextprotocol/servers` y variantes

**Estrellas:** ~1,500+ ⭐ (combinado)

---

**Descripción:**

Operaciones de Git: commits, branches, merges.

---

**Funcionalidades:**

- Ver estado del repositorio
- Crear y cambiar branches
- Hacer commits
- Ver historial
- Crear tags

---

**Instalación:**

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "/path/to/repo"]
    }
  }
}
```

---

**Ejemplo de uso:**

```
Usuario: "¿Qué cambios hay en el branch actual?"

Claude: [Usa git_status]
        "Hay 3 archivos modificados y 2 nuevos archivos sin staged..."
```

---

# Sequential Thinking Server

## Razonamiento paso a paso

---

**Repositorio:** `modelcontextprotocol/servers`

**Estrellas:** ~1,800+ ⭐

---

**Descripción:**

Ayuda al modelo a pensar paso a paso en problemas complejos.

---

**Funcionalidades:**

- Descomponer problemas
- Seguir pasos lógicos
- Mantener contexto de razonamiento
- Detectar inconsistencias

---

**Instalación:**

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

---

**Ejemplo de uso:**

```
Usuario: "Diseña una arquitectura para una app de reservas"

Claude: [Usa sequential_thinking]
        "Voy a pensar paso a paso:
         1. Primero, identificamos los actores principales...
         2. Luego, definimos las entidades...
         3. A continuación, diseñamos las APIs..."
```

---

# Fetch Server

## Peticiones HTTP

---

**Repositorio:** `modelcontextprotocol/servers`

**Estrellas:** ~1,300+ ⭐

---

**Descripción:**

Realizar peticiones HTTP a APIs externas.

---

**Funcionalidades:**

- GET, POST, PUT, DELETE
- Headers personalizados
- Autenticación
- Manejo de JSON

---

**Instalación:**

```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

---

**Ejemplo de uso:**

```
Usuario: "Obtén los datos de la API jsonplaceholder"

Claude: [Usa fetch]
        "He obtenido los datos de la API. El endpoint devuelve..."
```

---

# PARTE 5: WEB & BROWSER

---

# Puppeteer Server (Revisited)

## Más detalles sobre automatización web

---

**Ya cubierto en oficiales, pero profundicemos en casos avanzados.**

---

**Casos de uso avanzados:**

- Testing E2E automatizado
- Generación de PDFs de facturas
- Monitoreo de precios en e-commerce
- Login automático en dashboards
- Scraping de datos estructurados

---

**Ejemplo avanzado:**

```javascript
// Navegar, esperar contenido, extraer datos
Claude: [Usa puppeteer_navigate a página dinámica]
        [Usa puppeteer_wait para esperar carga]
        [Usa puppeteer_evaluate para extraer datos]
        "He extraído la tabla de precios. Los datos muestran..."
```

---

# Playwright Server

## Alternativa a Puppeteer

---

**Repositorio:** Varias implementaciones

**Estrellas:** ~900+ ⭐

---

**Descripción:**

Automatización de navegador con Playwright (más navegadores soportados).

---

**Ventajas sobre Puppeteer:**

- Soporte para Firefox y Safari
- Mejor manejo de esperas
- Captura de trazas de red
- Paralelización mejorada

---

**Instalación:**

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "playwright-mcp-server"]
    }
  }
}
```

---

# SERP Server

## Búsqueda en motores de búsqueda

---

**Repositorio:** Varias implementaciones

**Estrellas:** ~700+ ⭐

---

**Descripción:**

Búsquedas en Google, Bing, DuckDuckGo sin API.

---

**Funcionalidades:**

- Búsqueda web sin API key
- Extracción de snippets
- Soporte para múltiples motores
- Filtrado por fecha y región

---

**Ventaja:**

No requiere API key, funciona directamente con scraping.

---

# PARTE 6: AI & KNOWLEDGE

---

# Memory Server (Revisited)

## Memoria avanzada

---

**Ya cubierto en oficiales. Profundicemos en implementación.**

---

**Arquitectura de memoria:**

```
┌─────────────────────────────────────┐
│          MEMORY SERVER               │
├─────────────────────────────────────┤
│  ┌───────────┐    ┌───────────┐     │
│  │  Entities │    │Relations  │     │
│  │ (Nodos)   │────│ (Edges)   │     │
│  └───────────┘    └───────────┘     │
│                                      │
│  ┌───────────────────────────────┐  │
│  │     Vector Embeddings         │  │
│  │   (Semantic Search)           │  │
│  └───────────────────────────────┘  │
│                                      │
│  ┌───────────────────────────────┐  │
│  │     Knowledge Graph           │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

**Tipos de memoria:**

| Tipo | Uso | Ejemplo |
|------|-----|---------|
| Episódica | Eventos temporales | "Ayer fuimos al cine" |
| Semántica | Hechos y conceptos | "Paris es capital de Francia" |
| Procedural | Procedimientos | "Cómo hacer café" |
| Social | Relaciones | "Juan es amigo de María" |

---

# Knowledge Graph Server

## Grafos de conocimiento

---

**Repositorio:** Varias implementaciones

**Estrellas:** ~600+ ⭐

---

**Descripción:**

Gestión de grafos de conocimiento con entidades y relaciones.

---

**Funcionalidades:**

- Crear entidades
- Crear relaciones
- Consultar relaciones
- Buscar caminos
- Visualizar grafos

---

**Ejemplo:**

```
Usuario: "Añade que María trabaja en Google y Google tiene oficina en Madrid"

Claude: [Crea entidades María, Google, Madrid]
        [Crea relaciones trabaja_en, tiene_oficina_en]
        "He creado el grafo de conocimiento..."
```

---

# Vector Search Server

## Búsqueda semántica

---

**Repositorio:** Varias implementaciones

**Estrellas:** ~800+ ⭐

---

**Descripción:**

Búsqueda semántica usando embeddings vectoriales.

---

**Funcionalidades:**

- Indexar documentos
- Búsqueda por similitud
- Filtrado por metadatos
- Actualización de índices

---

**Backends soportados:**

- Pinecone
- Weaviate
- Qdrant
- Chroma
- Milvus

---

# PARTE 7: CLOUD SERVICES

---

# AWS Server

## Integración con Amazon Web Services

---

**Repositorio:** Varias implementaciones

**Estrellas:** ~1,200+ ⭐

---

**Descripción:**

Operaciones con servicios de AWS.

---

**Funcionalidades:**

- S3: subir, descargar, listar
- EC2: listar instancias, estados
- Lambda: invocar funciones
- DynamoDB: operaciones CRUD
- CloudWatch: métricas y logs

---

**Instalación:**

```json
{
  "mcpServers": {
    "aws": {
      "command": "npx",
      "args": ["-y", "aws-mcp-server"],
      "env": {
        "AWS_ACCESS_KEY_ID": "...",
        "AWS_SECRET_ACCESS_KEY": "...",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

---

# Google Cloud Server

## Integración con GCP

---

**Repositorio:** Varias implementaciones

**Estrellas:** ~900+ ⭐

---

**Descripción:**

Operaciones con Google Cloud Platform.

---

**Funcionalidades:**

- Cloud Storage
- BigQuery
- Cloud Functions
- Cloud Run
- Vertex AI

---

# Azure Server

## Integración con Microsoft Azure

---

**Repositorio:** Varias implementaciones

**Estrellas:** ~700+ ⭐

---

**Descripción:**

Operaciones con Microsoft Azure.

---

**Funcionalidades:**

- Blob Storage
- Azure Functions
- Cosmos DB
- Cognitive Services
- Virtual Machines

---

# PARTE 8: COMMUNICATION

---

# Slack Server (Revisited)

## Más allá de mensajes básicos

---

**Funcionalidades avanzadas:**

- Thread management
- Reactions
- File uploads
- User management
- Channel creation

---

**Patrón de uso común:**

```
# Notificación de CI/CD
Pipeline CI/CD ──► MCP Server ──► Slack Channel

"Build #1234 completado exitosamente"
"Tests: 847 passed, 0 failed"
"Deploy a producción completado"
```

---

# Discord Server

## Integración con Discord

---

**Repositorio:** Varias implementaciones

**Estrellas:** ~500+ ⭐

---

**Descripción:**

Interactuar con servidores de Discord.

---

**Funcionalidades:**

- Enviar mensajes a canales
- Leer mensajes
- Gestionar roles
- Moderar contenido

---

**Instalación:**

```json
{
  "mcpServers": {
    "discord": {
      "command": "npx",
      "args": ["-y", "discord-mcp-server"],
      "env": {
        "DISCORD_BOT_TOKEN": "..."
      }
    }
  }
}
```

---

# Email Server

## Envío y lectura de emails

---

**Repositorio:** Varias implementaciones

**Estrellas:** ~400+ ⭐

---

**Descripción:**

Enviar y recibir emails mediante IMAP/SMTP.

---

**Funcionalidades:**

- Enviar emails
- Leer bandeja de entrada
- Buscar emails
- Gestionar carpetas
- Adjuntar archivos

---

# PARTE 9: CASOS DE USO PRÁCTICOS

---

# Caso 1: Análisis de Código

## Flujo completo con múltiples servidores

---

**Escenario:**

Un desarrollador quiere analizar un repositorio de código.

---

**Servicios MCP utilizados:**

1. **GitHub Server** - Clonar/acceder al repo
2. **Filesystem Server** - Leer archivos
3. **PostgreSQL Server** - Consultar base de datos
4. **Memory Server** - Recordar contexto

---

**Flujo:**

```
1. GitHub: Obtener lista de archivos del repo
2. Filesystem: Leer código fuente
3. Memory: Recordar decisiones anteriores
4. Análisis del modelo
5. Respuesta estructurada al usuario
```

---

# Caso 2: Automatización de DevOps

## Pipeline de CI/CD

---

**Escenario:**

Automatizar despliegues con notificaciones.

---

**Servicios MCP utilizados:**

1. **Git Server** - Commits y branches
2. **GitHub Server** - Pull requests
3. **Slack Server** - Notificaciones
4. **AWS Server** - Despliegue

---

**Flujo:**

```
1. Git: Verificar branch y estado
2. GitHub: Crear PR si necesario
3. AWS: Desplegar a staging
4. Slack: Notificar equipo
5. Memory: Registrar despliegue
```

---

# Caso 3: Asistente de Investigación

## Búsqueda y síntesis

---

**Escenario:**

Investigar un tema y generar un informe.

---

**Servicios MCP utilizados:**

1. **Brave Search** - Búsqueda web
2. **Fetch Server** - Obtener páginas
3. **Memory Server** - Guardar hallazgos
4. **Filesystem Server** - Guardar informe

---

**Flujo:**

```
1. Brave Search: Buscar tema
2. Fetch: Obtener contenido de URLs
3. Análisis y síntesis del modelo
4. Memory: Guardar conclusiones
5. Filesystem: Exportar informe
```

---

# Caso 4: Asistente de Documentación

## Gestión documental

---

**Escenario:**

Gestionar documentación de proyectos.

---

**Servicios MCP utilizados:**

1. **Google Drive Server** - Acceder a docs
2. **Filesystem Server** - Archivos locales
3. **Slack Server** - Comunicar actualizaciones
4. **Memory Server** - Contexto del proyecto

---

# Caso 5: Testing Automatizado

## E2E Testing con Puppeteer

---

**Escenario:**

Automatizar tests de interfaz.

---

**Servicios MCP utilizados:**

1. **Puppeteer Server** - Navegación y capturas
2. **Filesystem Server** - Guardar screenshots
3. **Slack Server** - Notificar fallos
4. **Memory Server** - Recordar tests previos

---

**Flujo:**

```
1. Puppeteer: Navegar a página
2. Puppeteer: Interactuar con elementos
3. Puppeteer: Capturar resultado
4. Comparar con esperado
5. Filesystem: Guardar evidencia
6. Slack: Notificar si falla
```

---

# PARTE 10: RESUMEN Y RECURSOS

---

# Resumen de Servidores

## Los más populares por categoría

---

### Oficiales (más de 1,500 estrellas)

| Servidor | Estrellas | Uso principal |
|----------|-----------|---------------|
| filesystem | ~3,500 | Archivos locales |
| github | ~3,200 | Integración GitHub |
| postgres | ~2,800 | Base de datos |
| sqlite | ~2,500 | BD local |
| brave-search | ~2,200 | Búsqueda web |
| puppeteer | ~2,000 | Automatización |
| memory | ~2,000 | Persistencia |

---

### Comunidad (destacados)

| Servidor | Estrellas | Uso principal |
|----------|-----------|---------------|
| desktop-commander | ~1,800 | Control escritorio |
| sequential-thinking | ~1,800 | Razonamiento |
| aws-mcp | ~1,200 | AWS |
| everything-search | ~1,200 | Búsqueda Windows |
| mongodb-mcp | ~1,000 | MongoDB |

---

# Cómo Elegir un Servidor

## Factores a considerar

---

### 1. Mantenimiento

- ¿Última actualización reciente?
- ¿Issues activos?
- ¿Documentación completa?

---

### 2. Popularidad

- ¿Número de estrellas?
- ¿Número de forks?
- ¿Comunidad activa?

---

### 3. Compatibilidad

- ¿Cliente MCP soportado?
- ¿Versión de Node.js?
- ¿Dependencias?

---

### 4. Seguridad

- ¿Revisión de código?
- ¿Manejo de credenciales?
- ¿Permisos requeridos?

---

# Instalación General

## Patrón común

---

### Paso 1: Instalar dependencias

```bash
npm install -g @modelcontextprotocol/inspector
```

---

### Paso 2: Configurar en claude_desktop_config.json

```json
{
  "mcpServers": {
    "nombre-servidor": {
      "command": "npx",
      "args": ["-y", "@org/mcp-server-nombre"],
      "env": {
        "API_KEY": "tu-api-key"
      }
    }
  }
}
```

---

### Paso 3: Reiniciar Claude Desktop

Cerrar y volver a abrir la aplicación.

---

### Paso 4: Verificar

Preguntar a Claude: "¿Qué herramientas MCP tienes disponibles?"

---

# Depuración de Servidores

## Problemas comunes

---

### El servidor no inicia

**Causas:**

- Node.js no instalado
- Dependencias faltantes
- Variables de entorno incorrectas

**Solución:**

```bash
# Verificar Node.js
node --version

# Instalar dependencias
npm install

# Verificar logs
npx @modelcontextprotocol/inspector
```

---

### Las tools no aparecen

**Causas:**

- Configuración incorrecta
- API keys inválidas
- Permisos insuficientes

**Solución:**

```json
// Verificar config
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@org/server"],
      "env": {
        "API_KEY": "verificar-que-es-correcta"
      }
    }
  }
}
```

---

# Recursos Adicionales

## Dónde encontrar más información

---

### Repositorio Principal

**awesome-mcp-servers**

https://github.com/punkpeye/awesome-mcp-servers

Lista curada de todos los servidores MCP.

---

### Documentación Oficial

**Model Context Protocol**

https://modelcontextprotocol.io/

Documentación del protocolo.

---

### SDK Oficial

**TypeScript SDK**

https://github.com/modelcontextprotocol/typescript-sdk

Para crear tus propios servidores.

---

### Comunidad

- **Discord MCP**: Servidor de la comunidad
- **GitHub Discussions**: Preguntas y respuestas
- **Twitter/X**: @mcp_protocol

---

# Crear Tu Propio Servidor

## Pasos básicos

---

### 1. Instalar SDK

```bash
npm install @modelcontextprotocol/sdk
```

---

### 2. Estructura básica

```javascript
import { Server } from '@modelcontextprotocol/sdk';

const server = new Server({
  name: 'my-mcp-server',
  version: '1.0.0'
}, {
  capabilities: {
    tools: {}
  }
});

server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'my_tool',
        description: 'Descripción de la herramienta',
        inputSchema: { type: 'object', properties: {} }
      }
    ]
  };
});

server.setRequestHandler('tools/call', async (request) => {
  // Implementar lógica
  return { content: [{ type: 'text', text: 'Resultado' }] };
});
```

---

### 3. Publicar

```bash
npm publish --access public
```

---

# Próximos Pasos

## Cómo continuar

---

1. **Instalar Claude Desktop** si no lo tienes

2. **Configurar tu primer servidor** (filesystem es el más fácil)

3. **Probar tools básicas** (leer archivos, hacer búsquedas)

4. **Añadir más servidores** gradualmente

5. **Crear tu propio servidor** para necesidades específicas

---

# Cierre

---

## Servidores MCP: Ecosistema y Proyectos Destacados

### La comunidad está creciendo rápidamente

---

**Resumen:**

- Servidores oficiales: bien mantenidos, documentados
- Servidores de comunidad: innovación y casos específicos
- Ecosistema en expansión constante
- Fácil crear nuevos servidores

---

**Recursos:**

- awesome-mcp-servers: Lista curada
- modelcontextprotocol.io: Documentación
- Discord: Comunidad activa

---

**¡Explora, experimenta y contribuye!**