from typing import List, Optional, Dict
from app.src.models.Chat import Chat
from app.src.repository.RepositoryChat import RepositoryChat
from app.src.repository.RepositoryMessage import RepositoryMessage

class ServiceChat:
    def __init__(self):
        self.chat_repository = RepositoryChat()
        self.message_repository = RepositoryMessage()
    
    def create_chat(self, title: str = "Nuevo Chat") -> Dict:
        """Crea un nuevo chat"""
        try:
            chat = Chat(title=title)
            created_chat = self.chat_repository.create_chat(chat)
            
            return {
                "success": True,
                "data": {
                    "id": str(created_chat._id),
                    "title": created_chat.title,
                    "datetime": created_chat.datetime.isoformat()
                },
                "message": "Chat creado exitosamente"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al crear chat: {str(e)}",
                "message": "No se pudo crear el chat"
            }
    
    def get_chat_by_id(self, chat_id: str) -> Dict:
        """Obtiene un chat por su ID"""
        try:
            chat = self.chat_repository.get_chat_by_id(chat_id)
            
            if not chat:
                return {
                    "success": False,
                    "error": "Chat no encontrado",
                    "message": "El chat solicitado no existe"
                }
            
            return {
                "success": True,
                "data": {
                    "id": str(chat._id),
                    "title": chat.title,
                    "datetime": chat.datetime.isoformat()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener chat: {str(e)}",
                "message": "No se pudo obtener el chat"
            }
    