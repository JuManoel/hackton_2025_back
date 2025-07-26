from typing import Dict
from app.src.repository.RepositoryMessage import RepositoryMessage
from app.src.repository.RepositoryChat import RepositoryChat
from API.Mistral import MistralAPI
import re
import json


class ServiceMetricas:
    def __init__(self):
        self.message_repository = RepositoryMessage()
        self.chat_repository = RepositoryChat()
        self.model = MistralAPI()
    
    def create_analisis(self, chat_id):
        messages = self._get_messages_by_chat_id(chat_id)
        respuesta = []
        satisfacion_list = []
        precision_list = []
        
        for i in range(len(messages["data"])):
            response = self.model.responder_pregunta(f"Escrito por {messages['data'][i]['role']}: "+messages["data"][i]["content"])
            # Usar expresión regular para extraer diccionarios del string
            pattern = r'\{[^{}]*\}'
            matches = re.findall(pattern, response)
            
            for match in matches:
                try:
                    # Convertir el string a diccionario
                    dict_data = json.loads(match)
                    respuesta.append(dict_data)
                except json.JSONDecodeError:
                    # Si no se puede parsear como JSON, intentar con eval (menos seguro)
                    try:
                        dict_data = eval(match)
                        respuesta.append(dict_data)
                    except:
                        continue
        
        # Procesar las respuestas para extraer satisfacción y precisión
        for resp in respuesta:
            if "satisfacion" in resp:
                satisfacion_list.append(resp["satisfacion"])
            if "precision" in resp:
                precision_list.append(resp["precision"])
        
        # Calcular promedios
        satisfacion_promedio = sum(satisfacion_list) / len(satisfacion_list) if satisfacion_list else 0
        precision_promedio = sum(precision_list) / len(precision_list) if precision_list else 0
        
        # Retornar resultado organizado
        return {
            "satisfacion": satisfacion_list,
            "precision": precision_list,
            "satisfacion_promedio": satisfacion_promedio,
            "precision_promedio": precision_promedio
        }
    def _get_messages_by_chat_id(self, chat_id: str) -> Dict:
        """Obtiene todos los mensajes de un chat"""
        try:
            # Verificar que el chat existe
            chat = self.chat_repository.get_chat_by_id(chat_id)
            if not chat:
                return {
                    "success": False,
                    "error": "Chat no encontrado",
                    "message": "El chat especificado no existe"
                }
            
            messages = self.message_repository.get_messages_by_chat_id(chat_id)
            
            messages_data = []
            for message in messages:
                messages_data.append({
                    "role": message.role,
                    "content": message.content,
                })
            
            return {
                "success": True,
                "data": messages_data,
                "total": len(messages_data),
                "chat_id": chat_id
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener mensajes: {str(e)}",
                "message": "No se pudieron obtener los mensajes"
            }
    