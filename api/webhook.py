import os
import datetime
import requests

# ─── CONFIGURACIÓN ───────────────────────────────────────────────────────────
TOKEN = os.getenv("TELEGRAM_TOKEN")
# NOTA: CHAT_ID lo tomamos del propio payload de Telegram

# Fechas y ciclos
INICIO_LUZ, INICIO_AGUA = datetime.date(2025, 3, 28), datetime.date(2025, 2, 12)
CICLO_LUZ, CICLO_AGUA   = 31, 64

def send_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})

def calcular_proxima(inicio, ciclo):
    hoy   = datetime.date.today()
    dias  = (hoy - inicio).days
    ciclos = dias // ciclo
    return inicio + datetime.timedelta(days=(ciclos + 1) * ciclo)

def handler(request):
    # Vercel pasa aquí todos los requests
    if request.method != "POST":
        return {"statusCode": 200, "body": "OK"}

    data = request.json or {}
    msg  = data.get("message", {})
    text = msg.get("text", "").strip().lower()
    chat = msg.get("chat", {})
    chat_id = chat.get("id")

    if not chat_id or not text:
        return {"statusCode": 200, "body": "No message"}

    # Comandos
    if text == "/estado":
        luz  = calcular_proxima(INICIO_LUZ, CICLO_LUZ).strftime("%d/%m/%Y")
        agua = calcular_proxima(INICIO_AGUA, CICLO_AGUA).strftime("%d/%m/%Y")
        status = "sí" if os.getenv("INTERNET_PAGADO","false")=="true" else "no"
        reply = f"📶 Internet pagado: {status}\n💡 Próxima luz: {luz}\n💧 Próxima agua: {agua}"
        send_message(chat_id, reply)

    elif text == "/lecturas":
        luz  = calcular_proxima(INICIO_LUZ, CICLO_LUZ).strftime("%d/%m/%Y")
        agua = calcular_proxima(INICIO_AGUA, CICLO_AGUA).strftime("%d/%m/%Y")
        send_message(chat_id, f"💡 Luz: {luz}\n💧 Agua: {agua}")

    elif text == "/internet":
        send_message(chat_id, "📶 El internet se paga el día 20 de cada mes.")

    elif text == "/internet_pagado":
        # Guardamos en variable de entorno (para demo; en prod usarías DB)
        os.environ["INTERNET_PAGADO"] = "true"
        send_message(chat_id, "✅ Internet pagado")

    elif text == "/ayuda":
        send_message(chat_id,
            "Comandos:\n"
            "/estado\n"
            "/lecturas\n"
            "/internet\n"
            "/internet_pagado\n"
            "/ayuda"
        )

    else:
        send_message(chat_id, "❓ Comando no reconocido. Prueba /ayuda")

    return {"statusCode": 200, "body": "OK"}
