"""
Тест генерации URL для Web App
"""
import time

# Копируем функцию из casino_bot_improved.py
WEB_APP_URL = 'https://sudoxen.github.io/telegram-roulette-app/app.html'

def get_webapp_url(balance, user_id):
    """Генерирует URL Web App с актуальным балансом и версией"""
    timestamp = int(time.time())
    return f"{WEB_APP_URL}?balance={balance}&user_id={user_id}&v=2&t={timestamp}#balance={balance}"

# Тестируем с твоим user_id
user_id = 1769188948
balance = 200

url = get_webapp_url(balance, user_id)

print("\n" + "="*70)
print("🔗 ТЕСТ ГЕНЕРАЦИИ URL")
print("="*70)
print(f"\n👤 User ID: {user_id}")
print(f"💰 Balance: {balance} ⭐")
print(f"\n🌐 Сгенерированный URL:\n{url}")
print("\n" + "="*70)
print("\n📋 Скопируй этот URL и открой в браузере!")
print("Должен показать баланс 200 ⭐")
print("="*70 + "\n")
