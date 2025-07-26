from API.interface.ILLMApi import *
import google.generativeai as genai
from google import genai as export_pdf
import PyPDF2


class Gemini(ILLMApi):
    def __init__(self):
        super().__init__("gemini-2.5-flash")
        self.api_key = os.getenv("GEMINI_API")
        genai.configure(api_key=self.api_key)

        self._read_pdf()
        # Generate system prompt with PDF content
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

        system_prompt = f"""
        Eres Johan, agente virtual de Ingelean especializado en soluciones industriales 4.0.

        TONO: Profesional, empático y claro. Usa emojis y sé conciso.

        PROCESO:
        1. Solicita nombre del cliente
        2. Determina motivo de contacto y tipo de requerimiento
        3. Responde solo con información disponible
        4. Si no tienes info, sugiere agendar llamada

        EMPRESA: Soluciones innovadoras en ingeniería eléctrica, eficiencia energética y automatización industrial.

        {faq_content}

        INFORMACIÓN TÉCNICA:
        {self.pdf_text}
        """
        
        self.generar_system_prompt(system_prompt)

        self.model = genai.GenerativeModel(self.model_name,
                           system_instruction=self.system_prompt)


    def _read_pdf(self):
        file_path = './API/pdf/Brochure-Ingelean.pdf'
        self.pdf_text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        pdf_text += text
        except FileNotFoundError:
            print(f"Error: El archivo no se encontró en la ruta {file_path}")
            return ""
        except Exception as e:
            print(f"Ocurrió un error al leer el PDF: {e}")
            return ""
        return pdf_text

    def generar_system_prompt(self, system_prompt: str):
            self.system_prompt = system_prompt + f"\n\nContenido del documento de la empresa:\n{getattr(self, 'pdf_content', '')}"

    def responder_pregunta(self, pregunta: str):
        respuesta = self.model.generate_content([self.sample_file,pregunta])
        return respuesta.text

    def _parse_contexto(self, contexto: list):
        contexto_gemini: list = []
        for i in contexto:
            contexto_gemini.append({
                "role": "user" if i["role"] == "user" else "model",
                "parts": [i["content"]]
            })
        return contexto_gemini

    def responder_pregunta_con_contexto(self, pregunta: str, contexto: list):
        contexto_gemini = self._parse_contexto(contexto)
        chat = self.model.start_chat(history=contexto_gemini)
        respuesta = chat.send_message(pregunta)
        return respuesta.text