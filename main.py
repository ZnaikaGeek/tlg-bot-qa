# main.py - Telegram Bot с Q&A

import functions_framework
from firebase_admin import initialize_app, firestore
import requests
import json

# Инициализировать Firebase
initialize_app()
db = firestore.client()

TELEGRAM_BOT_TOKEN = "ВАШ_ТОКЕН_ЗДЕСЬ"  # Получить от @BotFather
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

@functions_framework.http
def telegram_webhook(request):
    """Webhook для Telegram сообщений"""
    
    data = request.get_json()
    
    # Если это сообщение (не другое событие)
    if 'message' not in data:
        return {'ok': True}
    
    message = data['message']
    chat_id = message['chat']['id']
    user_text = message.get('text', '').strip()
    
    # Поиск ответа в Firestore
    docs = db.collection('qa_pairs').where(
        'question', '==', user_text
    ).stream()
    
    answer = "❌ Ответ не найден"
    for doc in docs:
        answer = doc.get('answer')
        break
    
    # Отправить ответ в Telegram
    send_message(chat_id, answer)
    
    return {'ok': True}

def send_message(chat_id, text):
    """Отправить сообщение в Telegram"""
    url = f"{TELEGRAM_API}/sendMessage"
    requests.post(url, json={
        'chat_id': chat_id,
        'text': text
    })

@functions_framework.http
def health_check(request):
    """Проверка здоровья"""
    return {'status': 'ok'}
