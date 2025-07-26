from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.src.service.ServiceMessage import ServiceMessage
from API.Gemini import Gemini
import json
import asyncio

# Modelos Pydantic para request/response
class MessageCreateRequest(BaseModel):
    content: str  # Solo necesitamos el contenido para el test

class MessageUpdateRequest(BaseModel):
    content: str

class ControllerMessage:
    def __init__(self):
        self.router = APIRouter(prefix="/api/message", tags=["Message"])
        self.service = ServiceMessage()
        self._setup_routes()
        self.model = Gemini()
    
    async def _generate_response(self, result):
        """Genera respuesta en streaming"""
        try:
            for chunk in result:
                if chunk.text:  # Solo enviar si hay texto
                    chunk_data = {
                        "content": chunk.text,
                        "type": "content"
                    }
                    yield f"data: {json.dumps(chunk_data)}\n\n"
            
            # Señal de finalización
            final_data = {
                "content": "",
                "type": "done"
            }
            yield f"data: {json.dumps(final_data)}\n\n"
        except Exception as e:
            error_data = {
                "error": str(e),
                "type": "error"
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    def _setup_routes(self):
        """Configura las rutas del controlador"""
        # Rutas dinámicas para chat persistente
        @self.router.post("/chat/{chat_id}")
        async def create_message_in_chat(chat_id: str, request: MessageCreateRequest):
            """Crea un nuevo mensaje en un chat específico con respuesta streaming"""
            try:
                async def generate_response():
                    try:
                        async for chunk in self.service.create_message_with_response_streaming(chat_id, request.content):
                            if chunk.get("type") == "error":
                                error_data = {
                                    "error": chunk.get("error", "Error desconocido"),
                                    "type": "error"
                                }
                                yield f"data: {json.dumps(error_data)}\n\n"
                                return
                            
                            chunk_data = {
                                "content": chunk.get("content", ""),
                                "type": chunk.get("type", "content"),
                                "user_message_id": chunk.get("user_message_id")
                            }
                            yield f"data: {json.dumps(chunk_data)}\n\n"
                    except Exception as e:
                        error_data = {
                            "error": str(e),
                            "type": "error"
                        }
                        yield f"data: {json.dumps(error_data)}\n\n"
                
                return StreamingResponse(
                    generate_response(),
                    media_type="text/event-stream",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                        "Content-Type": "text/event-stream",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "*"
                    }
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error al procesar mensaje: {str(e)}"
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