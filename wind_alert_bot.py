def main():
    message = (
        f"🚀 Test GitHub Actions + CallMeBot\n"
        f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print(message)
    send_whatsapp(message)
