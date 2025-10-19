#!/usr/bin/env python3
"""
🔍 ДИАГНОСТИКА ТОКЕНА TELEGRAM БОТА
Проверяет правильность токена и определяет причину ошибки
"""

import re
import asyncio
import aiohttp

def validate_token_format(token):
    """Проверка формата токена"""
    print("🔍 АНАЛИЗ ФОРМАТА ТОКЕНА")
    print("-" * 40)
    
    if not token:
        print("❌ Токен пустой!")
        return False
    
    print(f"📝 Токен: {token}")
    print(f"📏 Длина: {len(token)} символов")
    
    # Проверка базового формата
    if ":" not in token:
        print("❌ Токен должен содержать двоеточие (:)")
        return False
    
    parts = token.split(":")
    if len(parts) != 2:
        print("❌ Токен должен содержать ровно одно двоеточие")
        return False
    
    bot_id, bot_hash = parts
    
    # Проверка ID бота
    print(f"🤖 Bot ID: {bot_id}")
    if not bot_id.isdigit():
        print("❌ Bot ID должен содержать только цифры")
        return False
    
    if len(bot_id) < 8 or len(bot_id) > 12:
        print("❌ Bot ID должен быть длиной 8-12 цифр")
        return False
    
    # Проверка хеша
    print(f"🔑 Bot Hash: {bot_hash}")
    if len(bot_hash) != 35:
        print(f"❌ Hash должен быть длиной 35 символов (текущая: {len(bot_hash)})")
        return False
    
    # Проверка символов в хеше
    if not re.match(r'^[A-Za-z0-9_-]+$', bot_hash):
        print("❌ Hash содержит недопустимые символы")
        return False
    
    print("✅ Формат токена корректный")
    return True

async def check_token_with_telegram(token):
    """Проверка токена через Telegram API"""
    print("\n🌐 ПРОВЕРКА ТОКЕНА ЧЕРЕЗ TELEGRAM API")
    print("-" * 40)
    
    url = f"https://api.telegram.org/bot{token}/getMe"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                print(f"📡 Статус ответа: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    if data.get('ok'):
                        bot_info = data.get('result', {})
                        print("✅ Токен действительный!")
                        print(f"🤖 Имя бота: {bot_info.get('first_name')}")
                        print(f"👤 Username: @{bot_info.get('username')}")
                        print(f"🆔 ID: {bot_info.get('id')}")
                        return True
                    else:
                        print(f"❌ Ошибка API: {data.get('description')}")
                        return False
                elif response.status == 401:
                    print("❌ Токен недействителен (401 Unauthorized)")
                    return False
                elif response.status == 404:
                    print("❌ Бот не найден (404 Not Found)")
                    return False
                else:
                    text = await response.text()
                    print(f"❌ Ошибка HTTP {response.status}: {text}")
                    return False
                    
    except asyncio.TimeoutError:
        print("⏰ Таймаут соединения с Telegram API")
        return False
    except Exception as e:
        print(f"💥 Ошибка соединения: {e}")
        return False

def check_common_issues(token):
    """Проверка типичных проблем с токеном"""
    print("\n🔧 ПРОВЕРКА ТИПИЧНЫХ ПРОБЛЕМ")
    print("-" * 40)
    
    issues = []
    
    # Проблемы с пробелами
    if token != token.strip():
        issues.append("Лишние пробелы в начале или конце токена")
    
    # Проблемы с переносами строк
    if '\n' in token or '\r' in token:
        issues.append("Токен содержит переносы строк")
    
    # Проблемы с кавычками
    if token.startswith('"') and token.endswith('"'):
        issues.append("Токен обернут в кавычки (возможно лишние)")
    
    # Проблемы с экранированием
    if '\\' in token:
        issues.append("Токен содержит обратные слеши (экранирование)")
    
    if issues:
        print("⚠️ Найденные проблемы:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        return False
    else:
        print("✅ Типичных проблем не обнаружено")
        return True

async def diagnose_token():
    """Полная диагностика токена"""
    # Читаем токен из файла
    try:
        with open("telegram_bot.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Ищем токен в файле
        import re
        match = re.search(r'BOT_TOKEN\s*=\s*["\']([^"\']+)["\']', content)
        if not match:
            print("❌ Не удалось найти BOT_TOKEN в файле telegram_bot.py")
            return
        
        token = match.group(1)
        
    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}")
        return
    
    print("🔍 ДИАГНОСТИКА ТОКЕНА TELEGRAM БОТА")
    print("=" * 50)
    
    # 1. Проверка формата
    format_ok = validate_token_format(token)
    
    # 2. Проверка типичных проблем
    common_ok = check_common_issues(token)
    
    # 3. Проверка через API (если формат правильный)
    if format_ok:
        api_ok = await check_token_with_telegram(token)
    else:
        api_ok = False
    
    # Итоговый результат
    print("\n" + "=" * 50)
    print("📋 ИТОГОВЫЙ РЕЗУЛЬТАТ")
    print("=" * 50)
    
    if format_ok and common_ok and api_ok:
        print("✅ Токен полностью корректен!")
        print("🤔 Возможные причины ошибки aiogram:")
        print("   - Устаревшая версия aiogram")
        print("   - Проблемы с сетью")
        print("   - Временные проблемы Telegram API")
    elif format_ok and common_ok and not api_ok:
        print("❌ Токен имеет правильный формат, но недействителен")
        print("💡 Решения:")
        print("   1. Проверьте токен у @BotFather")
        print("   2. Создайте нового бота")
        print("   3. Убедитесь, что бот не был удален")
    else:
        print("❌ Проблема с форматом токена")
        print("💡 Решения:")
        print("   1. Получите новый токен у @BotFather")
        print("   2. Скопируйте токен точно как есть")
        print("   3. Проверьте отсутствие лишних символов")

if __name__ == "__main__":
    asyncio.run(diagnose_token())