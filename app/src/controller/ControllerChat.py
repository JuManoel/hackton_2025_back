from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from app.src.service.ServiceChat import ServiceChat

# Modelos Pydantic para request/response
class ChatCreateRequest(BaseModel):
    title: Optional[str] = "Nuevo Chat"

class ChatUpdateRequest(BaseModel):
    title: str

class ControllerChat:
    def __init__(self):
        self.router = APIRouter(prefix="/api/chat", tags=["Chat"])
        self.service = ServiceChat()
        self._setup_routes()
    
    def _setup_routes(self):
        """Configura las rutas del controlador"""
        
        @self.router.post("/")
        async def create_chat():
            """Crea un nuevo chat"""
            result = self.service.create_chat()
            
            if result["success"]:
                return {
                    "status": "success",
                    "data": result["data"],
                    "message": result["message"]
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=result["error"]
                )
        
        @self.router.get("/")
        async def get_all_chats():
            """Obtiene todos los chats con información de último mensaje"""
            result = self.service.get_all_chats()
            
            if result["success"]:
                return {
                    "status": "success",
                    "data": result["data"],
                    "total": result["total"]
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=result["error"]
                )
        
        @self.router.get("/{chat_id}")
        async def get_chat(chat_id: str):
            """Obtiene un chat por su ID"""
            result = self.service.get_chat_by_id(chat_id)
            
            if result["success"]:
                return {
                    "status": "success",
                    "data": result["data"]
                }
            else:
                status_code = status.HTTP_404_NOT_FOUND if "no encontrado" in result["error"] else status.HTTP_500_INTERNAL_SERVER_ERROR
                raise HTTPException(
                    status_code=status_code,
                    detail=result["error"]
                )
        
    
    def get_router(self):
        """Retorna el router configurado"""
        return self.router