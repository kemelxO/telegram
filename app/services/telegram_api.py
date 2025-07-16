import requests
from django.conf import settings

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=data)
    return response.json()

def delete_telegram_message(chat_id, message_id):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/deleteMessage"
    data = {"chat_id": chat_id, "message_id": message_id}
    return requests.post(url, json=data).json()
