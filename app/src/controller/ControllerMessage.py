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
        

        @self.router.post("/")
        async def test_preguntar(request: MessageCreateRequest):
            """Prueba de endpoint para preguntar con streaming"""
            try:
                result = self.model.responder_pregunta(request.content)
                return StreamingResponse(
                    self._generate_response(result),
                    media_type="text/plain",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                        "Content-Type": "text/plain; charset=utf-8"
                    }
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error al generar respuesta: {str(e)}"
                )

        @self.router.post("/chat")
        async def preguntar_con_contexto(request: dict):
            """Endpoint para preguntar con contexto de conversación"""
            try:
                pregunta = request.get("content", "")
                # Contexto de ejemplo si no se proporciona
                contexto_default = [
                    {"role": "user", "content": "Hola, soy Juan y soy estudiante de ingeniería"},
                    {"role": "assistant", "content": "¡Hola Juan! Es un placer conocerte. Como estudiante de ingeniería, seguramente tienes muchos proyectos interesantes. ¿En qué puedo ayudarte hoy?"},
                    {"role": "user", "content": "¿Qué lenguajes de programación me recomiendas?"},
                    {"role": "assistant", "content": "Para ingeniería, te recomiendo Python por su versatilidad y facilidad de aprendizaje, Java para desarrollo robusto, y C++ para sistemas de bajo nivel. También considera JavaScript si te interesa el desarrollo web."},
                    {"role": "user", "content": "¿Cómo puedo mejorar mis habilidades de programación?"},
                    {"role": "assistant", "content": "Te sugiero: 1) Practica diariamente con problemas de coding, 2) Contribuye a proyectos open source, 3) Desarrolla proyectos personales, 4) Lee código de otros programadores, y 5) Participa en hackathons como este."}
                ]
                
                contexto = request.get("context", contexto_default)
                
                if not pregunta:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El campo 'content' es requerido"
                    )
                
                result = self.model.responder_pregunta_con_contexto(pregunta, contexto)

                return StreamingResponse(
                    self._generate_response(result),
                    media_type="text/plain",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                        "Content-Type": "text/plain; charset=utf-8"
                    }
                )
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error al generar respuesta con contexto: {str(e)}"
                )
            

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