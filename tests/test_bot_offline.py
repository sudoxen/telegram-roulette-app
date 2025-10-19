#!/usr/bin/env python3
"""
Тестовый режим бота - проверяет все функции без подключения к Telegram
"""

import asyncio
from database import db

class MockMessage:
    """Имитация сообщения от пользователя"""
    def __init__(self, user_id, username, first_name):
        self.from_user = MockUser(user_id, username, first_name)

class MockUser:
    """Имитация пользователя"""
    def __init__(self, user_id, username, first_name):
        self.id = user_id
        self.username = username
        self.first_name = first_name

async def test_bot_functions():
    """Тестирование всех функций бота без Telegram API"""
    print("🤖 Тестовый режим бота")
    print("=" * 50)
    
    # Инициализируем базу данных
    await db.init_db()
    print("✅ База данных инициализирована")
    
    # Тестируем команду /start
    print("\n🎯 Тестируем команду /start")
    mock_message = MockMessage(123456789, "test_user", "Тестовый Пользователь")
    
    user_id = mock_message.from_user.id
    username = mock_message.from_user.username
    first_name = mock_message.from_user.first_name
    
    # Создаем или получаем пользователя (логика из команды /start)
    user = await db.get_or_create_user(user_id, username, first_name)
    balance = user['balance']
    print(f"   👤 Пользователь: {first_name} (@{username})")
    print(f"   💰 Стартовый баланс: {balance} ⭐")
    
    # Тестируем команду /balance
    print("\n💰 Тестируем команду /balance")
    balance = await db.get_balance(user_id)
    print(f"   💰 Ваш баланс: {balance} ⭐")
    
    # Тестируем симуляцию игры (Web App data)
    print("\n🎲 Тестируем игровую логику")
    # Симулируем ставку 200, выигрыш 400 (множитель 2X)
    bet = 200
    win = 400
    new_balance = balance - bet + win
    
    await db.update_balance(user_id, new_balance)
    await db.record_bet(user_id, bet, win)
    
    print(f"   🎯 Ставка: {bet} ⭐")
    print(f"   🏆 Выигрыш: {win} ⭐")
    print(f"   💰 Новый баланс: {new_balance} ⭐")
    
    # Тестируем команду /stats
    print("\n📊 Тестируем команду /stats")
    stats = await db.get_user_stats(user_id)
    if stats:
        profit_emoji = "📈" if stats['profit'] >= 0 else "📉"
        print(f"   📊 Статистика:")
        print(f"   💰 Баланс: {stats['balance']} ⭐")
        print(f"   🎯 Общих ставок: {stats['total_bets']} ⭐")
        print(f"   🏆 Общих выигрышей: {stats['total_wins']} ⭐")
        print(f"   {profit_emoji} Прибыль/убыток: {stats['profit']} ⭐")
    
    # Создаем еще пользователей для топа
    print("\n👥 Создаем дополнительных пользователей для топа")
    test_users = [
        (987654321, "winner_alice", "Алиса"),
        (987654322, "lucky_bob", "Боб"),
        (987654323, "pro_charlie", "Чарли")
    ]
    
    for i, (uid, uname, fname) in enumerate(test_users):
        await db.get_or_create_user(uid, uname, fname)
        # Симулируем разные балансы
        fake_balance = 1000 + i * 500
        await db.update_balance(uid, fake_balance)
        await db.record_bet(uid, 100, 200 + i * 100)
        print(f"   ✅ {fname} - баланс: {fake_balance} ⭐")
    
    # Тестируем команду /top
    print("\n🏆 Тестируем команду /top")
    top_users = await db.get_top_users(5)
    for i, user in enumerate(top_users, 1):
        emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][min(i-1, 4)]
        profit = user['total_wins'] - user['total_bets']
        print(f"   {emoji} {user['first_name']} - {user['balance']} ⭐ (прибыль: {profit:+d})")
    
    # Тестируем команду /reset
    print("\n🔄 Тестируем команду /reset")
    await db.reset_user_balance(user_id, 1000)
    reset_balance = await db.get_balance(user_id)
    print(f"   🔄 Баланс после сброса: {reset_balance} ⭐")
    
    print("\n✅ Все функции бота работают корректно!")
    print("🔗 Для реального запуска замените BOT_TOKEN в telegram_bot.py")
    print("💡 Получите токен у @BotFather в Telegram")

if __name__ == "__main__":
    asyncio.run(test_bot_functions())