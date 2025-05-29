import os
import datetime
import requests
from bs4 import BeautifulSoup

# ─── CONFIGURACIÓN ───────────────────────────────────────────────────────────
INICIO_LUZ  = datetime.date(2025, 3, 28)
INICIO_AGUA = datetime.date(2025, 2, 12)
CICLO_LUZ   = 31
CICLO_AGUA  = 64

def send_message(chat_id: int, text: str):
    """Envía texto a Telegram usando el token configurado."""
    token = os.getenv("TELEGRAM_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})

def check_internet(chat_id: int):
    """Recuerda pagar el internet si hoy es día 20."""
    if datetime.date.today().day == 20:
        send_message(chat_id, "📶 Mamonaa ¡acuérdate de pagar el internet hoy!")

def check_meters(chat_id: int):
    """Recuerda la próxima lectura de luz y agua según ciclos."""
    hoy = datetime.date.today()
    if (hoy - INICIO_LUZ).days % CICLO_LUZ == 0:
        send_message(chat_id,
            f"💡 Illo acuérdate de echarle una fotito al contador de luz (cerca de {hoy.strftime('%d/%m/%Y')})."
        )
    if (hoy - INICIO_AGUA).days % CICLO_AGUA == 0:
        send_message(chat_id,
            f"💧 Illo acuérdate de echarle una fotito al contador de agua (cerca de {hoy.strftime('%d/%m/%Y')})."
        )

def check_matches(chat_id: int):
    """Comprueba si juega el Málaga mañana en La Rosaleda."""
    mañana = datetime.date.today() + datetime.timedelta(days=1)
    resp = requests.get("https://www.malagacf.com/partidos")
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for card in soup.select("div.card-match"):
        fecha_txt = card.select_one(".date-match").text.strip()
        estadio   = card.select_one(".stadium").text.strip()
        try:
            fecha = datetime.datetime.strptime(fecha_txt, "%d/%m/%Y").date()
        except ValueError:
            continue
        if estadio.lower().startswith("la rosaleda") and fecha == mañana:
            send_message(chat_id, 
                "⚽ Novea.. Mañana juega el Málaga en casa. Si no tienes que coger el coxe, no lo muevas!"
            )
            break
