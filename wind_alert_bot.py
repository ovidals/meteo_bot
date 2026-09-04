"""
Bot de alertas de viento por WhatsApp — 100% GRATIS
-----------------------------------------------------
- Ubicación: Platja Llarga, Tarragona
- Datos de viento: Open-Meteo (gratis, sin API key), en km/h
- Envío WhatsApp: CallMeBot (gratis, sin caducidad de sesión)
- Ejecución: pensado para GitHub Actions (gratis) con cron

Requisitos:
    pip install requests

Setup CallMeBot (una sola vez):
    1. Guarda el contacto +34 644 71 79 45
    2. Envíale por WhatsApp: "I allow callmebot to send me messages"
    3. Te responde con tu apikey -> guárdala como secret CALLMEBOT_APIKEY

Variables de entorno necesarias:
    CALLMEBOT_PHONE   -> tu número con prefijo, ej: "34600000000"
    CALLMEBOT_APIKEY  -> el apikey que te da CallMeBot
"""

import os
import requests
from datetime import datetime, timezone
from urllib.parse import quote

# ----------------------------
# CONFIGURACIÓN — AJUSTA ESTO
# ----------------------------

# Platja Llarga, Tarragona (no confundir con la Platja Llarga de Roda de Berà,
# que es otra playa distinta con el mismo nombre)
LATITUDE = 41.152
LONGITUDE = 1.271

MIN_WIND_KMH = 20.4            # = 11 nudos — avisa si el viento medio supera esto (km/h)
MIN_GUST_KMH = 37.0            # o si la racha supera esto (km/h)
HOURS_AHEAD = 12               # cuántas horas hacia adelante revisar
ONLY_DAYTIME = True
DAY_START_HOUR = 9
DAY_END_HOUR = 19


def fetch_wind_forecast():
    """Descarga el pronóstico horario de viento desde Open-Meteo (gratis)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "wind_speed_10m,wind_gusts_10m,wind_direction_10m",
        "wind_speed_unit": "kmh",
        "forecast_days": 2,
        "timezone": "auto",
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def find_matching_hours(data):
    times = data["hourly"]["time"]
    speeds = data["hourly"]["wind_speed_10m"]
    gusts = data["hourly"]["wind_gusts_10m"]
    dirs = data["hourly"]["wind_direction_10m"]

    now = datetime.now().astimezone()
    matches = []

    for t_str, speed, gust, wdir in zip(times, speeds, gusts, dirs):
        t = datetime.fromisoformat(t_str)
        if t.tzinfo is None:
            t = t.astimezone()

        hours_from_now = (t - now).total_seconds() / 3600
        if not (0 <= hours_from_now <= HOURS_AHEAD):
            continue

        if ONLY_DAYTIME and not (DAY_START_HOUR <= t.hour <= DAY_END_HOUR):
            continue

        if speed >= MIN_WIND_KMH or gust >= MIN_GUST_KMH:
            matches.append((t, speed, gust, wdir))

    return matches


def build_message(matches):
    lines = ["💨 Alerta de viento:"]
    for t, speed, gust, wdir in matches:
        lines.append(
            f"  {t.strftime('%a %H:%M')} — {speed:.1f} km/h "
            f"(ráfagas {gust:.1f} km/h, dir {wdir:.0f}°)"
        )
    return "\n".join(lines)


def send_whatsapp(message: str):
    phone = os.environ["CALLMEBOT_PHONE"]
    apikey = os.environ["CALLMEBOT_APIKEY"]
    url = (
        "https://api.callmebot.com/whatsapp.php"
        f"?phone={phone}&text={quote(message)}&apikey={apikey}"
    )
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    print("Respuesta CallMeBot:", resp.text)


def main():
    data = fetch_wind_forecast()
    matches = find_matching_hours(data)

    if matches:
        message = build_message(matches)
        print(message)
        send_whatsapp(message)
    else:
        print(f"[{datetime.now(timezone.utc).isoformat()}] Sin condiciones de aviso.")


if __name__ == "__main__":
    main()
