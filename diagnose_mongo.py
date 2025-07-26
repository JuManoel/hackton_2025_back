#!/usr/bin/env python3
"""
Script para diagnosticar problemas de conexión MongoDB
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus

# Cargar variables de entorno
load_dotenv()

def test_different_connection_strings():
    """Prueba diferentes configuraciones de conexión"""
    
    print("🔍 DIAGNÓSTICO DE CONEXIÓN MONGODB\n")
    
    # Obtener URL original
    original_url = os.getenv("MONGO_URL")
    print(f"URL original: {original_url}")
    
    # Diferentes configuraciones para probar
    test_configs = [
        {
            "name": "Configuración original",
            "url": original_url
        },
        {
            "name": "Con encoding de credenciales",
            "url": "mongodb+srv://{}:{}@hackton2025.dxzwfib.mongodb.net/?retryWrites=true&w=majority&appName=hackton2025".format(
                quote_plus("juanmiranda41303"), 
                quote_plus("manoel2004")
            )
        },
        {
            "name": "Sin parámetros adicionales",
            "url": "mongodb+srv://juanmiranda41303:manoel2004@hackton2025.dxzwfib.mongodb.net/"
        },
        {
            "name": "Con base de datos específica",
            "url": "mongodb+srv://juanmiranda41303:manoel2004@hackton2025.dxzwfib.mongodb.net/hackaton_chat?retryWrites=true&w=majority"
        }
    ]
    
    for i, config in enumerate(test_configs, 1):
        print(f"\n{i}. Probando: {config['name']}")
        print(f"   URL: {config['url'][:50]}...")
        
        try:
            client = MongoClient(config['url'], serverSelectionTimeoutMS=5000)
            
            # Probar ping
            client.admin.command('ping')
            print("   ✅ Conexión exitosa!")
            
            # Listar bases de datos
            dbs = client.list_database_names()
            print(f"   📊 Bases de datos disponibles: {dbs}")
            
            # Probar acceso a nuestra base de datos
            db = client["hackaton_chat"]
            collections = db.list_collection_names()
            print(f"   📁 Colecciones en hackaton_chat: {collections}")
            
            client.close()
            return config['url']  # Retornar la URL que funcionó
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    return None

def suggest_solutions():
    """Sugiere posibles soluciones"""
    print("\n🔧 POSIBLES SOLUCIONES:")
    print("1. Verificar credenciales en MongoDB Atlas")
    print("2. Verificar que el usuario tenga permisos de lectura/escritura")
    print("3. Verificar Network Access (IP Whitelist) en MongoDB Atlas")
    print("4. Verificar que el cluster esté activo")
    print("5. Probar crear un nuevo usuario en MongoDB Atlas")
    
    print("\n📋 PASOS PARA VERIFICAR EN MONGODB ATLAS:")
    print("1. Ir a https://cloud.mongodb.com/")
    print("2. Seleccionar tu proyecto")
    print("3. En 'Database Access' verificar usuario y contraseña")
    print("4. En 'Network Access' agregar 0.0.0.0/0 (allow from anywhere)")
    print("5. En 'Database' verificar que el cluster esté corriendo")

def main():
    working_url = test_different_connection_strings()
    
    if working_url:
        print(f"\n🎉 ¡CONEXIÓN EXITOSA! URL que funciona:")
        print(f"{working_url}")
        
        # Actualizar .env si es necesario
        original_url = os.getenv("MONGO_URL")
        if working_url != original_url:
            print(f"\n💡 Considera actualizar tu .env con esta URL:")
            print(f"MONGO_URL={working_url}")
    else:
        print("\n❌ No se pudo establecer conexión con ninguna configuración")
        suggest_solutions()

if __name__ == "__main__":
    main()
