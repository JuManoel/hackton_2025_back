#!/usr/bin/env python3
"""
Script para probar las APIs del servidor FastAPI
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Prueba todos los endpoints del API"""
    print("🚀 PROBANDO APIs DEL SERVIDOR FASTAPI\n")
    
    # 1. Probar health check
    print("🔍 1. Verificando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print("   ✅ Health check OK\n")
    except Exception as e:
        print(f"   ❌ Error en health check: {e}\n")
        return
    
    # 2. Crear un nuevo chat
    print("📝 2. Creando nuevo chat...")
    try:
        response = requests.post(f"{BASE_URL}/api/chat/")
        chat_data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {chat_data}")
        
        if response.status_code == 200 and chat_data.get("status") == "success":
            chat_id = chat_data["data"]["id"]
            print(f"   ✅ Chat creado con ID: {chat_id}\n")
        else:
            print("   ❌ Error al crear chat\n")
            return
    except Exception as e:
        print(f"   ❌ Error al crear chat: {e}\n")
        return
    
    # 3. Obtener todos los chats
    print("📚 3. Obteniendo todos los chats...")
    try:
        response = requests.get(f"{BASE_URL}/api/chat/")
        chats_data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Total chats: {chats_data.get('total', 0)}")
        print("   ✅ Chats obtenidos correctamente\n")
    except Exception as e:
        print(f"   ❌ Error al obtener chats: {e}\n")
    
    # 4. Enviar mensaje al chat (sin streaming por simplicidad)
    print(f"💬 4. Enviando mensaje al chat {chat_id}...")
    try:
        message_data = {
            "content": "Hola, soy Juan y estudio ingeniería de sistemas"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/message/chat/{chat_id}",
            json=message_data,
            stream=True,
            headers={"Accept": "text/event-stream"}
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   📨 Recibiendo respuesta streaming...")
            response_chunks = []
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith('data: '):
                    try:
                        chunk_data = json.loads(line[6:])  # Remover 'data: '
                        if chunk_data.get("type") == "content":
                            response_chunks.append(chunk_data.get("content", ""))
                        elif chunk_data.get("type") == "done":
                            break
                        elif chunk_data.get("type") == "error":
                            print(f"   ❌ Error en streaming: {chunk_data.get('error')}")
                            break
                    except json.JSONDecodeError:
                        continue
            
            full_response = ''.join(response_chunks)
            print(f"   ✅ Respuesta recibida ({len(response_chunks)} chunks)")
            print(f"   📄 Respuesta: {full_response[:100]}...")
            print()
        else:
            print(f"   ❌ Error al enviar mensaje: {response.text}\n")
    except Exception as e:
        print(f"   ❌ Error al enviar mensaje: {e}\n")
    
    # 5. Obtener historial del chat
    print(f"📋 5. Obteniendo historial del chat {chat_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/message/chat/{chat_id}")
        history_data = response.json()
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            messages = history_data["data"]
            print(f"   📝 {len(messages)} mensajes en el historial:")
            for i, msg in enumerate(messages, 1):
                print(f"      {i}. [{msg['role']}] {msg['content'][:50]}...")
            print("   ✅ Historial obtenido correctamente\n")
        else:
            print(f"   ❌ Error al obtener historial: {history_data}\n")
    except Exception as e:
        print(f"   ❌ Error al obtener historial: {e}\n")
    
    # 6. Enviar segundo mensaje para probar contexto
    print(f"💬 6. Enviando segundo mensaje con contexto...")
    try:
        message_data = {
            "content": "¿Qué tecnologías me recomiendas para desarrollo web?"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/message/chat/{chat_id}",
            json=message_data,
            stream=True,
            headers={"Accept": "text/event-stream"}
        )
        
        if response.status_code == 200:
            print("   📨 Recibiendo segunda respuesta...")
            response_chunks = []
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith('data: '):
                    try:
                        chunk_data = json.loads(line[6:])
                        if chunk_data.get("type") == "content":
                            response_chunks.append(chunk_data.get("content", ""))
                        elif chunk_data.get("type") == "done":
                            break
                    except json.JSONDecodeError:
                        continue
            
            full_response = ''.join(response_chunks)
            print(f"   ✅ Segunda respuesta recibida ({len(response_chunks)} chunks)")
            print(f"   📄 Respuesta: {full_response[:100]}...")
            print()
        else:
            print(f"   ❌ Error en segundo mensaje: {response.text}\n")
    except Exception as e:
        print(f"   ❌ Error en segundo mensaje: {e}\n")
    
    # 7. Verificar historial final
    print(f"📋 7. Verificando historial final...")
    try:
        response = requests.get(f"{BASE_URL}/api/message/chat/{chat_id}")
        final_history = response.json()
        
        if response.status_code == 200:
            messages = final_history["data"]
            print(f"   📝 {len(messages)} mensajes finales:")
            for i, msg in enumerate(messages, 1):
                print(f"      {i}. [{msg['role']}] {msg['content'][:50]}...")
            print("   ✅ Historial final verificado\n")
        else:
            print(f"   ❌ Error al verificar historial final\n")
    except Exception as e:
        print(f"   ❌ Error al verificar historial final: {e}\n")
    
    print("🎉 ¡PRUEBAS DEL API COMPLETADAS!")

if __name__ == "__main__":
    print("⏳ Esperando 2 segundos para que el servidor esté listo...")
    time.sleep(2)
    test_api_endpoints()
