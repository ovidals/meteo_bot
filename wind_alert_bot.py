import os
import requests
from datetime import datetime
from urllib.parse import quote


def send_whatsapp(message: str):
    phone = os.environ["CALLMEBOT_PHONE"]
    apikey = os.environ["CALLMEBOT_APIKEY"]

    url = (
        "https://api.callmebot.com/whatsapp.php"
        f"?phone={phone}&text={quote(message)}&apikey={apikey}"
    )

    print("=== TEST CALLMEBOT ===")
    print("PHONE existe:", bool(phone))
    print("APIKEY existe:", bool(apikey))
    print("URL construida correctamente")

    response = requests.get(url, timeout=30)

    print("Status Code:", response.status_code)
    print("Respuesta API:")
    print(response.text)

    response.raise_for_status()


def main():
    print("Script arrancado")

    message = (
        f"🚀 Test GitHub Actions\n"
        f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Si recibes esto, CallMeBot funciona correctamente."
    )

    send_whatsapp(message)

    print("Script finalizado")


if __name__ == "__main__":
    main()
