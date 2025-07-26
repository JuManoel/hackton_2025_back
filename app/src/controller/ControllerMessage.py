from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Literal
from app.src.service.ServiceMessage import ServiceMessage

# Modelos Pydantic para request/response
class MessageCreateRequest(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class MessageUpdateRequest(BaseModel):
    content: str

class ControllerMessage:
    def __init__(self):
        self.router = APIRouter(prefix="/api/message", tags=["Message"])
        self.service = ServiceMessage()
        self._setup_routes()
    
    def _setup_routes(self):
        """Configura las rutas del controlador"""
        
        @self.router.post("/chat/{chat_id}")
        async def create_message(chat_id: str, request: MessageCreateRequest):
            """Crea un nuevo mensaje en un chat"""
            result = self.service.create_message(chat_id, request.content)
            
            if result["success"]:
                return {
                    "status": "success",
                    "data": result["data"],
                    "message": result["message"]
                }
            else:
                status_code = status.HTTP_404_NOT_FOUND if "no encontrado" in result["error"] else status.HTTP_400_BAD_REQUEST
                raise HTTPException(
                    status_code=status_code,
                    detail=result["error"]
                )
        
        @self.router.get("/{message_id}")
        async def get_message(message_id: str):
            """Obtiene un mensaje por su ID"""
            result = self.service.get_message_by_id(message_id)
            
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
        
        @self.router.get("/chat/{chat_id}")
        async def get_messages_by_chat(chat_id: str):
            """Obtiene todos los mensajes de un chat"""
            result = self.service.get_messages_by_chat_id(chat_id)
            
            if result["success"]:
                return {
                    "status": "success",
                    "data": result["data"],
                    "total": result["total"],
                    "chat_id": result["chat_id"]
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