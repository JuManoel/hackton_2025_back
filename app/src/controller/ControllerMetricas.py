from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.src.service.ServiceMetricas import ServiceMetricas


# Modelos Pydantic para request/response
class MessageCreateRequest(BaseModel):
    content: str  # Solo necesitamos el contenido para el test

class MessageUpdateRequest(BaseModel):
    content: str

class ControllerMetricas:
    def __init__(self):
        self.router = APIRouter(prefix="/api/metricas", tags=["Metricas"])
        self.service = ServiceMetricas()
        self._setup_routes()
    

    def _setup_routes(self):
        """Configura las rutas del controlador"""
        

        @self.router.get("/{chat_id}")
        async def create_metricas(chat_id: str):
            return self.service.create_analisis(chat_id)
    def get_router(self):
        """Retorna el router configurado"""
        return self.router