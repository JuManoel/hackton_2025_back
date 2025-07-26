from API.interface.ILLMApi import *
from mistralai import Mistral
import os
import PyPDF2

class MistralAPI(ILLMApi):
    def __init__(self):
        super().__init__("mistral-large-latest")
        self.api_key = os.getenv("MISTRAL_API")
        self.client = Mistral(api_key=self.api_key)
        
        self._get_info()
        self.generar_system_prompt("""
        Eres un asistente virtual experto para nuestra empresa. Tu única fuente de conocimiento es el documento PDF que se te ha proporcionado.

        Tu tarea principal es responder a las preguntas de los usuarios basándote exclusivamente en la información contenida en ese documento.

        **Reglas importantes:**

        1.  **Fuente de verdad única:** Toda tu información debe provenir del PDF adjunto. No utilices conocimiento externo ni inventes respuestas. Si la respuesta no está en el documento, indícalo claramente.
        2.  **Enfoque exclusivo:** Responde únicamente a preguntas relacionadas con la empresa y la información del PDF. Si te preguntan sobre cualquier otro tema, declina amablemente la respuesta y redirige la conversación hacia tus funciones como asistente de la empresa.
        3.  **Adaptabilidad en el tono:** Presta mucha atención a cómo se expresa el usuario. Debes adaptar tu tono y estilo de lenguaje para que coincida con el suyo. Por ejemplo:
        *   Si el usuario es muy formal, responde de manera formal.
        *   Si el usuario utiliza un lenguaje coloquial o jerga de una región específica (como la jerga "rola" de Bogotá, con expresiones como "¿qué más, parce?", "chévere", "bacano"), debes incorporar de forma natural y respetuosa un lenguaje similar para que la conversación se sienta más cercana y amigable.
        4.  **Respeto ante todo:** Sin importar el estilo de la conversación, siempre debes ser respetuoso, amable y profesional.
        5.  **Formato de respuesta:** Responde siempre con texto puro. No utilices formato Markdown (como negritas, cursivas, listas, etc.).
        """)

    def _get_info(self):
        """Extrae el contenido del PDF para usarlo como contexto"""
        try:
            with open(self.path_info, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                self.pdf_content = ""
                for page in pdf_reader.pages:
                    self.pdf_content += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error al leer el PDF: {e}")
            self.pdf_content = ""

    def generar_system_prompt(self, system_prompt: str):
        """Genera el prompt del sistema incluyendo el contenido del PDF"""
        self.system_prompt = system_prompt + f"\n\nContenido del documento de la empresa:\n{getattr(self, 'pdf_content', '')}"

    def responder_pregunta(self, pregunta: str):
        """Responde una pregunta sin contexto previo"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user", 
                    "content": pregunta
                }
            ]
            
            response = self.client.chat.complete(
                model=self.model_name,
                messages=messages
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error al procesar la pregunta: {e}"

    def _parse_contexto(self, contexto: list):
        """Convierte el contexto al formato esperado por Mistral"""
        contexto_mistral = []
        for mensaje in contexto:
            contexto_mistral.append({
                "role": mensaje["role"],
                "content": mensaje["content"]
            })
        return contexto_mistral

    def responder_pregunta_con_contexto(self, pregunta: str, contexto: list):
        """Responde una pregunta considerando el contexto de la conversación"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                }
            ]
            
            # Agregar el contexto de la conversación
            contexto_mistral = self._parse_contexto(contexto)
            messages.extend(contexto_mistral)
            
            # Agregar la nueva pregunta
            messages.append({
                "role": "user",
                "content": pregunta
            })
            
            response = self.client.chat.complete(
                model=self.model_name,
                messages=messages
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error al procesar la pregunta con contexto: {e}"
