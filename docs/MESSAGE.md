# 📨 API de Mensajes - Documentación

Esta API gestiona mensajes individuales dentro de conversaciones, con soporte para streaming en tiempo real, contexto conversacional e integración con múltiples LLMs.

## 📋 Endpoints Disponibles

### 🚀 Crear Mensaje con Streaming (Recomendado)
**POST** `/api/message/chat`

Crea un mensaje del usuario y genera una respuesta de IA en tiempo real usando Server-Sent Events.

#### Request Body
```json
{
  "content": "¿Qué servicios ofrece IngeLean?",
  "chat_id": "67a1b2c3d4e5f6789012345"
}
```

#### Response (Server-Sent Events)
```
data: {"type": "content", "content": "IngeLean"}

data: {"type": "content", "content": " ofrece"}

data: {"type": "content", "content": " servicios"}

data: {"type": "content", "content": " de consultoría..."}

data: {"type": "done", "message": "Respuesta completada"}
```

#### Ejemplo JavaScript
```javascript
const response = await fetch('/api/message/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    content: "¿Qué servicios ofrecen?",
    chat_id: "67a1b2c3d4e5f6789012345"
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.slice(6));
      if (data.type === 'content') {
        console.log(data.content); // Texto en tiempo real
      }
    }
  }
}
```

---

### 💬 Crear Mensaje Tradicional
**POST** `/api/message/chat/{chat_id}`

Crea un mensaje tradicional sin streaming (para usuarios específicos o bots).

#### Parámetros
- `chat_id` (string): ID único del chat

#### Request Body
```json
{
  "role": "user",          // "user" o "assistant"
  "content": "¿Cómo están?"
}
```

#### Response
```json
{
  "status": "success",
  "data": {
    "id": "67a1b2c3d4e5f6789012346",
    "chat_id": "67a1b2c3d4e5f6789012345",
    "role": "user",
    "content": "¿Cómo están?",
    "created_at": "2025-01-26T10:30:00Z"
  },
  "message": "Mensaje creado exitosamente"
}
```

#### Ejemplo cURL
```bash
curl -X POST "http://localhost:8000/api/message/chat/67a1b2c3d4e5f6789012345" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "user",
    "content": "¿Qué servicios de consultoría ofrecen?"
  }'
```

---

### 🔍 Obtener Mensaje Específico
**GET** `/api/message/{message_id}`

Obtiene los detalles de un mensaje específico por su ID.

#### Parámetros
- `message_id` (string): ID único del mensaje

#### Response
```json
{
  "status": "success",
  "data": {
    "id": "67a1b2c3d4e5f6789012346",
    "chat_id": "67a1b2c3d4e5f6789012345",
    "role": "assistant",
    "content": "IngeLean ofrece servicios de consultoría en ingeniería...",
    "created_at": "2025-01-26T10:30:00Z"
  },
  "message": "Mensaje obtenido exitosamente"
}
```

#### Ejemplo cURL
```bash
curl -X GET "http://localhost:8000/api/message/67a1b2c3d4e5f6789012346"
```

---

### 📝 Listar Mensajes de un Chat
**GET** `/api/message/chat/{chat_id}`

Obtiene todos los mensajes de un chat específico ordenados cronológicamente.

#### Parámetros
- `chat_id` (string): ID único del chat

#### Response
```json
{
  "status": "success",
  "data": [
    {
      "id": "67a1b2c3d4e5f6789012346",
      "chat_id": "67a1b2c3d4e5f6789012345",
      "role": "user",
      "content": "¿Qué servicios ofrecen?",
      "created_at": "2025-01-26T10:30:00Z"
    },
    {
      "id": "67a1b2c3d4e5f6789012347",
      "chat_id": "67a1b2c3d4e5f6789012345",
      "role": "assistant",
      "content": "IngeLean ofrece servicios de consultoría...",
      "created_at": "2025-01-26T10:30:15Z"
    }
  ],
  "total": 2,
  "chat_id": "67a1b2c3d4e5f6789012345",
  "message": "Mensajes obtenidos exitosamente"
}
```

#### Ejemplo cURL
```bash
curl -X GET "http://localhost:8000/api/message/chat/67a1b2c3d4e5f6789012345"
```

---

### ✏️ Actualizar Mensaje
**PUT** `/api/message/{message_id}`

Actualiza el contenido de un mensaje existente.

#### Parámetros
- `message_id` (string): ID único del mensaje

#### Request Body
```json
{
  "content": "Nuevo contenido del mensaje"
}
```

#### Response
```json
{
  "status": "success",
  "data": {
    "id": "67a1b2c3d4e5f6789012346",
    "chat_id": "67a1b2c3d4e5f6789012345",
    "role": "user",
    "content": "Nuevo contenido del mensaje",
    "created_at": "2025-01-26T10:30:00Z"
  },
  "message": "Mensaje actualizado exitosamente"
}
```

#### Ejemplo cURL
```bash
curl -X PUT "http://localhost:8000/api/message/67a1b2c3d4e5f6789012346" \
  -H "Content-Type: application/json" \
  -d '{"content": "¿Qué servicios de consultoría en ingeniería ofrecen?"}'
```

---

### 🗑️ Eliminar Mensaje
**DELETE** `/api/message/{message_id}`

Elimina un mensaje específico de forma permanente.

#### Parámetros
- `message_id` (string): ID único del mensaje

#### Response
```json
{
  "status": "success",
  "data": null,
  "message": "Mensaje eliminado exitosamente"
}
```

#### Ejemplo cURL
```bash
curl -X DELETE "http://localhost:8000/api/message/67a1b2c3d4e5f6789012346"
```

---

## 🤖 Integración con LLMs

### Contexto Conversacional Automático
El sistema automáticamente:
- 📚 **Recupera** el historial completo del chat
- 🧠 **Analiza** el contexto de la conversación
- 📄 **Incluye** información de documentos PDF (IngeLean)
- 🎯 **Genera** respuestas coherentes y contextuales

### LLMs Soportados
- **Google Gemini 2.5 Flash** (Principal)
- **Mistral AI** (Alternativo)

### Proceso de Respuesta
1. **Usuario envía mensaje** → Se guarda en BD
2. **Sistema recupera contexto** → Historial + documentos
3. **LLM genera respuesta** → Con contexto completo
4. **Respuesta se transmite** → Streaming en tiempo real
5. **Respuesta se guarda** → Persistencia en BD

---

## 📡 Server-Sent Events (SSE)

### Tipos de Eventos
| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `content` | Fragmento de texto | `{"type": "content", "content": "Hola"}` |
| `done` | Respuesta completada | `{"type": "done", "message": "Completado"}` |
| `error` | Error en el proceso | `{"type": "error", "error": "Error message"}` |

### Manejo de Errores en Streaming
```javascript
try {
  const parsedData = JSON.parse(data);
  
  if (parsedData.type === 'content') {
    // Mostrar contenido
    displayContent(parsedData.content);
  } else if (parsedData.type === 'error') {
    // Manejar error
    console.error('Error:', parsedData.error);
  }
} catch (error) {
  console.error('Error parsing SSE:', error);
}
```

---

## 🔧 Códigos de Estado

| Código | Descripción |
|--------|-------------|
| 200 | Operación exitosa |
| 201 | Mensaje creado exitosamente |
| 400 | Datos de entrada inválidos |
| 404 | Mensaje o chat no encontrado |
| 500 | Error interno del servidor |

---

## 🚨 Manejo de Errores

### Error de Chat No Encontrado
```json
{
  "status": "error",
  "error": "Chat no encontrado",
  "message": "El chat especificado no existe"
}
```

### Error de Mensaje No Encontrado
```json
{
  "status": "error",
  "error": "Mensaje no encontrado",
  "message": "El mensaje especificado no existe"
}
```

### Error de Validación
```json
{
  "status": "error",
  "error": "Datos inválidos",
  "message": "El contenido del mensaje es requerido"
}
```

---

## 💡 Casos de Uso Comunes

### 1. Conversación Completa con Streaming
```javascript
// Crear chat
const chatResponse = await fetch('/api/chat/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: "Mi consulta" })
});
const chat = await chatResponse.json();

// Enviar mensaje con streaming
const messageResponse = await fetch('/api/message/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    content: "¿Qué servicios ofrecen?",
    chat_id: chat.data.id
  })
});

// Procesar streaming
const reader = messageResponse.body.getReader();
// ... código de streaming
```

### 2. Gestión de Historial
```bash
# Obtener historial completo
curl -X GET "http://localhost:8000/api/message/chat/67a1b2c3d4e5f6789012345"

# Editar mensaje específico
curl -X PUT "http://localhost:8000/api/message/67a1b2c3d4e5f6789012346" \
  -H "Content-Type: application/json" \
  -d '{"content": "Mensaje corregido"}'

# Eliminar mensaje
curl -X DELETE "http://localhost:8000/api/message/67a1b2c3d4e5f6789012346"
```

### 3. Bot o Sistema Automatizado
```bash
# Crear mensaje de sistema
curl -X POST "http://localhost:8000/api/message/chat/67a1b2c3d4e5f6789012345" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "assistant",
    "content": "Mensaje automático del sistema"
  }'
```

---

## 🔗 Enlaces Relacionados

- [💬 API de Chats](CHAT.md) - Para gestionar conversaciones
- [📊 API de Métricas](METRICAS.md) - Para analizar calidad de mensajes
- [🏠 README Principal](../README.md) - Guía de instalación y configuración