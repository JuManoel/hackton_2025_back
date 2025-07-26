from datetime import datetime
from typing import Optional
from bson import ObjectId

class Chat:
    def __init__(self):
        self._id: Optional[ObjectId] = None
        self.datetime = datetime.now()
    
    def to_dict(self):
        """Convierte el objeto a diccionario para MongoDB"""
        return {
            "_id": self._id,
            "datetime": self.datetime
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Chat desde un diccionario de MongoDB"""
        chat = cls(data.get("title", "Nuevo Chat"))
        chat._id = data.get("_id")
        chat.datetime = data.get("datetime", datetime.now())
        return chat