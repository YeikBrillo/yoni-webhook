import os
from logic import check_internet, check_meters, check_matches
# Vercel proporciona `request` y espera que devolvamos un dict con statusCode/body

def handler(request):
    if request.method != "POST":
        return {"statusCode": 200, "body": "OK"}

    data = request.json or {}
    msg  = data.get("message", {})
    text = msg.get("text", "").strip().lower()
    chat = msg.get("chat", {})
    chat_id = chat.get("id")

    if not chat_id or not text:
        return {"statusCode": 200, "body": "No message"}

    # Ruteo de comandos
    if text == "/estado":
        # Ejecuta ambos recordatorios, que solo envían mensaje si toca
        check_internet(chat_id)
        check_meters(chat_id)

    elif text == "/lecturas":
        check_meters(chat_id)

    elif text == "/internet":
        check_internet(chat_id)

    elif text == "/malaga":
        check_matches(chat_id)

    elif text == "/ayuda":
        from api.logic import send_message
        send_message(chat_id,
            "Comandos disponibles:\n"
            "/estado     (estado internet y lecturas)\n"
            "/lecturas   (solo fecha lecturas)\n"
            "/internet   (info pago internet)\n"
            "/malaga     (partidos Málaga)\n"
            "/ayuda      (esta ayuda)"
        )

    else:
        from api.logic import send_message
        send_message(chat_id, "❓ Comando no reconocido. Prueba /ayuda")

    return {"statusCode": 200, "body": "OK"}
