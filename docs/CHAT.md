# 💬 API de Chats - Documentación

Esta API permite gestionar conversaciones completas con persistencia en MongoDB y contexto conversacional inteligente.

## 📋 Endpoints Disponibles

### 🆕 Crear Chat
**POST** `/api/chat/`

Crea una nueva conversación con título opcional.

#### Request Body
```json
{
  "title": "Mi conversación con IngeLean"  // Opcional
}
```

#### Response
```json
{
  "status": "success",
  "data": {
    "id": "67a1b2c3d4e5f6789012345",
    "title": "Mi conversación con IngeLean",
    "created_at": "2025-01-26T10:30:00Z",
    "updated_at": "2025-01-26T10:30:00Z"
  },
  "message": "Chat creado exitosamente"
}
```

#### Ejemplo cURL
```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Consulta sobre servicios IngeLean"}'
```

---

### 📝 Listar Chats
**GET** `/api/chat/`

Obtiene todos los chats del usuario ordenados por fecha de actualización.

#### Response
```json
{
  "status": "success",
  "data": [
    {
      "id": "67a1b2c3d4e5f6789012345",
      "title": "Consulta sobre servicios",
      "created_at": "2025-01-26T10:30:00Z",
      "updated_at": "2025-01-26T10:35:00Z"
    },
    {
      "id": "67a1b2c3d4e5f6789012346",
      "title": "Chat sobre productos",
      "created_at": "2025-01-26T09:15:00Z",
      "updated_at": "2025-01-26T09:20:00Z"
    }
  ],
  "total": 2,
  "message": "Chats obtenidos exitosamente"
}
```

#### Ejemplo cURL
```bash
curl -X GET "http://localhost:8000/api/chat/"
```

---

### 🔍 Obtener Chat Específico
**GET** `/api/chat/{chat_id}`

Obtiene los detalles de un chat específico por su ID.

#### Parámetros
- `chat_id` (string): ID único del chat

#### Response
```json
{
  "status": "success",
  "data": {
    "id": "67a1b2c3d4e5f6789012345",
    "title": "Consulta sobre servicios",
    "created_at": "2025-01-26T10:30:00Z",
    "updated_at": "2025-01-26T10:35:00Z"
  },
  "message": "Chat obtenido exitosamente"
}
```

#### Ejemplo cURL
```bash
curl -X GET "http://localhost:8000/api/chat/67a1b2c3d4e5f6789012345"
```

---

### ✏️ Actualizar Chat
**PUT** `/api/chat/{chat_id}`

Actualiza el título de un chat existente.

#### Parámetros
- `chat_id` (string): ID único del chat

#### Request Body
```json
{
  "title": "Nuevo título del chat"
}
```

#### Response
```json
{
  "status": "success",
  "data": {
    "id": "67a1b2c3d4e5f6789012345",
    "title": "Nuevo título del chat",
    "created_at": "2025-01-26T10:30:00Z",
    "updated_at": "2025-01-26T10:40:00Z"
  },
  "message": "Chat actualizado exitosamente"
}
```

#### Ejemplo cURL
```bash
curl -X PUT "http://localhost:8000/api/chat/67a1b2c3d4e5f6789012345" \
  -H "Content-Type: application/json" \
  -d '{"title": "Consulta sobre productos IngeLean"}'
```

---

### 🗑️ Eliminar Chat
**DELETE** `/api/chat/{chat_id}`

Elimina un chat y todos sus mensajes asociados de forma permanente.

#### Parámetros
- `chat_id` (string): ID único del chat

#### Response
```json
{
  "status": "success",
  "data": null,
  "message": "Chat y sus mensajes eliminados exitosamente"
}
```

#### Ejemplo cURL
```bash
curl -X DELETE "http://localhost:8000/api/chat/67a1b2c3d4e5f6789012345"
```

---

## 🔧 Códigos de Estado

| Código | Descripción |
|--------|-------------|
| 200 | Operación exitosa |
| 201 | Chat creado exitosamente |
| 400 | Datos de entrada inválidos |
| 404 | Chat no encontrado |
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

### Error de Validación
```json
{
  "status": "error",
  "error": "Datos inválidos",
  "message": "El título debe ser una cadena de texto"
}
```

---

## 💡 Casos de Uso Comunes

### 1. Flujo Completo de Chat
```bash
# 1. Crear chat
CHAT_ID=$(curl -s -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Mi consulta"}' | jq -r '.data.id')

# 2. Enviar mensajes (ver MESSAGE.md)
curl -X POST "http://localhost:8000/api/message/chat/$CHAT_ID" \
  -H "Content-Type: application/json" \
  -d '{"role": "user", "content": "¿Qué servicios ofrecen?"}'

# 3. Obtener historial
curl -X GET "http://localhost:8000/api/message/chat/$CHAT_ID"

# 4. Actualizar título
curl -X PUT "http://localhost:8000/api/chat/$CHAT_ID" \
  -H "Content-Type: application/json" \
  -d '{"title": "Consulta sobre servicios IngeLean"}'
```

### 2. Gestión de Múltiples Chats
```bash
# Listar todos los chats
curl -X GET "http://localhost:8000/api/chat/"

# Obtener detalles específicos
curl -X GET "http://localhost:8000/api/chat/{chat_id}"

# Eliminar chat antiguo
curl -X DELETE "http://localhost:8000/api/chat/{chat_id}"
```

---

## 🔗 Enlaces Relacionados

- [📨 API de Mensajes](MESSAGE.md) - Para gestionar mensajes dentro de los chats
- [📊 API de Métricas](METRICAS.md) - Para analizar la calidad de las conversaciones
- [🏠 README Principal](../README.md) - Guía de instalación y configuración