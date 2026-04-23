---
theme: seriph
background: https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=2070
class: text-center
highlighter: shiki
lineNumbers: true
drawings:
  persist: false
transition: slide-left
title: Gradio - Interfaces para ML
---

<div class="absolute top-0 left-0 w-full h-full bg-black/50 z--1"></div>

# Introducción a Gradio

Crea interfaces web para tus modelos de Machine Learning en minutos

[gradio.app](https://gradio.app/)

---
layout: default
---

# ¿Qué es Gradio?

Gradio es la forma más rápida de presentar tu modelo de Machine Learning con una interfaz web amigable para que cualquiera pueda usarlo en cualquier lugar.

- **Rápido:** Define interfaces en pocas líneas de código.
- **Flexible:** Soporta texto, imágenes, audio, video y más.
- **Fácil de compartir:** Genera enlaces públicos automáticamente.
- **Integración:** Funciona perfectamente con Python y las librerías de ML más populares.

---

# Instalación

Para instalar Gradio, simplemente usa `pip` en tu terminal:

```bash
pip install gradio
```

O si usas un entorno específico dentro de un notebook:

```python
%pip install gradio
```

---

# Hola Mundo con Gradio

El concepto principal es la clase `Interface`, que requiere una función, entradas y salidas.

```python {all|3-4|6-10|12|all}
import gradio as gr

def saludo(nombre):
    return f"¡Hola {nombre}! Bienvenido a Gradio."

demo = gr.Interface(
    fn=saludo,
    inputs="text",
    outputs="text"
)

demo.launch()
```

---

# Elementos de Interfaz (Inputs/Outputs)

Gradio ofrece múltiples componentes predefinidos para interactuar con tus funciones.

```python {all|4-8|all}
import gradio as gr

def procesar_datos(texto, numero, imagen):
    # Lógica de procesamiento aquí
    return f"Procesado: {texto}", numero * 2, imagen

demo = gr.Interface(
    fn=procesar_datos,
    inputs=[
        gr.Textbox(label="Mensaje"),
        gr.Slider(0, 100, label="Puntuación"),
        gr.Image(label="Sube una foto")
    ],
    outputs=["text", "number", "image"]
)

demo.launch()
```

---

# Bloques (Blocks) para Layouts Complejos

Si necesitas más control que el que ofrece `Interface`, usa `gr.Blocks`.

```python
import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("# Sistema de Análisis")
    
    with gr.Row():
        inp = gr.Textbox(placeholder="Escribe algo aquí...")
        out = gr.Textbox()
        
    btn = gr.Button("Ejecutar")
    btn.click(fn=lambda x: x.upper(), inputs=inp, outputs=out)

demo.launch()
```

---

# Compartiendo tu interfaz

Para crear un enlace público temporal (válido por 72 horas), simplemente añade `share=True` al método `launch()`.

```python
demo.launch(share=True)
```

Esto te proporcionará una URL tipo `https://12345.gradio.app` que puedes enviar a cualquier persona para que pruebe tu demo directamente desde tu máquina.

---

# Integración con Hugging Face Spaces

Gradio se integra de forma nativa con **Hugging Face Spaces**, permitiéndote alojar tus demos de forma gratuita y permanente.

- **Fácil despliegue:** Sube un archivo `app.py` y un `requirements.txt`.
- **Visibilidad:** Haz que tu modelo sea accesible para toda la comunidad.
- **Hardware:** Opciones para usar GPUs gratuitas o de pago.

```python
# Puedes cargar modelos directamente desde el Hub
import gradio as gr

gr.Interface.load("huggingface/gpt2").launch()
```

---

# Ejemplos de Elementos Avanzados

Gradio incluye componentes para manejar casi cualquier tipo de dato:

| Componente | Uso |
| --- | --- |
| `gr.Audio` | Grabar o subir archivos de audio |
| `gr.Video` | Reproducir o capturar vídeo |
| `gr.File` | Subir/Bajar archivos arbitrarios |
| `gr.Dataframe` | Visualizar y editar tablas tipo Excel |
| `gr.Chatbot` | Interfaz optimizada para LLMs |

---

# Ejemplo: Interfaz de Chat con Ollama

Integrar Ollama es sencillo usando su librería oficial. Esto permite conectar tu interfaz con modelos locales como Llama 3 o Mistral.

```python {all|3-4|6-10|all}
import gradio as gr
import ollama

def responder(mensaje, historia):
    response = ollama.chat(
        model="llama3.2",
        messages=[{'role': 'user', 'content': mensaje}],
    )
    return response['message']['content']

demo = gr.ChatInterface(fn=responder, title="Chat Local con Ollama")
demo.launch()
```

---

# Chat con Ollama y Streaming

Para una experiencia fluida, podemos usar el modo `stream=True` de Ollama junto con `yield` en Gradio.

```python {all|4-10|all}
import gradio as gr
import ollama

def responder_streaming(mensaje, historia):
    response = ollama.chat(
        model="llama3",
        messages=[{'role': 'user', 'content': mensaje}],
        stream=True
    )
    
    mensaje_completo = ""
    for chunk in response:
        mensaje_completo += chunk['message']['content']
        yield mensaje_completo

gr.ChatInterface(fn=responder_streaming).launch()
```

---

# Personalización del Chat (UI Atractiva)

Puedes añadir ejemplos predefinidos, cambiar el tema y añadir un icono para hacerlo más visual.

```python {all|4-10|12-14|all}
import gradio as gr

demo = gr.ChatInterface(
    fn=responder,
    title="🤖 IA Avanzada",
    description="Pregunta lo que quieras a tu asistente personal.",
    examples=["¿Cómo funciona Gradio?", "¿Cómo conecto Ollama?"],
    theme="soft", # Temas: 'soft', 'glass', 'monochrome', etc.
    cache_examples=True,
    retry_btn=None, # Personaliza o quita botones
    undo_btn="Deshacer",
    clear_btn="Limpiar",
)

demo.launch()
```

---

# Streaming: Respuestas en Tiempo Real

Para una experiencia tipo ChatGPT, usa generadores (`yield`) para mostrar la respuesta palabra a palabra.

```python {all|3-6|all}
import gradio as gr
import time

def responder_streaming(mensaje, historia):
    respuesta = f"Generando una respuesta larga para: {mensaje}..."
    for i in range(len(respuesta)):
        time.sleep(0.05)
        yield respuesta[:i+1]

gr.ChatInterface(fn=responder_streaming).launch()
```

---
layout: center
class: text-center
---

# ¡Gracias!

¿Listo para crear tu primera interfaz?

[Documentación oficial](https://gradio.app/docs/)
