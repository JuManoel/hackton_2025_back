from typing import List, Optional
from bson import ObjectId
from app.src.models.Chat import Chat
from app.src.database.connection import db_connection

class RepositoryChat:
    def __init__(self):
        self.db = db_connection.get_database()
        self.collection = self.db["chats"]
    
    def create_chat(self, chat: Chat) -> Chat:
        """Crea un nuevo chat en la base de datos"""
        try:
            chat_dict = chat.to_dict()
            # Eliminar _id si es None para que MongoDB genere uno nuevo
            if chat_dict["_id"] is None:
                del chat_dict["_id"]
            
            result = self.collection.insert_one(chat_dict)
            chat._id = result.inserted_id
            return chat
        except Exception as e:
            print(f"Error al crear chat: {e}")
            raise e
    
    def get_chat_by_id(self, chat_id: str) -> Optional[Chat]:
        """Obtiene un chat por su ID"""
        try:
            obj_id = ObjectId(chat_id)
            chat_data = self.collection.find_one({"_id": obj_id})
            
            if chat_data:
                return Chat.from_dict(chat_data)
            return None
        except Exception as e:
            print(f"Error al obtener chat: {e}")
            return None
    
    def get_all_chats(self) -> List[Chat]:
        """Obtiene todos los chats ordenados por fecha de creación"""
        try:
            chats_data = self.collection.find().sort("datetime", -1)
            return [Chat.from_dict(chat_data) for chat_data in chats_data]
        except Exception as e:
            print(f"Error al obtener chats: {e}")
            return []
    