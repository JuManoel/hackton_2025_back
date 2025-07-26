from datetime import datetime
from typing import Optional
from bson import ObjectId

class Message:
    def __init__(self, role: str, content: str, chat_id: Optional[ObjectId] = None):
        self._id: Optional[ObjectId] = None
        self.role = role
        self.content = content
        self.datetime = datetime.now()
        self.chat_id = chat_id
    
    def to_dict(self):
        """Convierte el objeto a diccionario para MongoDB"""
        return {
            "_id": self._id,
            "role": self.role,
            "content": self.content,
            "datetime": self.datetime,
            "chat_id": self.chat_id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Message desde un diccionario de MongoDB"""
        message = cls(
            role=data.get("role", "user"),
            content=data.get("content", ""),
            chat_id=data.get("chat_id")
        )
        message._id = data.get("_id")
        message.datetime = data.get("datetime", datetime.now())
        return message
        