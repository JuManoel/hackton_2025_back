import os

class ILLMApi:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.path_info = "./API/pdf/Brochure-Ingelean.pdf"

    def _get_info(self):
        pass

    def generar_system_prompt(self, system_prompt: str):
        pass

    def responder_pregunta(self, pregunta: str):
        pass

    def responder_pregunta_con_contexto(self, pregunta: str, contexto: str):
        pass
