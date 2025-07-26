from typing import List, Optional
from bson import ObjectId
from app.src.models.Message import Message
from app.src.database.connection import db_connection

class RepositoryMessage:
    def __init__(self):
        self.db = db_connection.get_database()
        self.collection = self.db["messages"]
    
    def create_message(self, message: Message) -> Message:
        """Crea un nuevo mensaje en la base de datos"""
        try:
            message_dict = message.to_dict()
            # Eliminar _id si es None para que MongoDB genere uno nuevo
            if message_dict["_id"] is None:
                del message_dict["_id"]
            
            result = self.collection.insert_one(message_dict)
            message._id = result.inserted_id
            return message
        except Exception as e:
            print(f"Error al crear mensaje: {e}")
            raise e
    
    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        """Obtiene un mensaje por su ID"""
        try:
            obj_id = ObjectId(message_id)
            message_data = self.collection.find_one({"_id": obj_id})
            
            if message_data:
                return Message.from_dict(message_data)
            return None
        except Exception as e:
            print(f"Error al obtener mensaje: {e}")
            return None
    
    def get_messages_by_chat_id(self, chat_id: str) -> List[Message]:
        """Obtiene todos los mensajes de un chat ordenados por fecha"""
        try:
            obj_id = ObjectId(chat_id)
            messages_data = self.collection.find({"chat_id": obj_id}).sort("datetime", 1)
            return [Message.from_dict(message_data) for message_data in messages_data]
        except Exception as e:
            print(f"Error al obtener mensajes del chat: {e}")
            return []
    