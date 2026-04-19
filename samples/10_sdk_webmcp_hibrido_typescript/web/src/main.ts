type JsonSchema = { type: string; properties?: Record<string, unknown>; required?: string[] };
type ModelContextTool = {
  name: string;
  description: string;
  inputSchema?: JsonSchema;
  execute: (input: unknown) => Promise<unknown> | unknown;
};

interface ModelContext {
  registerTool: (tool: ModelContextTool) => void;
  unregisterTool: (name: string) => void;
}

declare global {
  interface Navigator {
    modelContext?: ModelContext;
  }
}

const cart: Array<{ name: string; qty: number }> = [];

function log(message: string): void {
  const el = document.getElementById("log");
  if (el) el.textContent += `${message}\n`;
}

function registerTools(): void {
  if (!("modelContext" in navigator) || !navigator.modelContext) {
    log("WebMCP API no disponible en este navegador/contexto.");
    log("Activa chrome://flags/#enable-webmcp-for-testing si usas Chrome 146+.");
    return;
  }

  navigator.modelContext.registerTool({
    name: "cart_add_item",
    description: "Add an item to the in-memory cart (frontend)",
    inputSchema: {
      type: "object",
      properties: { name: { type: "string" }, qty: { type: "number" } },
      required: ["name", "qty"],
    },
    execute: async (input: unknown) => {
      const p = input as { name: string; qty: number };
      cart.push({ name: p.name, qty: p.qty });
      return { ok: true, items: cart };
    },
  });

  navigator.modelContext.registerTool({
    name: "cart_list_items",
    description: "List current items from the in-memory cart (frontend)",
    inputSchema: { type: "object", properties: {} },
    execute: async () => ({ items: cart, total_items: cart.length }),
  });

  navigator.modelContext.registerTool({
    name: "cart_clear",
    description: "Clear the in-memory cart (frontend)",
    inputSchema: { type: "object", properties: {} },
    execute: async () => { cart.splice(0, cart.length); return { ok: true }; },
  });

  log("WebMCP tools registradas: cart_add_item, cart_list_items, cart_clear");
  log("Estas tools corren 100% client-side (frontend).");
  log("El backend MCP (backend.py) ofrece sync_cart, checkout, check_stock.");
}

function main(): void {
  const btn = document.getElementById("register-btn");
  if (btn) btn.addEventListener("click", () => registerTools());
  log("App cargada. Haz click en 'Register WebMCP tools'.");
}

main();
export {};