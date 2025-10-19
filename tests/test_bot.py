#!/usr/bin/env python3
"""
🧪 ТЕСТОВАЯ ВЕРСИЯ БОТА С ЛОКАЛЬНЫМ WEB APP
Использует локальный сервер для тестирования синхронизации баланса
"""

import asyncio
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp, BotCommand
from aiogram.filters import Command
from database import db

# 🔑 ТОКЕН ОТ BOTFATHER
BOT_TOKEN = "8211492486:AAEdPWoquZmjHdDaf0e-lqLrkjn57K8q-gM"

# 🧪 ЛОКАЛЬНЫЙ URL для тестирования
LOCAL_WEB_APP_URL = "http://localhost:8000/test_webapp.html"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("test"))
async def test_command(message):
    """Команда /test - тестирование с локальным Web App"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Создаем или получаем пользователя в базе данных
    user = await db.get_or_create_user(user_id, username, first_name)
    balance = user['balance']
    
    # Создаем кнопку с тестовым Web App с передачей баланса
    webapp_url = f"{LOCAL_WEB_APP_URL}?balance={balance}&user_id={user_id}&test=1"
    web_app = WebAppInfo(url=webapp_url)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧪 ТЕСТ Web App", web_app=web_app)],
        [InlineKeyboardButton(text="💰 Баланс в БД", callback_data="balance")]
    ])
    
    await message.answer(
        f"🧪 <b>ТЕСТОВЫЙ РЕЖИМ</b>\n\n"
        f"👤 Пользователь: {first_name}\n"
        f"💰 Баланс в БД: {balance} ⭐\n"
        f"🔗 URL: {webapp_url}\n\n"
        f"📱 Нажмите кнопку для тестирования:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "balance")
async def balance_callback(callback):
    """Показать баланс из БД"""
    user_id = callback.from_user.id
    balance = await db.get_balance(user_id)
    stats = await db.get_user_stats(user_id)
    
    text = (
        f"💰 Баланс в БД: {balance} ⭐\n"
        f"🎯 Ставок: {stats['total_bets']} ⭐\n"
        f"🏆 Выигрышей: {stats['total_wins']} ⭐\n"
        f"📈 Прибыль: {stats['profit']} ⭐"
    )
    
    await callback.answer(text, show_alert=True)

@dp.message(F.web_app_data)
async def web_app_data(message):
    """Обработка данных от тестового Web App"""
    try:
        data = json.loads(message.web_app_data.data)
        user_id = message.from_user.id
        
        if data.get('action') == 'bet_result':
            # Обновляем баланс пользователя
            new_balance = data.get('balance', 0)
            old_balance = await db.get_balance(user_id)
            
            await db.update_balance(user_id, new_balance)
            
            bet = data.get('bet', 0)
            multiplier = data.get('multiplier', 1)
            win = data.get('win', 0)
            
            # Записываем статистику ставки
            await db.record_bet(user_id, bet, win)
            
            # Подробный ответ
            await message.answer(
                f"🎲 <b>Результат игры:</b>\n\n"
                f"💰 Было: {old_balance} ⭐\n"
                f"🎯 Ставка: {bet} ⭐\n"
                f"🎲 Множитель: {multiplier}X\n"
                f"🏆 Выигрыш: {win} ⭐\n"
                f"💰 Стало: {new_balance} ⭐\n"
                f"{'🎉 ДЖЕКПОТ!' if multiplier == 10 else '🎯 Обычная игра'}",
                parse_mode="HTML"
            )
            
    except Exception as e:
        await message.answer(f"❌ Ошибка обработки данных: {e}")

async def main():
    """Запуск тестового бота"""
    print("🧪 ЗАПУСК ТЕСТОВОГО БОТА")
    print("=" * 40)
    
    await db.init_db()
    print("✅ База данных готова")
    
    print(f"🌐 Локальный Web App: {LOCAL_WEB_APP_URL}")
    print("📝 Команды:")
    print("   /test - тестирование Web App")
    print("🚀 Бот запущен...")
    
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Тестовый бот остановлен")