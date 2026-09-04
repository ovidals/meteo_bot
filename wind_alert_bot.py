def main():
    print("Script arrancado")

    print("PHONE existe:", bool(os.environ.get("CALLMEBOT_PHONE")))
    print("APIKEY existe:", bool(os.environ.get("CALLMEBOT_APIKEY")))

    send_whatsapp("🚀 TEST DESDE GITHUB ACTIONS")

    print("Mensaje enviado")
