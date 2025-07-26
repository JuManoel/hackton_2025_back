# 🚀 IngeLean AI Assistant - Hackaton 2025

Un asistente virtual inteligente con avatar, streaming en tiempo real y análisis de métricas desarrollado para el Hackaton 2025 de la Universidad de Caldas.

## ✨ Características Principales

- 💬 **Chat inteligente** con múltiples LLMs
- 📡 **Streaming en tiempo real** (Server-Sent Events)
- 🎤 **Reconocimiento de voz** integrado
- 📊 **Dashboard de métricas** con análisis IA
- 💾 **Base de datos MongoDB** para persistencia
- 🤖 **Múltiples LLMs** (Gemini, Mistral)
- 🌐 **Interfaz web completa** responsive

## 📋 Requisitos

### Sistema
- **Python 3.12+**
- **MongoDB 4.4+**
- **Navegador moderno** (Chrome, Firefox, Edge)

### APIs Requeridas
- **Google Gemini API** - [Obtener clave](https://makersuite.google.com/app/apikey)
- **Mistral AI API** - [Obtener clave](https://console.mistral.ai/)

## ⚡ Inicio Rápido

### 1. Instalación
```bash
# Clonar repositorio
git clone <repository-url>
cd hackton2025

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración
Crear archivo `.env` en la raíz:
```env
# APIs obligatorias
GEMINI_API=tu_clave_de_gemini_aqui
MISTRAL_API=tu_clave_de_mistral_aqui

# Base de datos
MONGO_URL=mongodb://localhost:27017
```

### 3. MongoDB
#### Ubuntu/Debian:
```bash
sudo apt update && sudo apt install mongodb
sudo systemctl start mongodb
```

#### macOS (Homebrew):
```bash
brew tap mongodb/brew && brew install mongodb-community
brew services start mongodb-community
```

#### Docker:
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 4. Ejecutar
```bash
python main.py
```

## 🌐 Acceso a la Aplicación

Una vez ejecutado el servidor:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **🎮 Interfaz Principal** | http://localhost:8000/html/mix.html | Asistente inteligente completo |
| **📖 API Docs** | http://localhost:8000/docs | Documentación Swagger |
| **🔧 Health Check** | http://localhost:8000/health | Estado del servidor |

## 📚 Documentación de APIs

### 📋 Endpoints Principales
| Recurso | Documentación | Descripción |
|---------|---------------|-------------|
| **💬 Chats** | [docs/CHAT.md](docs/CHAT.md) | Crear, listar, actualizar conversaciones |
| **📨 Mensajes** | [docs/MESSAGE.md](docs/MESSAGE.md) | Envío con streaming, historial, edición |
| **📊 Métricas** | [docs/METRICAS.md](docs/METRICAS.md) | Análisis de calidad con IA |

### 🔗 APIs Externas
- **[Google Gemini](https://ai.google.dev/)** - LLM principal con streaming
- **[Mistral AI](https://mistral.ai/)** - LLM alternativo y análisis

## 🎯 Uso Básico

### 1. Interfaz Web (Recomendado)
1. Abrir http://localhost:8000/html/mix.html
2. Escribir pregunta o usar micrófono 🎤
3. Ver respuesta en tiempo real con streaming
4. Generar métricas con el botón 📊

### 2. API REST
```bash
# Crear chat
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Mi consulta"}'

# Enviar mensaje
curl -X POST "http://localhost:8000/api/message/chat" \
  -H "Content-Type: application/json" \
  -d '{"content": "¿Qué servicios ofrecen?", "chat_id": "CHAT_ID"}'
```

## 🛠 Tecnologías

- **Backend**: FastAPI + Python 3.12
- **Frontend**: HTML5 + JavaScript + TailwindCSS
- **Base de datos**: MongoDB + PyMongo
- **IA**: Google Gemini 2.5 Flash + Mistral AI
- **Streaming**: Server-Sent Events (SSE)
- **Voz**: Web Speech API

## 🚨 Solución de Problemas

### MongoDB no conecta
```bash
sudo systemctl status mongodb
sudo systemctl restart mongodb
```

### Error de APIs
- Verificar claves en `.env`
- Confirmar créditos disponibles
- Revisar logs: `python main.py`

### Streaming no funciona
- Usar navegador moderno
- Verificar CORS
- Comprobar conexión a internet

## 📁 Estructura del Proyecto

```
hackton2025/
├── 🌐 html/mix.html              # Interfaz principal
├── 🤖 API/                       # Integraciones LLM
├── 📱 app/src/                   # Backend FastAPI
├── 📚 docs/                      # Documentación APIs
├── 📄 main.py                    # Servidor principal
├── 📋 requirements.txt           # Dependencias
└── 🔧 .env                       # Configuración
```

## 🤝 Contribución

Este proyecto fue desarrollado para el **Hackaton 2025** de la Universidad de Caldas como una solución completa de asistente virtual empresarial.

---

⭐ **¡Disfruta usando IngeLean AI Assistant!** ⭐
