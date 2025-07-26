import os
from pymongo import MongoClient
from pymongo.database import Database

class DatabaseConnection:
    _instance = None
    _client = None
    _database = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self.connect()
    
    def connect(self):
        """Establece la conexión con MongoDB"""
        try:
            mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
            self._client = MongoClient(mongo_url)
            self._database = self._client["hackaton_chat"]
            print("Conexión a MongoDB establecida correctamente")
        except Exception as e:
            print(f"Error al conectar con MongoDB: {e}")
            raise e
    
    def get_database(self) -> Database:
        """Retorna la instancia de la base de datos"""
        if self._database is None:
            self.connect()
        return self._database
    
    def close_connection(self):
        """Cierra la conexión con MongoDB"""
        if self._client:
            self._client.close()
            self._client = None
            self._database = None
            print("Conexión a MongoDB cerrada")

# Instancia global de la conexión
db_connection = DatabaseConnection()
