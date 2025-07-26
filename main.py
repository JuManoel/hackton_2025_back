from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.src.controller.ControllerChat import ControllerChat
from app.src.controller.ControllerMessage import ControllerMessage
from app.src.controller.ControllerMetricas import ControllerMetricas
from app.src.database.connection import db_connection

# Crear la aplicación FastAPI
app = FastAPI(
    title="Hackaton Chat API",
    description="API para gestionar chats y mensajes con MongoDB",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar controladores
chat_controller = ControllerChat()
message_controller = ControllerMessage()
metricas_controller = ControllerMetricas()

# Registrar rutas
app.include_router(chat_controller.get_router())
app.include_router(message_controller.get_router())
app.include_router(metricas_controller.get_router())

@app.get("/")
async def root():
    """Endpoint de prueba"""
    return {
        "message": "Hackaton Chat API",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la aplicación"""
    try:
        # Verificar conexión a MongoDB
        db = db_connection.get_database()
        db.command("ping")
        
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Todos los servicios funcionando correctamente"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)