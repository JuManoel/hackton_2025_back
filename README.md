# 🚀 Hackaton Chat API 2025

Una API REST completa para gestión de chats y mensajes con integración de múltiples LLMs (Large Language Models), desarrollada para el Hackaton 2025 de la Universidad de Caldas.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Arquitectura](#-arquitectura)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Ejecución](#-ejecución)
- [Uso de la API](#-uso-de-la-api)
- [Endpoints](#-endpoints)
- [Ejemplos de Uso](#-ejemplos-de-uso)
- [Integración con LLMs](#-integración-con-llms)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Contribución](#-contribución)

## ✨ Características

- 🔄 **API REST completa** con FastAPI
- 💾 **Base de datos MongoDB** para persistencia
- 🤖 **Integración con múltiples LLMs**:
  - Google Gemini 2.5 Flash
  - Mistral AI
- 📱 **Gestión de chats** (crear, listar, actualizar, eliminar)
- 💬 **Gestión de mensajes** (enviar, obtener, editar, eliminar)
- 📄 **Procesamiento de documentos PDF** para contexto de empresa
- 🔍 **Contexto conversacional** para respuestas coherentes
- 📖 **Documentación automática** con Swagger UI
- 🛡️ **Validación de datos** con Pydantic
- 🌐 **CORS habilitado** para desarrollo frontend

## 🛠 Tecnologías

- **Backend**: Python 3.12+ con FastAPI
- **Base de datos**: MongoDB
- **LLMs**: 
  - Google Generative AI (Gemini)
  - Mistral AI
- **Procesamiento PDF**: PyPDF2
- **Validación**: Pydantic
- **Servidor**: Uvicorn
- **Gestión de entorno**: python-dotenv

## 🏗 Arquitectura

El proyecto sigue una arquitectura de capas limpia:

```
📁 Arquitectura del Sistema
├── 🎯 Controllers (FastAPI routes)
├── 🔧 Services (Lógica de negocio)
├── 💾 Repositories (Acceso a datos)
├── 📊 Models (Entidades de dominio)
└── 🤖 API LLM (Integración con IAs)
```

## 📋 Requisitos

### Sistema
- Python 3.12 o superior
- MongoDB 4.4 o superior
- Git

### APIs Externas
- Clave API de Google Gemini
- Clave API de Mistral AI

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd hackton2025
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
# o
.venv\Scripts\activate     # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Instalar y configurar MongoDB

#### En Ubuntu/Debian:
```bash
sudo apt update
sudo apt install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

#### En macOS (con Homebrew):
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

#### Con Docker:
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## ⚙️ Configuración

### 1. Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# APIs de LLM
GEMINI_API=tu_clave_api_de_gemini_aqui
MISTRAL_API=tu_clave_api_de_mistral_aqui

# Base de datos
MONGO_URL=mongodb://localhost:27017
```

### 2. Obtener claves de API

#### Google Gemini:
1. Visita [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una nueva API key
3. Copia la clave en el archivo `.env`

#### Mistral AI:
1. Visita [Mistral AI Console](https://console.mistral.ai/)
2. Crea una cuenta y genera una API key
3. Copia la clave en el archivo `.env`

### 3. Documento PDF de contexto

Coloca tu documento PDF de empresa en:
```
API/pdf/Brochure-Ingelean.pdf
```

## 🎮 Ejecución

### Desarrollo
```bash
python main.py
```

### Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Con recarga automática (desarrollo)
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📚 Uso de la API

### Documentación interactiva
Una vez ejecutado el servidor, accede a http://localhost:8000/docs para ver la documentación interactiva de Swagger UI.

### Formato de respuesta
Todas las respuestas siguen este formato estándar:
```json
{
  "status": "success|error",
  "data": {...},
  "message": "Mensaje descriptivo",
  "total": 10  // Solo en listados
}
```

## 🔗 Endpoints

### 🏠 Sistema
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Estado de la API |
| GET | `/health` | Verificación de salud del sistema |

### 💬 Chats
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/chat/` | Crear nuevo chat |
| GET | `/api/chat/` | Listar todos los chats |
| GET | `/api/chat/{chat_id}` | Obtener chat específico |
| PUT | `/api/chat/{chat_id}` | Actualizar título del chat |
| DELETE | `/api/chat/{chat_id}` | Eliminar chat y sus mensajes |

### 💌 Mensajes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/message/chat/{chat_id}` | Crear mensaje en chat |
| GET | `/api/message/{message_id}` | Obtener mensaje específico |
| GET | `/api/message/chat/{chat_id}` | Listar mensajes del chat |
| PUT | `/api/message/{message_id}` | Actualizar contenido del mensaje |
| DELETE | `/api/message/{message_id}` | Eliminar mensaje |

## 💡 Ejemplos de Uso

### Crear un chat
```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Consulta sobre servicios"}'
```

### Enviar mensaje del usuario
```bash
curl -X POST "http://localhost:8000/api/message/chat/{chat_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "user",
    "content": "¿Qué servicios ofrece la empresa?"
  }'
```

### Obtener todos los mensajes de un chat
```bash
curl -X GET "http://localhost:8000/api/message/chat/{chat_id}"
```

### Listar todos los chats
```bash
curl -X GET "http://localhost:8000/api/chat/"
```

## 🤖 Integración con LLMs

### Gemini AI
```python
from API.Gemini import Gemini

gemini = Gemini()
respuesta = gemini.responder_pregunta("¿Cómo están?")
```

### Mistral AI
```python
from API.Mistral import MistralAPI

mistral = MistralAPI()
respuesta = mistral.responder_pregunta("¿Cómo están?")
```

### Con contexto conversacional
```python
contexto = [
    {"role": "user", "parts": "Hola"},
    {"role": "assistant", "parts": "¡Hola! ¿En qué puedo ayudarte?"}
]

respuesta = gemini.responder_pregunta_con_contexto(
    "¿Qué servicios tienen?", 
    contexto
)
```

## 📁 Estructura del Proyecto

```
hackton2025/
├── 📁 API/                          # Integración con LLMs
│   ├── 📄 Gemini.py                # Cliente Google Gemini
│   ├── 📄 Mistral.py               # Cliente Mistral AI
│   ├── 📁 interface/               # Interfaces y abstracciones
│   │   └── 📄 ILLMApi.py          # Interfaz base para LLMs
│   └── 📁 pdf/                    # Documentos de contexto
│       └── 📄 Brochure-Ingelean.pdf
├── 📁 app/                         # Aplicación principal
│   └── 📁 src/
│       ├── 📁 controller/          # Controladores FastAPI
│       │   ├── 📄 ControllerChat.py
│       │   └── 📄 ControllerMessage.py
│       ├── 📁 database/            # Gestión de base de datos
│       │   └── 📄 connection.py
│       ├── 📁 models/              # Modelos de dominio
│       │   ├── 📄 Chat.py
│       │   └── 📄 Message.py
│       ├── 📁 repository/          # Acceso a datos
│       │   ├── 📄 RepositoryChat.py
│       │   └── 📄 RepositoryMessage.py
│       └── 📁 service/             # Lógica de negocio
│           ├── 📄 ServiceChat.py
│           └── 📄 ServiceMessage.py
├── 📁 docs/                        # Documentación
├── 📄 main.py                      # Punto de entrada de la aplicación
├── 📄 requirements.txt             # Dependencias Python
├── 📄 .env                         # Variables de entorno
└── 📄 README.md                    # Este archivo
```

## 🚨 Solución de Problemas

### Error de conexión a MongoDB
```bash
# Verificar que MongoDB esté ejecutándose
sudo systemctl status mongodb

# Reiniciar MongoDB
sudo systemctl restart mongodb
```

### Error de claves API
- Verificar que las claves en `.env` sean correctas
- Confirmar que las APIs tengan créditos disponibles
- Revisar los logs del servidor para errores específicos

### Problemas con dependencias
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto fue desarrollado para el Hackaton 2025 de la Universidad de Caldas.

## 📞 Soporte

Para soporte y preguntas:
- 📧 Email: [tu-email@example.com]
- 💬 Issues: [GitHub Issues]

---

⭐ **¡Dale una estrella al proyecto si te ha sido útil!** ⭐