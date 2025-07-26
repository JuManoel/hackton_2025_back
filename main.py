from API.Gemini import Gemini
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

try:
    gemini = Gemini()
    # Contexto rápido con 3 preguntas y respuestas
    contexto = [
        {"role": "user", "content": "¿Qué servicios ofrece Ingelean? me llamo Juan"},
        {"role": "model", "content": "Hola Juan, gracias por entrar en contacto con nosotros.Ingelean ofrece consultoría en ingeniería, desarrollo de software y automatización industrial."},
        {"role": "user", "content": "¿En qué sectores trabaja Ingelean?"},
        {"role": "model", "content": "Trabajamos principalmente en manufactura, energía y tecnología."},
        {"role": "user", "content": "¿Cómo puedo contactar a Ingelean?"},
        {"role": "model", "content": "Puedes contactarnos a través de nuestro sitio web o llamando al +57 300 123 4567."}
    ]
    import time

    start_time = time.time()
    respuesta = gemini.responder_pregunta_con_contexto("Cual es el diferencial de la empresa?", contexto)
    
    first_chunk = True
    for chunk in respuesta:
        if first_chunk:
            end_time = time.time()
            delta_time = end_time - start_time
            print(f"Delta time to first chunk: {delta_time:.4f} seconds")
            first_chunk = False
        print(chunk.text)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
