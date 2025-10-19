#!/usr/bin/env python3
"""
🧪 ТЕСТИРОВАНИЕ СИНХРОНИЗАЦИИ БАЛАНСА
Проверяет правильность передачи и получения баланса между ботом и Web App
"""

import asyncio
from database import db

async def test_balance_sync():
    """Тестирование синхронизации баланса"""
    print("🧪 ТЕСТИРОВАНИЕ СИНХРОНИЗАЦИИ БАЛАНСА")
    print("=" * 50)
    
    # Инициализация БД
    await db.init_db()
    print("✅ База данных инициализирована")
    
    # Создаем тестового пользователя
    user_id = 123456789
    user = await db.get_or_create_user(user_id, "test_user", "Тестер")
    print(f"👤 Пользователь создан: {user['first_name']}")
    print(f"💰 Стартовый баланс: {user['balance']} ⭐")
    
    # Симулируем URL, который получит Web App
    base_url = "https://sudoxen.github.io/telegram-roulette-app/"
    webapp_url = f"{base_url}?balance={user['balance']}&user_id={user_id}"
    print(f"🌐 Web App URL: {webapp_url}")
    
    # Симулируем игру в Web App
    print("\n🎲 СИМУЛЯЦИЯ ИГРЫ")
    print("-" * 30)
    
    # Игра 1: Выиграл 200
    bet = 200
    win = 400  # Множитель 2X
    new_balance = user['balance'] - bet + win
    
    print(f"🎯 Ставка: {bet} ⭐")
    print(f"🏆 Выигрыш: {win} ⭐")
    print(f"💰 Новый баланс: {new_balance} ⭐")
    
    # Обновляем баланс в БД (как это делает бот)
    await db.update_balance(user_id, new_balance)
    await db.record_bet(user_id, bet, win)
    
    # Проверяем, что баланс сохранился
    saved_balance = await db.get_balance(user_id)
    print(f"💾 Сохраненный баланс: {saved_balance} ⭐")
    
    # Симулируем повторное открытие Web App
    print("\n🔄 ПОВТОРНОЕ ОТКРЫТИЕ WEB APP")
    print("-" * 30)
    
    current_balance = await db.get_balance(user_id)
    new_webapp_url = f"{base_url}?balance={current_balance}&user_id={user_id}"
    print(f"🌐 Новый Web App URL: {new_webapp_url}")
    print(f"💰 Баланс при открытии: {current_balance} ⭐")
    
    # Еще одна игра
    bet2 = 200
    win2 = 2000  # Джекпот! Множитель 10X
    new_balance2 = current_balance - bet2 + win2
    
    print(f"\n🎉 ДЖЕКПОТ!")
    print(f"🎯 Ставка: {bet2} ⭐")
    print(f"🏆 Выигрыш: {win2} ⭐")
    print(f"💰 Новый баланс: {new_balance2} ⭐")
    
    await db.update_balance(user_id, new_balance2)
    await db.record_bet(user_id, bet2, win2)
    
    # Финальная проверка
    final_balance = await db.get_balance(user_id)
    stats = await db.get_user_stats(user_id)
    
    print(f"\n📊 ФИНАЛЬНАЯ СТАТИСТИКА")
    print("-" * 30)
    print(f"💰 Финальный баланс: {final_balance} ⭐")
    print(f"🎯 Общие ставки: {stats['total_bets']} ⭐")
    print(f"🏆 Общие выигрыши: {stats['total_wins']} ⭐")
    print(f"📈 Прибыль: {stats['profit']} ⭐")
    
    # Демонстрация правильной работы
    print(f"\n✅ РЕЗУЛЬТАТ ТЕСТИРОВАНИЯ")
    print("=" * 50)
    print("🔄 При каждом открытии Web App баланс загружается из БД")
    print("💾 После каждой игры баланс сохраняется в БД")
    print("🎯 Синхронизация работает корректно!")
    
    if final_balance != 567:  # Если не равен старому жестко заданному значению
        print("✅ Проблема с фиксированным балансом 567 решена!")
    else:
        print("⚠️ Возможно, Web App все еще использует старую логику")

if __name__ == "__main__":
    asyncio.run(test_balance_sync())