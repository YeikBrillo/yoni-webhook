import os
import datetime
from flask import Flask, request
import requests

# ─── CONFIGURACIÓN ───────────────────────────────────────────────────────────
TOKEN   = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Fechas y ciclos para las lecturas (igual que en reminders.py)
INICIO_LUZ  = datetime.date(2025, 3, 28)
INICIO_AGUA = datetime.date(2025, 2, 12)
CICLO_LUZ   = 31
CICLO_AGUA  = 64

# Estado en memoria (se reinicia al cada deploy)
internet_pagado = False

app = Flask(__name__)

def send_message(text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})

def calcular_proxima(inicio, ciclo):
    hoy = datetime.date.today()
    dias = (hoy - inicio).days
    ciclos = dias // ciclo
    return inicio + datetime.timedelta(days=(ciclos + 1) * ciclo)

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    global internet_pagado
    data = request.get_json(force=True)
    if "message" in data:
        text = data["message"]["text"].strip().lower()
        # /estado
        if text == "/estado":
            luz = calcular_proxima(INICIO_LUZ, CICLO_LUZ).strftime("%d/%m/%Y")
            agua = calcular_proxima(INICIO_AGUA, CICLO_AGUA).strftime("%d/%m/%Y")
            status = "sí" if internet_pagado else "no"
            reply = (
                f"📶 Internet pagado: {status}\n"
                f"💡 Próxima lectura luz: {luz}\n"
                f"💧 Próxima lectura agua: {agua}"
            )
            send_message(reply)
        # /lecturas
        elif text == "/lecturas":
            luz = calcular_proxima(INICIO_LUZ, CICLO_LUZ).strftime("%d/%m/%Y")
            agua = calcular_proxima(INICIO_AGUA, CICLO_AGUA).strftime("%d/%m/%Y")
            send_message(f"💡 Luz: {luz}\n💧 Agua: {agua}")
        # /internet
        elif text == "/internet":
            send_message("📶 El internet se paga el día 20 de cada mes.")
        # /internet_pagado
        elif text == "/internet_pagado":
            internet_pagado = True
            send_message("✅ Internet pagado")
        # /ayuda
        elif text == "/ayuda":
            send_message(
                "Comandos disponibles:\n"
                "/estado\n"
                "/lecturas\n"
                "/internet\n"
                "/internet_pagado\n"
                "/ayuda"
            )
    return "ok", 200

if __name__ == "__main__":
    # Para pruebas locales
    app.run(host="0.0.0.0", port=8080)
