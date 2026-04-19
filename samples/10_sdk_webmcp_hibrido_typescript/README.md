# 10 - SDK WebMCP Hibrido (TypeScript + Python)

Demo hibrida: frontend WebMCP (TypeScript) para tools client-side + backend MCP low-level (Python) para operaciones server-side.

## Requisitos

- Python 3.10+
- Node.js 18+ (solo para recompilar TypeScript)
- Navegador compatible con WebMCP experimental

## Preparacion

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Opcional: recompilar TypeScript

```bash
npm install && npm run build
```

## Ejecucion

### Backend MCP (cliente Python para probar tools server-side)

```bash
python client.py
```

### Frontend WebMCP (navegador)

```bash
python serve.py
```

Abre `http://127.0.0.1:8000` y haz click en "Register WebMCP tools".

## Arquitectura

- **Frontend (WebMCP):** tools de carrito client-side (`cart_add_item`, `cart_list_items`, `cart_clear`).
- **Backend (MCP SDK low-level):** tools server-side (`sync_cart`, `checkout`, `check_stock`) + resources (`catalog://all`, `audit://log`).
- Ambas capas se complementan: el frontend maneja la interaccion con el usuario; el backend maneja logica de negocio y persistencia.

## Nota sobre WebMCP

WebMCP es experimental. Necesitas Chrome 146+ con flag `chrome://flags/#enable-webmcp-for-testing` activada.