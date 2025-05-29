import os
import json
from logic import check_internet, check_meters, check_matches, send_message

def handler(request):
    # Solo respondemos a POST
    if request.method != "POST":
        return {"statusCode": 200, "body": "OK"}

    # Leemos el cuerpo crudo y parseamos JSON
    try:
        payload = json.loads(request.body.decode("utf-8") if isinstance(request.body, bytes) else request.body)
    except Exception:
        return {"statusCode": 400, "body": "Invalid JSON"}

    msg = payload.get("message", {})
    text = msg.get("text", "").strip().lower()
    chat = msg.get("chat", {})
    chat_id = chat.get("id")

    if not chat_id or not text:
        return {"statusCode": 200, "body": "No message"}

    # Ruteo de comandos
    if text == "/estado":
        check_internet(chat_id)
        check_meters(chat_id)
    elif text == "/lecturas":
        check_meters(chat_id)
    elif text == "/internet":
        check_internet(chat_id)
    elif text == "/malaga":
        check_matches(chat_id)
    elif text == "/ayuda":
        send_message(chat_id,
            "Comandos disponibles:\n"
            "/estado     (internet y lecturas)\n"
            "/lecturas   (solo lecturas)\n"
            "/internet   (info internet)\n"
            "/malaga     (partidos Málaga)\n"
            "/ayuda      (esta ayuda)"
        )
    else:
        send_message(chat_id, "❓ Comando no reconocido. Prueba /ayuda")

    return {"statusCode": 200, "body": "OK"}
