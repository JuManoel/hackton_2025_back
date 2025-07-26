from typing import List, Optional, Dict
from bson import ObjectId
from app.src.models.Message import Message
from app.src.repository.RepositoryMessage import RepositoryMessage
from app.src.repository.RepositoryChat import RepositoryChat
from API.Gemini import Gemini
from API.Mistral import MistralAPI


class ServiceMessage:
    def __init__(self):
        self.message_repository = RepositoryMessage()
        self.chat_repository = RepositoryChat()
        self.model = Gemini()
    
    def create_message(self, chat_id: str, content: str) -> Dict:
        """Crea un nuevo mensaje en un chat"""
        try:
            # Verificar que el chat existe
            chat = self.chat_repository.get_chat_by_id(chat_id)
            if not chat:
                return {
                    "success": False,
                    "error": "Chat no encontrado",
                    "message": "El chat especificado no existe"
                }
            
            history = self.message_repository.get_messages_by_chat_id(chat_id)


            # Crear el mensaje
            message = Message(role="user", content=content, chat_id=ObjectId(chat_id))
            created_message = self.message_repository.create_message(message)
            
            #generar respuesta por el utilizando Modelo
            if not history:
                respuesta = self.model.responder_pregunta(content)
            else:
                history_dict = []
                for msg in history:
                    history_dict.append({
                        "role": msg.role,
                        "content": msg.content
                    })
                respuesta = self.model.responder_pregunta_con_contexto(content, history_dict)

            message = Message(role="model", content=respuesta, chat_id=ObjectId(chat_id))

            return {
                "success": True,
                "data": {
                    "id": str(created_message._id),
                    "role": created_message.role,
                    "content": created_message.content,
                    "datetime": created_message.datetime.isoformat(),
                    "chat_id": str(created_message.chat_id)
                },
                "message": "Mensaje creado exitosamente"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al crear mensaje: {str(e)}",
                "message": "No se pudo crear el mensaje"
            }
    
    def get_message_by_id(self, message_id: str) -> Dict:
        """Obtiene un mensaje por su ID"""
        try:
            message = self.message_repository.get_message_by_id(message_id)
            
            if not message:
                return {
                    "success": False,
                    "error": "Mensaje no encontrado",
                    "message": "El mensaje solicitado no existe"
                }
            
            return {
                "success": True,
                "data": {
                    "id": str(message._id),
                    "role": message.role,
                    "content": message.content,
                    "datetime": message.datetime.isoformat(),
                    "chat_id": str(message.chat_id)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener mensaje: {str(e)}",
                "message": "No se pudo obtener el mensaje"
            }
    
    def get_messages_by_chat_id(self, chat_id: str) -> Dict:
        """Obtiene todos los mensajes de un chat"""
        try:
            # Verificar que el chat existe
            chat = self.chat_repository.get_chat_by_id(chat_id)
            if not chat:
                return {
                    "success": False,
                    "error": "Chat no encontrado",
                    "message": "El chat especificado no existe"
                }
            
            messages = self.message_repository.get_messages_by_chat_id(chat_id)
            
            messages_data = []
            for message in messages:
                messages_data.append({
                    "id": str(message._id),
                    "role": message.role,
                    "content": message.content,
                    "datetime": message.datetime.isoformat(),
                    "chat_id": str(message.chat_id)
                })
            
            return {
                "success": True,
                "data": messages_data,
                "total": len(messages_data),
                "chat_id": chat_id
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener mensajes: {str(e)}",
                "message": "No se pudieron obtener los mensajes"
            }
    
    
    def get_chat_conversation_context(self, chat_id: str) -> List[Dict]:
        """Obtiene el contexto de conversación para las APIs de LLM"""
        try:
            messages = self.message_repository.get_messages_by_chat_id(chat_id)
            context = []
            
            for message in messages:
                context.append({
                    "role": message.role,
                    "parts": message.content
                })
            
            return context
        except Exception as e:
            print(f"Error al obtener contexto de conversación: {e}")
            return []