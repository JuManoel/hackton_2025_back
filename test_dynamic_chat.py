#!/usr/bin/env python3
"""
Script de prueba para las nuevas funcionalidades dinámicas de chat
"""

import os
import sys
import asyncio
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

async def test_dynamic_chat_functionality():
    """Prueba las nuevas funcionalidades dinámicas"""
    try:
        print("🚀 PROBANDO FUNCIONALIDADES DINÁMICAS DE CHAT\n")
        
        # Importar clases necesarias
        from app.src.service.ServiceChat import ServiceChat
        from app.src.service.ServiceMessage import ServiceMessage
        from app.src.database.connection import db_connection
        
        print("✅ Imports exitosos")
        
        # Inicializar servicios
        chat_service = ServiceChat()
        message_service = ServiceMessage()
        
        print("✅ Servicios inicializados")
        
        # 1. Crear un nuevo chat
        print("\n📝 Creando nuevo chat...")
        chat_result = chat_service.create_chat()
        
        if chat_result["success"]:
            chat_id = chat_result["data"]["id"]
            print(f"✅ Chat creado con ID: {chat_id}")
        else:
            print(f"❌ Error al crear chat: {chat_result['error']}")
            return
        
        # 2. Probar envío de mensaje con streaming (simulado)
        print(f"\n💬 Enviando mensaje al chat {chat_id}...")
        test_message = "Hola, soy Juan y soy estudiante de ingeniería"
        
        try:
            response_chunks = []
            async for chunk in message_service.create_message_with_response_streaming(chat_id, test_message):
                print(f"📨 Chunk recibido: {chunk.get('type', 'unknown')} - {chunk.get('content', '')[:50]}...")
                response_chunks.append(chunk)
                
                # Simular pequeña pausa para ver el streaming
                await asyncio.sleep(0.1)
            
            print(f"✅ Mensaje procesado con {len(response_chunks)} chunks")
        except Exception as e:
            print(f"❌ Error en streaming: {e}")
        
        # 3. Obtener historial del chat
        print(f"\n📋 Obteniendo historial del chat {chat_id}...")
        history_result = message_service.get_messages_by_chat_id(chat_id)
        
        if history_result["success"]:
            messages = history_result["data"]
            print(f"✅ Historial obtenido: {len(messages)} mensajes")
            for i, msg in enumerate(messages, 1):
                print(f"   {i}. [{msg['role']}] {msg['content'][:50]}...")
        else:
            print(f"❌ Error al obtener historial: {history_result['error']}")
        
        # 4. Obtener todos los chats
        print("\n📚 Obteniendo todos los chats...")
        all_chats_result = chat_service.get_all_chats()
        
        if all_chats_result["success"]:
            chats = all_chats_result["data"]
            print(f"✅ {len(chats)} chats encontrados")
            for i, chat in enumerate(chats, 1):
                last_msg = chat.get("last_message")
                print(f"   {i}. Chat {chat['id'][:8]}... - {chat['message_count']} mensajes")
                if last_msg:
                    print(f"      Último: [{last_msg['role']}] {last_msg['content'][:30]}...")
        else:
            print(f"❌ Error al obtener chats: {all_chats_result['error']}")
        
        # 5. Enviar otro mensaje para probar contexto
        print(f"\n💬 Enviando segundo mensaje con contexto...")
        second_message = "¿Qué lenguajes me recomiendas para machine learning?"
        
        try:
            response_chunks = []
            async for chunk in message_service.create_message_with_response_streaming(chat_id, second_message):
                print(f"📨 Chunk: {chunk.get('type', 'unknown')} - {chunk.get('content', '')[:30]}...")
                response_chunks.append(chunk)
                await asyncio.sleep(0.1)
            
            print(f"✅ Segundo mensaje procesado con {len(response_chunks)} chunks")
        except Exception as e:
            print(f"❌ Error en segundo mensaje: {e}")
        
        # 6. Verificar historial actualizado
        print(f"\n📋 Verificando historial actualizado...")
        updated_history = message_service.get_messages_by_chat_id(chat_id)
        
        if updated_history["success"]:
            messages = updated_history["data"]
            print(f"✅ Historial actualizado: {len(messages)} mensajes")
            for i, msg in enumerate(messages, 1):
                print(f"   {i}. [{msg['role']}] {msg['content'][:50]}...")
        
        print("\n🎉 ¡TODAS LAS PRUEBAS DINÁMICAS COMPLETADAS!")
        
    except Exception as e:
        print(f"❌ Error en pruebas dinámicas: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Función principal"""
    asyncio.run(test_dynamic_chat_functionality())

if __name__ == "__main__":
    main()
