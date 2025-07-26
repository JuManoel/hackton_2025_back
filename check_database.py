#!/usr/bin/env python3
"""
Script simple para verificar el estado de la base de datos MongoDB
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Cargar variables de entorno
load_dotenv()

def show_database_status():
    """Muestra el estado actual de la base de datos"""
    try:
        # Conectar a MongoDB
        mongo_url = os.getenv("MONGO_URL")
        client = MongoClient(mongo_url)
        db = client["hackaton_chat"]
        
        print("📊 ESTADO DE LA BASE DE DATOS 'hackaton_chat'")
        print("=" * 50)
        
        # Mostrar colecciones
        collections = db.list_collection_names()
        print(f"📁 Colecciones disponibles: {collections}")
        
        # Mostrar estadísticas de cada colección
        for collection_name in collections:
            collection = db[collection_name]
            count = collection.count_documents({})
            print(f"   📝 {collection_name}: {count} documentos")
            
            # Mostrar algunos ejemplos si hay documentos
            if count > 0:
                examples = list(collection.find().limit(2))
                for i, doc in enumerate(examples, 1):
                    # Ocultar el _id para mejor legibilidad
                    doc_copy = {k: v for k, v in doc.items() if k != '_id'}
                    print(f"      Ejemplo {i}: {doc_copy}")
        
        print("\n✅ Base de datos lista para usar!")
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    show_database_status()
