import os
import requests


def send_telegram_message(chat_id, text):
    """Отправляет сообщение в Telegram через прокси."""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Публичный HTTPS прокси
    proxies = {
        'https': 'https://159.203.61.220:3128',
    }

    payload = {
        'chat_id': chat_id,
        'text': text,
    }
    try:
        response = requests.post(url, data=payload, proxies=proxies, timeout=10)
        response.raise_for_status()
        print(f"[TELEGRAM] Sent to {chat_id}: {text}")
        return True
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")
        return False
