#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы базы данных
"""

import asyncio
from database import UserDatabase

async def test_database():
    """Тестирование функций базы данных"""
    print("🧪 Тестирование базы данных...")
    
    # Создаем экземпляр базы данных
    db = UserDatabase("test_users.db")
    
    # Инициализируем базу данных
    await db.init_db()
    print("✅ База данных инициализирована")
    
    # Тестируем создание пользователя
    user_id = 123456789
    username = "test_user"
    first_name = "Тестовый Пользователь"
    
    user = await db.get_or_create_user(user_id, username, first_name)
    print(f"✅ Пользователь создан: {user}")
    
    # Тестируем получение баланса
    balance = await db.get_balance(user_id)
    print(f"💰 Баланс пользователя: {balance}")
    
    # Тестируем обновление баланса
    await db.update_balance(user_id, 1500)
    new_balance = await db.get_balance(user_id)
    print(f"💰 Новый баланс: {new_balance}")
    
    # Тестируем добавление к балансу
    final_balance = await db.add_balance(user_id, -200)
    print(f"💰 Баланс после вычета 200: {final_balance}")
    
    # Тестируем запись ставки
    await db.record_bet(user_id, 200, 400)
    print("✅ Ставка записана")
    
    # Тестируем получение статистики
    stats = await db.get_user_stats(user_id)
    print(f"📊 Статистика пользователя: {stats}")
    
    # Создаем еще несколько тестовых пользователей
    for i in range(2, 6):
        test_user_id = 123456789 + i
        await db.get_or_create_user(test_user_id, f"user_{i}", f"User {i}")
        await db.update_balance(test_user_id, 1000 + i * 100)
        await db.record_bet(test_user_id, 100, 50 * i)
    
    # Тестируем топ пользователей
    top_users = await db.get_top_users(5)
    print(f"🏆 Топ пользователей: {top_users}")
    
    # Тестируем сброс баланса
    await db.reset_user_balance(user_id)
    reset_balance = await db.get_balance(user_id)
    print(f"🔄 Баланс после сброса: {reset_balance}")
    
    print("✅ Все тесты пройдены успешно!")
    
    # Удаляем тестовую базу данных
    import os
    if os.path.exists("test_users.db"):
        os.remove("test_users.db")
        print("🗑️ Тестовая база данных удалена")

if __name__ == "__main__":
    asyncio.run(test_database())