#!/usr/bin/env python3
"""
Script de debug para verificar la conexión a MongoDB y crear las colecciones
"""

import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# Cargar variables de entorno
load_dotenv()

def test_mongo_connection():
    """Prueba la conexión a MongoDB"""
    try:
        print("🔄 Probando conexión a MongoDB...")
        
        # Obtener URL de MongoDB desde variables de entorno
        mongo_url = os.getenv("MONGO_URL")
        if not mongo_url:
            print("❌ ERROR: MONGO_URL no encontrada en variables de entorno")
            return False
            
        print(f"📡 Conectando a: {mongo_url[:50]}...")
        
        # Crear cliente de MongoDB
        client = MongoClient(mongo_url)
        
        # Probar conexión
        client.admin.command('ping')
        print("✅ Conexión a MongoDB exitosa!")
        
        # Obtener base de datos
        db = client["hackaton_chat"]
        print(f"📊 Base de datos seleccionada: {db.name}")
        
        return True, client, db
        
    except Exception as e:
        print(f"❌ Error al conectar a MongoDB: {str(e)}")
        return False, None, None

def create_collections_and_test(db):
    """Crea las colecciones y hace pruebas básicas"""
    try:
        print("\n🏗️  Creando y probando colecciones...")
        
        # Crear colección de chats
        chats_collection = db["chats"]
        messages_collection = db["messages"]
        
        # Probar inserción en chats
        print("📝 Probando inserción en colección 'chats'...")
        test_chat = {
            "datetime": datetime.now()
        }
        
        chat_result = chats_collection.insert_one(test_chat)
        chat_id = chat_result.inserted_id
        print(f"✅ Chat de prueba creado con ID: {chat_id}")
        
        # Probar inserción en messages
        print("📝 Probando inserción en colección 'messages'...")
        test_message = {
            "chat_id": chat_id,
            "role": "user",
            "content": "Mensaje de prueba para verificar conexión",
            "datetime": datetime.now()
        }
        
        message_result = messages_collection.insert_one(test_message)
        message_id = message_result.inserted_id
        print(f"✅ Mensaje de prueba creado con ID: {message_id}")
        
        # Verificar que podemos leer los datos
        print("\n🔍 Verificando lectura de datos...")
        
        # Leer chat
        chat_found = chats_collection.find_one({"_id": chat_id})
        if chat_found:
            print(f"✅ Chat encontrado: datetime={chat_found['datetime']}")
        
        # Leer mensaje
        message_found = messages_collection.find_one({"_id": message_id})
        if message_found:
            print(f"✅ Mensaje encontrado: content='{message_found['content']}'")
        
        # Leer mensajes por chat_id
        messages_in_chat = list(messages_collection.find({"chat_id": chat_id}))
        print(f"✅ Mensajes en el chat: {len(messages_in_chat)}")
        
        # Limpiar datos de prueba
        print("\n🧹 Limpiando datos de prueba...")
        chats_collection.delete_one({"_id": chat_id})
        messages_collection.delete_one({"_id": message_id})
        print("✅ Datos de prueba eliminados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear/probar colecciones: {str(e)}")
        return False

def test_repository_classes():
    """Prueba las clases de repository"""
    try:
        print("\n🧪 Probando clases de Repository...")
        
        # Importar clases necesarias
        from app.src.database.connection import db_connection
        from app.src.repository.RepositoryChat import RepositoryChat
        from app.src.repository.RepositoryMessage import RepositoryMessage
        from app.src.models.Chat import Chat
        from app.src.models.Message import Message
        
        print("✅ Imports de clases exitosos")
        
        # Probar conexión desde clase singleton
        db = db_connection.get_database()
        print(f"✅ Conexión desde singleton: {db.name}")
        
        # Probar RepositoryChat
        print("📝 Probando RepositoryChat...")
        repo_chat = RepositoryChat()
        
        # Crear chat de prueba
        test_chat = Chat()
        created_chat = repo_chat.create_chat(test_chat)
        print(f"✅ Chat creado desde Repository: {created_chat._id}")
        
        # Recuperar chat
        found_chat = repo_chat.get_chat_by_id(str(created_chat._id))
        if found_chat:
            print(f"✅ Chat recuperado: datetime={found_chat.datetime}")
        
        # Probar RepositoryMessage
        print("📝 Probando RepositoryMessage...")
        repo_message = RepositoryMessage()
        
        # Crear mensaje de prueba
        test_message = Message(
            chat_id=created_chat._id,
            role="user",
            content="Mensaje de prueba desde Repository"
        )
        created_message = repo_message.create_message(test_message)
        print(f"✅ Mensaje creado desde Repository: {created_message._id}")
        
        # Recuperar mensaje
        found_message = repo_message.get_message_by_id(str(created_message._id))
        if found_message:
            print(f"✅ Mensaje recuperado: content='{found_message.content}'")
        
        # Recuperar mensajes por chat
        messages_in_chat = repo_message.get_messages_by_chat_id(str(created_chat._id))
        print(f"✅ Mensajes en chat desde Repository: {len(messages_in_chat)}")
        
        print("✅ Todas las pruebas de Repository exitosas!")
        return True
        
    except Exception as e:
        print(f"❌ Error al probar Repository classes: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal de debug"""
    print("🚀 INICIANDO DEBUG DE CONEXIÓN MONGODB\n")
    
    # Probar conexión básica
    success, client, db = test_mongo_connection()
    if not success:
        print("❌ No se pudo establecer conexión. Abortando...")
        return
    
    # Probar colecciones
    if create_collections_and_test(db):
        print("✅ Pruebas de colecciones exitosas!")
    else:
        print("❌ Falló la prueba de colecciones")
        return
    
    # Cerrar conexión básica
    client.close()
    
    # Probar clases de Repository
    if test_repository_classes():
        print("\n🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("✅ MongoDB conectado correctamente")
        print("✅ Colecciones funcionando")
        print("✅ Clases Repository funcionando")
    else:
        print("\n❌ Falló alguna prueba de Repository")

if __name__ == "__main__":
    main()
