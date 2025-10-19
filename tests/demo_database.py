#!/usr/bin/env python3
"""
Демонстрационный скрипт - показывает как работает база данных в боте
Запустите этот скрипт, чтобы увидеть как создается и работает база данных
"""

import asyncio
from database import db

async def demo():
    """Демонстрация работы базы данных"""
    print("🎰 Демонстрация базы данных казино-бота")
    print("=" * 50)
    
    # Инициализируем базу данных
    await db.init_db()
    print("✅ База данных инициализирована")
    
    # Симулируем регистрацию пользователей
    users_data = [
        (111111111, "alice_player", "Алиса"),
        (222222222, "bob_gambler", "Боб"),
        (333333333, "charlie_lucky", "Чарли"),
        (444444444, "diana_winner", "Диана"),
        (555555555, "eve_casino", "Ева")
    ]
    
    print("\n👥 Регистрируем пользователей...")
    for user_id, username, first_name in users_data:
        user = await db.get_or_create_user(user_id, username, first_name)
        print(f"   ✅ {first_name} (@{username}) - баланс: {user['balance']} ⭐")
    
    # Симулируем игровую активность
    print("\n🎲 Симулируем игровую активность...")
    
    # Алиса выиграла джекпот
    await db.update_balance(111111111, 3000)
    await db.record_bet(111111111, 200, 2000)
    print("   🎉 Алиса выиграла джекпот! +2000 ⭐")
    
    # Боб проиграл немного
    await db.update_balance(222222222, 600)
    await db.record_bet(222222222, 400, 0)
    print("   😔 Боб проиграл 400 ⭐")
    
    # Чарли играл активно
    await db.update_balance(333333333, 1500)
    await db.record_bet(333333333, 200, 400)
    await db.record_bet(333333333, 300, 600)
    print("   🎯 Чарли сделал несколько удачных ставок")
    
    # Диана немного выиграла
    await db.update_balance(444444444, 1200)
    await db.record_bet(444444444, 200, 400)
    print("   💎 Диана выиграла 200 ⭐")
    
    # Ева только начала играть
    await db.record_bet(555555555, 100, 100)
    print("   🆕 Ева сделала первую ставку")
    
    # Показываем топ игроков
    print("\n🏆 Топ-5 игроков по балансу:")
    top_users = await db.get_top_users(5)
    for i, user in enumerate(top_users, 1):
        emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
        profit = user['total_wins'] - user['total_bets']
        profit_text = f"+{profit}" if profit > 0 else str(profit)
        print(f"   {emoji} {user['first_name']} - {user['balance']} ⭐ (прибыль: {profit_text})")
    
    # Показываем детальную статистику Алисы
    print(f"\n📊 Детальная статистика Алисы:")
    stats = await db.get_user_stats(111111111)
    if stats:
        print(f"   💰 Баланс: {stats['balance']} ⭐")
        print(f"   🎯 Всего ставок: {stats['total_bets']} ⭐")
        print(f"   🏆 Всего выигрышей: {stats['total_wins']} ⭐")
        print(f"   📈 Прибыль: {stats['profit']} ⭐")
        print(f"   📅 Играет с: {stats['created_at'][:10]}")
    
    print(f"\n🗄️ База данных сохранена в файл: users.db")
    print("   Данные останутся даже после перезапуска бота!")
    print("\n✅ Демонстрация завершена!")

if __name__ == "__main__":
    asyncio.run(demo())