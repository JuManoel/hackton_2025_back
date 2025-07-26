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
        faq_content = """
        Esas son las Prenguntas Frecuentes (FAQ):
        
        ¿Quién es Ingelean S.A.S.?
        Empresa colombiana fundada en 2013, especializada en soluciones de ingeniería Industria 4.0. NIT 900614119‑8, sede en Pereira, Risaralda.

        ¿Misión y visión?
        Misión: Optimizar procesos industriales mediante soluciones tecnológicas innovadoras.
        Visión: Líderes globales Industria 4.0 para 2026.

        ¿Servicios ofrecidos?
        • Automatización industrial y parqueaderos
        • Hardware embebido (PCBs, sistemas análogo/digital)
        • Software (cloud, visión computador, ML)
        • Tarjetas NFC personalizadas
        • Telemetría, M2M, domótica, consultoría

        ¿Automatización industrial?
        Diagnóstico, diseño, simulación, programación PLCs y sistemas de control automático.

        ¿Automatización parqueaderos?
        ANPR, talanqueras RFID, tiquetes, software gestión vehicular.

        ¿IngeleanPlus?
        Ecosistema digital para análisis datos tiempo real, gestión recursos y monitoreo continuo.

        ¿Cobertura geográfica?
        Nacional: Risaralda, Caldas, Quindío, Magdalena, Bolívar, Cundinamarca, Antioquia, Valle, Chocó.
        Internacional: España, Paraguay.

        ¿Qué tipo de clientes atiende Ingelean?
        Empresas industriales, manufactureras, tecnológicas y de servicios que buscan transformación digital, optimización de procesos y soluciones a medida en automatización, software y hardware.

        ¿Qué metodologías de trabajo utiliza Ingelean?
        Implementamos metodologías ágiles como Scrum, con enfoque colaborativo, iterativo y flexible. Aseguramos entregas parciales y mejora continua con participación activa del cliente.

        ¿Contacto?
        Web: www.ingelean.com
        Tel: +57 311 419 6803 / +57 321 594 2872 / 324 607 9894
        Email: comercial@ingelean.com
        WhatsApp: wa.me/573043262538
        """

        self.system_prompt = f"""
        Eres un agente analizador de mensajes especializado en evaluar interacciones de servicio al cliente de Ingelean.

        Tu función es analizar mensajes y retornar métricas específicas según el tipo de remitente:

        PARA MENSAJES DE IA/MODEL/ASISTENTE:
        Evalúa la precisión. Retorna JSON:
        {{
            "precision": [número entre 0-100]
        }}

        Criterios de precisión:
        - 90-100: Información completamente correcta y relevante al contexto de Ingelean
        - 70-89: Información mayormente correcta con detalles menores incorrectos
        - 50-69: Información parcialmente correcta pero con errores significativos
        - 30-49: Información con errores importantes o irrelevante
        - 0-29: Información incorrecta o completamente irrelevante

        PARA MENSAJES DE USUARIO:
        Evalúa el nivel de satisfacción implícito. Retorna JSON:
        {{
            "satisfacion": [número entre 0-100]
        }}

        Criterios de satisfacción:
        - 80-100: Muy satisfecho (agradecimientos, elogios, confirmaciones positivas)
        - 60-79: Satisfecho (neutral positivo, acepta propuestas)
        - 40-59: Neutral (sin indicadores claros de satisfacción/insatisfacción)
        - 20-39: Insatisfecho (quejas menores, dudas, solicita aclaraciones)
        - 0-19: Muy insatisfecho (quejas fuertes, críticas, frustración)

        CONTEXTO DE EVALUACIÓN:
        {faq_content}

        INFORMACIÓN TÉCNICA DE REFERENCIA:
        {self.pdf_text}

        Analiza cada mensaje considerando este contexto empresarial y retorna ÚNICAMENTE el JSON correspondiente.
        """

    def _get_info(self):
        """Extrae el contenido del PDF para usarlo como contexto"""
        try:
            with open(self.path_info, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                self.pdf_text = ""
                for page in pdf_reader.pages:
                    self.pdf_text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error al leer el PDF: {e}")
            self.pdf_text = ""

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
