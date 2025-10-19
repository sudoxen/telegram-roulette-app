#!/usr/bin/env python3
"""
🔍 ПРОВЕРКА КОНКРЕТНОГО ТОКЕНА
Проверяет токен "8211492486:AAEdPWoquZmjHdDaf0e-lqLrkjn57K8q-gM"
"""

import asyncio
import aiohttp

async def test_specific_token():
    """Тестирование конкретного токена"""
    token = "8211492486:AAEdPWoquZmjHdDaf0e-lqLrkjn57K8q-gM"
    
    print("🔍 ПРОВЕРКА ТОКЕНА БОТА")
    print("=" * 50)
    print(f"🔑 Токен: {token}")
    print(f"📏 Длина: {len(token)} символов")
    
    # Проверка формата
    if ":" in token:
        parts = token.split(":")
        bot_id, bot_hash = parts
        print(f"🤖 Bot ID: {bot_id}")
        print(f"🔑 Hash: {bot_hash}")
        print(f"📐 Hash длина: {len(bot_hash)} символов")
        
        if len(bot_hash) == 35:
            print("✅ Формат токена правильный")
        else:
            print("❌ Неправильная длина хеша")
    
    # Проверка через Telegram API
    print("\n🌐 ПРОВЕРКА ЧЕРЕЗ TELEGRAM API")
    print("-" * 30)
    
    url = f"https://api.telegram.org/bot{token}/getMe"
    print(f"📡 URL: {url}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as response:
                print(f"📊 HTTP статус: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"📋 Ответ: {data}")
                    
                    if data.get('ok'):
                        bot_info = data['result']
                        print("\n✅ ТОКЕН ДЕЙСТВИТЕЛЬНЫЙ!")
                        print(f"🤖 Имя: {bot_info.get('first_name')}")
                        print(f"👤 Username: @{bot_info.get('username')}")
                        print(f"🆔 ID: {bot_info.get('id')}")
                        print(f"🔗 Поддержка inline: {bot_info.get('supports_inline_queries', False)}")
                        return True
                    else:
                        print(f"❌ API ошибка: {data}")
                        return False
                        
                elif response.status == 401:
                    error_data = await response.json()
                    print(f"❌ ТОКЕН НЕДЕЙСТВИТЕЛЕН (401)")
                    print(f"📝 Детали: {error_data}")
                    return False
                    
                else:
                    error_text = await response.text()
                    print(f"❌ HTTP ошибка {response.status}")
                    print(f"📝 Ответ: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"💥 Ошибка соединения: {e}")
        return False

async def test_with_aiogram():
    """Тест с aiogram для проверки конкретной ошибки"""
    print("\n🤖 ТЕСТ С AIOGRAM")
    print("-" * 30)
    
    try:
        from aiogram import Bot
        from aiogram.utils.token import validate_token
        
        token = "8211492486:AAEdPWoquZmjHdDaf0e-lqLrkjn57K8q-gM"
        
        print("🔍 Проверка валидации aiogram...")
        validate_token(token)
        print("✅ Токен прошел валидацию aiogram")
        
        print("🔍 Создание объекта Bot...")
        bot = Bot(token=token)
        print("✅ Объект Bot создан успешно")
        
        print("🔍 Тест getMe через aiogram...")
        me = await bot.get_me()
        print(f"✅ Bot info: {me.first_name} (@{me.username})")
        
        await bot.session.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка aiogram: {e}")
        print(f"🔍 Тип ошибки: {type(e).__name__}")
        return False

async def main():
    print("🎯 ПОЛНАЯ ДИАГНОСТИКА ТОКЕНА")
    print("=" * 50)
    
    # 1. Прямая проверка API
    api_ok = await test_specific_token()
    
    # 2. Проверка aiogram
    aiogram_ok = await test_with_aiogram()
    
    print("\n" + "=" * 50)
    print("📋 ИТОГИ")
    print("=" * 50)
    print(f"🌐 Telegram API: {'✅ OK' if api_ok else '❌ FAIL'}")
    print(f"🤖 aiogram: {'✅ OK' if aiogram_ok else '❌ FAIL'}")
    
    if api_ok and not aiogram_ok:
        print("\n🤔 Токен работает с API, но не с aiogram")
        print("💡 Возможные причины:")
        print("   - Устаревшая версия aiogram")
        print("   - Проблемы с зависимостями")
        print("   - Кодировка токена")
    elif not api_ok:
        print("\n❌ Токен недействителен")
        print("💡 Нужен новый токен от @BotFather")
    else:
        print("\n✅ Все OK! Токен должен работать")

if __name__ == "__main__":
    asyncio.run(main())