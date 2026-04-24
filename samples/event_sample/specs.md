# Servidore MCP para organizar eventos
## Introduccion
Este servidor MCP (Model Context Protocol) está diseñado para gestionar y organizar eventos de manera eficiente. Proporciona herramientas para crear, actualizar, eliminar y recuperar eventos, así como recursos para acceder a la información de los eventos de forma estructurada.

## Tecnologías Utilizadas
- **FastMCP**: Framework principal para la implementación del servidor MCP.
- **Python**: Lenguaje de programación utilizado para el desarrollo del servidor.

## Specs del Servidor

### Tools
- **create_event**: Permite crear un nuevo evento en el sistema. Requiere los siguientes parámetros:
  - `event_name`: El nombre del evento.
  - `event_date`: La fecha del evento.
  - `event_time`: La hora del evento.
  - `event_location`: La ubicación del evento.
  - `event_description`: Una descripción del evento (opcional).
  - `invitees_list`: Lista de personas invitadas al evento (opcional).
- **get_event**: Permite recuperar un evento existente por su ID. Parámetro:
  - `event_id`: El identificador único del evento que se desea recuperar. Si no se proporciona un ID, se devuelve un evento aleatorio.
- **update_event**: Permite actualizar un evento existente. Requiere los siguientes parámetros:
  - `event_id`: El identificador único del evento que se desea actualizar.
    - `event_name`: El nuevo nombre del evento (opcional).
    - `event_date`: La nueva fecha del evento (opcional).
    - `event_time`: La nueva hora del evento (opcional).
    - `event_location`: La nueva ubicación del evento (opcional).
    - `event_description`: Una nueva descripción del evento (opcional).
    - `invitees_list`: Nueva lista de personas invitadas al evento (opcional).
    - `atendiees_list`: Nueva lista de personas que asistirán al evento (opcional).
- **delete_event**: Permite eliminar un evento existente por su ID. Parámetro:
  - `event_id`: El identificador único del evento que se desea eliminar.
  - **mark_attendance**: Permite marcar la asistencia de un invitado a un evento. Requiere los siguientes parámetros:
    - `event_id`: El identificador único del evento al que se desea marcar la asistencia.
    - `invitee_id`: El identificador único del invitado cuya asistencia se desea marcar.
  - **unmark_attendance**: Permite desmarcar la asistencia de un invitado a un evento. Requiere los siguientes parámetros:
    - `event_id`: El identificador único del evento al que se desea desmarcar la asistencia.
    - `invitee_id`: El identificador único del invitado cuya asistencia se desea desmarcar.

### Resources
- **Event Resource**: 'event:/{id}' representa un evento específico en el sistema. Devuelve la info en json o markdown. Contiene los siguientes atributos:
  - `id`: Identificador único del evento.
  - `event_name`: El nombre del evento.
  - `event_date`: La fecha del evento.
  - `event_time`: La hora del evento.
  - `event_location`: La ubicación del evento.
  - `event_description`: Una descripción del evento (opcional).
  - `invitees_list`: Lista de personas invitadas al evento (opcional).
  - `atendiees_list`: Lista de personas que asistirán al evento (opcional).

### Prompts
- **Event Summary Prompt**: Genera un resumen del evento con su información clave. Utiliza el siguiente template:
```Event Summary:
- Name: {event_name}
- Date: {event_date}
- Time: {event_time}
- Location: {event_location}
- Description: {event_description}
- Invitees: {invitees_list}
- Attendees: {atendiees_list}
```