from typing import List, Optional, Dict
from app.src.models.Chat import Chat
from app.src.repository.RepositoryChat import RepositoryChat
from app.src.repository.RepositoryMessage import RepositoryMessage

class ServiceChat:
    def __init__(self):
        self.chat_repository = RepositoryChat()
        self.message_repository = RepositoryMessage()
    
    def create_chat(self) -> Dict:
        """Crea un nuevo chat"""
        try:
            chat = Chat()
            created_chat = self.chat_repository.create_chat(chat)
            
            return {
                "success": True,
                "data": {
                    "id": str(created_chat._id),
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
                    "datetime": chat.datetime.isoformat()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener chat: {str(e)}",
                "message": "No se pudo obtener el chat"
            }
    
    def get_all_chats(self) -> Dict:
        """Obtiene todos los chats"""
        try:
            chats = self.chat_repository.get_all_chats()
            
            chats_data = []
            for chat in chats:
                # Obtener el último mensaje para preview
                messages = self.message_repository.get_messages_by_chat_id(str(chat._id))
                last_message = messages[-1] if messages else None
                
                chat_data = {
                    "id": str(chat._id),
                    "datetime": chat.datetime.isoformat(),
                    "message_count": len(messages),
                    "last_message": {
                        "content": last_message.content[:100] + "..." if last_message and len(last_message.content) > 100 else last_message.content if last_message else None,
                        "datetime": last_message.datetime.isoformat() if last_message else None,
                        "role": last_message.role if last_message else None
                    } if last_message else None
                }
                chats_data.append(chat_data)
            
            return {
                "success": True,
                "data": chats_data,
                "total": len(chats_data)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener chats: {str(e)}",
                "message": "No se pudieron obtener los chats"
            }
    