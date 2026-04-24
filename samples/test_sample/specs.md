# Servidor MCP para tests de preguntas

## Introduccion
Este servidor es una implementación de un servidor MCP (Model Context Protocol) diseñado para facilitar la realización de pruebas de preguntas. El objetivo principal es proporcionar un entorno controlado donde se puedan ejecutar y evaluar preguntas de manera eficiente y precisa.

## Tecnologías Utilizadas
- **FastMCP**: Framework principal para la implementación del servidor MCP.
- **Python**: Lenguaje de programación utilizado para el desarrollo del servidor.

## Specs del Servidor

### Tools
- **create_question**: Permite crear una nueva pregunta en el sistema. Requiere los siguientes parámetros:
  - `question_text`: El texto de la pregunta.
  - `answer_options`: Una lista de opciones de respuesta.
  - `correct_answer`: La opción correcta entre las proporcionadas.
- **get_question**: Permite recuperar una pregunta existente por su ID. Parámetro:
  - `question_id`: El identificador único de la pregunta que se desea recuperar. Si no se proporciona un ID, se devuelve una pregunta aleatoria.
- **update_question**: Permite actualizar una pregunta existente. Requiere los siguientes parámetros:
  - `question_id`: El identificador único de la pregunta que se desea actualizar.
    - `question_text`: El nuevo texto de la pregunta (opcional).
    - `answer_options`: La nueva lista de opciones de respuesta (opcional).
    - `correct_answer`: La nueva opción correcta entre las proporcionadas (opcional).
- **delete_question**: Permite eliminar una pregunta existente por su ID. Parámetro:
  - `question_id`: El identificador único de la pregunta que se desea eliminar.

### Resources
- **Question Resource**: 'question:/{id}' representa una pregunta específica en el sistema. Devuelve la info en json o markdown. Contiene los siguientes atributos:
  - `id`: Identificador único de la pregunta.
  - `question_text`: El texto de la pregunta.
  - `answer_options`: Una lista de opciones de respuesta.
  - `correct_answer`: La opción correcta entre las proporcionadas. 

### Prompts
