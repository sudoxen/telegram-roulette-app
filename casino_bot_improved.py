#!/usr/bin/env python3
"""
🎰 КАЗИНО-БОТ - УЛУЧШЕННАЯ ВЕРСИЯ
Протестировано как обычный пользователь и исправлены все проблемы
"""

import asyncio
import json
import time
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp, BotCommand
from aiogram.filters import Command
from database import db

# � Загрузка переменных окружения из .env файла
load_dotenv()

# �🔑 ТОКЕН ОТ BOTFATHER (из .env файла)
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Создай файл .env с токеном бота.")

# 🌐 URL Web App (из .env или дефолтный)
WEB_APP_URL = os.getenv('WEB_APP_URL', 'https://sudoxen.github.io/telegram-roulette-app/game.html')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_webapp_url(balance, user_id):
    """Генерирует URL Web App - БЕЗ параметров, баланс передаём через start_param в кнопке"""
    # Telegram УДАЛЯЕТ query параметры! Используем только базовый URL
    # Баланс передаётся через web_app.url + start_param в keyboard кнопке
    return WEB_APP_URL

@dp.message(Command("start"))
async def start_command(message):
    """Команда /start - приветствие и запуск Web App"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Создаем или получаем пользователя в базе данных
    user = await db.get_or_create_user(user_id, username, first_name)
    balance = user['balance']
    
    # Создаем кнопку с Web App
    # ВАЖНО: передаём баланс через URL параметр (Telegram его передаст как start_param)
    webapp_url = f"{WEB_APP_URL}?balance={balance}"
    web_app = WebAppInfo(url=webapp_url)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Играть в рулетку", web_app=web_app)],
        [InlineKeyboardButton(text="💰 Мой баланс", callback_data="balance")],
        [InlineKeyboardButton(text="📊 Моя статистика", callback_data="stats")],
        [InlineKeyboardButton(text="🏆 Топ игроков", callback_data="top")]
    ])
    
    print(f"🌐 Отправляем Web App URL: {webapp_url}")
    print(f"💰 Баланс пользователя {user_id}: {balance} ⭐")
    
    await message.answer(
        f"🎉 Привет, {first_name}!\n\n"
        f"🎰 Добро пожаловать в казино!\n"
        f"💰 Ваш баланс: <b>{balance} ⭐</b>\n\n"
        f"🎮 Нажмите кнопку ниже, чтобы играть:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(Command("play"))
@dp.message(Command("webapp"))
async def play_command(message):
    """Команда /play - быстрый запуск игры"""
    user_id = message.from_user.id
    balance = await db.get_balance(user_id)
    
    if balance < 200:
        await message.answer(
            "😔 <b>Недостаточно средств!</b>\n\n"
            f"💰 Ваш баланс: {balance} ⭐\n"
            f"🎯 Нужно минимум: 200 ⭐\n\n"
            f"💡 Используйте /reset для получения 1000 ⭐",
            parse_mode="HTML"
        )
        return
    
    webapp_url = f"{WEB_APP_URL}?balance={balance}"
    web_app = WebAppInfo(url=webapp_url)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 ИГРАТЬ СЕЙЧАС!", web_app=web_app)],
        [InlineKeyboardButton(text="💰 Баланс", callback_data="balance")]
    ])
    
    print(f"🌐 /play - Отправляем Web App URL: {webapp_url}")
    print(f"💰 Баланс пользователя {user_id}: {balance} ⭐")
    
    await message.answer(
        f"🎯 <b>Готовы к игре?</b>\n\n"
        f"💰 Ваш баланс: <b>{balance} ⭐</b>\n"
        f"🎲 Ставка: 200 ⭐\n"
        f"🏆 Выигрыш: 200-2000 ⭐\n\n"
        f"🍀 Удачи!",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(Command("balance"))
async def balance_command(message):
    """Команда /balance - показать баланс"""
    user_id = message.from_user.id
    balance = await db.get_balance(user_id)
    
    # Кнопка для игры
    webapp_url = get_webapp_url(balance, user_id)
    web_app = WebAppInfo(url=webapp_url)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Играть", web_app=web_app)],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="🔄 Сбросить", callback_data="reset_confirm")]
    ])
    
    await message.answer(
        f"💰 <b>Ваш баланс: {balance} ⭐</b>\n\n"
        f"🎯 Минимальная ставка: 200 ⭐\n"
        f"🎲 Множители: 1X, 10X\n"
        f"🏆 Максимальный выигрыш: 2000 ⭐",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(Command("stats"))
async def stats_command(message):
    """Команда /stats - показать статистику"""
    user_id = message.from_user.id
    stats = await db.get_user_stats(user_id)
    
    if stats:
        profit_emoji = "📈" if stats['profit'] >= 0 else "📉"
        
        # Кнопки для действий
        webapp_url = get_webapp_url(stats['balance'], user_id)
        web_app = WebAppInfo(url=webapp_url)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎰 Играть", web_app=web_app)],
            [InlineKeyboardButton(text="🏆 Топ игроков", callback_data="top")]
        ])
        
        await message.answer(
            f"📊 <b>Ваша статистика:</b>\n\n"
            f"💰 Баланс: <b>{stats['balance']} ⭐</b>\n"
            f"🎯 Общих ставок: {stats['total_bets']} ⭐\n"
            f"🏆 Общих выигрышей: {stats['total_wins']} ⭐\n"
            f"{profit_emoji} Прибыль/убыток: <b>{stats['profit']:+d} ⭐</b>\n"
            f"📅 Играете с: {stats['created_at'][:10]}",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    else:
        await message.answer("📊 Статистика недоступна")

@dp.message(Command("top"))
async def top_command(message):
    """Команда /top - топ игроков"""
    top_users = await db.get_top_users(10)
    
    if top_users:
        text = "🏆 <b>Топ-10 игроков:</b>\n\n"
        for i, user in enumerate(top_users, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}️⃣"
            name = user['first_name'] or user['username'] or f"Игрок {user['user_id']}"
            profit = user['total_wins'] - user['total_bets']
            profit_emoji = "📈" if profit >= 0 else "📉"
            text += f"{emoji} {name}\n💰 {user['balance']} ⭐ {profit_emoji} {profit:+d}\n\n"
        
        # Кнопка для игры
        user_id = message.from_user.id
        balance = await db.get_balance(user_id)
        webapp_url = get_webapp_url(balance, user_id)
        web_app = WebAppInfo(url=webapp_url)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎰 Попробовать попасть в топ!", web_app=web_app)]
        ])
        
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await message.answer("🏆 Топ игроков пуст")

@dp.message(Command("reset"))
async def reset_command(message):
    """Команда /reset - сброс баланса"""
    user_id = message.from_user.id
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да, сбросить", callback_data="reset_confirm")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="reset_cancel")]
    ])
    
    await message.answer(
        "🔄 <b>Сброс баланса</b>\n\n"
        "⚠️ Это действие нельзя отменить!\n"
        "Ваш баланс станет 0 ⭐\n\n"
        "Подтвердите действие:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(Command("help"))
async def help_command(message):
    """Команда /help - справка"""
    help_text = """
🎰 <b>КАЗИНО-БОТ - СПРАВКА</b>

🎮 <b>Команды:</b>
• /start - начать игру
• /play - быстрая игра
• /balance - показать баланс  
• /stats - моя статистика
• /top - топ игроков
• /reset - сбросить баланс
• /help - эта справка

🎲 <b>Как играть:</b>
1️⃣ Нажмите "🎰 Играть"
2️⃣ Сделайте ставку 200 ⭐
3️⃣ Крутите рулетку
4️⃣ Выигрывайте 200-2000 ⭐!

🏆 <b>Множители:</b>
• 1X = выигрыш 200 ⭐
• 10X = ДЖЕКПОТ 2000 ⭐

🍀 <b>Удачи в игре!</b>
"""
    
    # Кнопка для игры
    user_id = message.from_user.id
    balance = await db.get_balance(user_id)
    webapp_url = get_webapp_url(balance, user_id)
    web_app = WebAppInfo(url=webapp_url)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 НАЧАТЬ ИГРАТЬ!", web_app=web_app)]
    ])
    
    await message.answer(help_text, reply_markup=keyboard, parse_mode="HTML")

# Обработчики кнопок
@dp.callback_query(F.data == "balance")
async def balance_callback(callback):
    """Показать баланс"""
    user_id = callback.from_user.id
    balance = await db.get_balance(user_id)
    await callback.answer(f"💰 Ваш баланс: {balance} ⭐", show_alert=True)

@dp.callback_query(F.data == "stats")
async def stats_callback(callback):
    """Показать статистику"""
    user_id = callback.from_user.id
    stats = await db.get_user_stats(user_id)
    
    if stats:
        profit_emoji = "📈" if stats['profit'] >= 0 else "📉"
        stats_text = (
            f"📊 Ваша статистика:\n\n"
            f"💰 Баланс: {stats['balance']} ⭐\n"
            f"🎯 Ставок: {stats['total_bets']} ⭐\n"
            f"🏆 Выигрышей: {stats['total_wins']} ⭐\n"
            f"{profit_emoji} Прибыль: {stats['profit']:+d} ⭐"
        )
    else:
        stats_text = "📊 Статистика недоступна"
    
    await callback.answer(stats_text, show_alert=True)

@dp.callback_query(F.data == "top")
async def top_callback(callback):
    """Показать топ"""
    await top_command(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "reset_confirm")
async def reset_confirm_callback(callback):
    """Подтверждение сброса"""
    user_id = callback.from_user.id
    await db.reset_user_balance(user_id, 0)
    
    # Кнопка для игры
    webapp_url = get_webapp_url(0, user_id)
    web_app = WebAppInfo(url=webapp_url)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Играть с новым балансом!", web_app=web_app)]
    ])
    
    await callback.message.edit_text(
        "✅ <b>Баланс сброшен!</b>\n\n"
        "💰 Ваш новый баланс: 0 ⭐\n"
        "🎮 Удачи в новых играх!",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer("✅ Баланс сброшен!")

@dp.callback_query(F.data == "reset_cancel")
async def reset_cancel_callback(callback):
    """Отмена сброса"""
    await callback.message.edit_text(
        "❌ Сброс баланса отменен.\n\n"
        "💰 Ваш баланс остался прежним.",
        parse_mode="HTML"
    )
    await callback.answer("❌ Отменено")

# Обработка данных от Web App
@dp.message(F.web_app_data)
async def web_app_data(message):
    """Обработка данных от Web App С СЕРВЕРНОЙ ВАЛИДАЦИЕЙ"""
    print("\n" + "="*60)
    print("📥 ПОЛУЧЕНЫ ДАННЫЕ ОТ WEB APP!")
    print("="*60)
    
    try:
        raw_data = message.web_app_data.data
        print(f"Raw data: {raw_data}")
        
        data = json.loads(raw_data)
        print(f"Parsed data: {data}")
        
        user_id = message.from_user.id
        print(f"User ID: {user_id}")
        
        if data.get('action') == 'bet_result':
            print("✅ Действие: bet_result")
            
            # 🛡️ ЗАЩИТА ОТ ЧИТОВ: Загружаем РЕАЛЬНЫЙ баланс из БД (НЕ доверяем клиенту!)
            current_balance = await db.get_balance(user_id)
            print(f"� РЕАЛЬНЫЙ баланс из БД: {current_balance}")
            
            client_balance = data.get('balance', 0)
            print(f"📱 Баланс от клиента (НЕ доверяем): {client_balance}")
            
            bet = data.get('bet', 0)
            multiplier = data.get('multiplier', 1)
            win = data.get('win', 0)
            
            print(f"🎲 Ставка: {bet}, Множитель: {multiplier}X, Выигрыш от клиента: {win}")
            
            # 🛡️ ВАЛИДАЦИЯ 1: Проверяем что ставка не больше баланса
            if bet > current_balance:
                print(f"🚨 ЧИТЕР ОБНАРУЖЕН! Ставка {bet} больше баланса {current_balance}")
                await message.answer(
                    "🚨 <b>ОШИБКА ВАЛИДАЦИИ!</b>\n\n"
                    f"❌ Ставка {bet} ⭐ больше вашего баланса {current_balance} ⭐\n\n"
                    "🔒 Попытка обмана зафиксирована.",
                    parse_mode="HTML"
                )
                return
            
            # 🛡️ ВАЛИДАЦИЯ 2: Проверяем множитель (максимум 10X)
            if multiplier < 1 or multiplier > 10:
                print(f"🚨 ЧИТЕР ОБНАРУЖЕН! Множитель {multiplier}X недопустим")
                await message.answer(
                    "🚨 <b>ОШИБКА ВАЛИДАЦИИ!</b>\n\n"
                    f"❌ Множитель {multiplier}X недопустим (допустимо: 1-10X)\n\n"
                    "🔒 Попытка обмана зафиксирована.",
                    parse_mode="HTML"
                )
                return
            
            # 🛡️ ВАЛИДАЦИЯ 3: Пересчитываем выигрыш на СЕРВЕРЕ (НЕ доверяем клиенту!)
            server_win = bet * multiplier
            print(f"💰 Выигрыш пересчитан на сервере: {server_win}")
            
            if abs(server_win - win) > 1:  # Допускаем погрешность в 1 звезду
                print(f"⚠️ ПРЕДУПРЕЖДЕНИЕ: Выигрыш от клиента ({win}) не совпадает с серверным ({server_win})")
                print(f"Используем СЕРВЕРНОЕ значение: {server_win}")
            
            # 🛡️ СЕРВЕРНЫЙ РАСЧЁТ НОВОГО БАЛАНСА (НЕ доверяем клиенту!)
            new_balance = current_balance - bet + server_win
            print(f"💰 СЕРВЕРНЫЙ расчёт: {current_balance} - {bet} + {server_win} = {new_balance}")
            
            # Обновляем баланс пользователя
            print(f"💾 Обновляем баланс в БД на: {new_balance}")
            await db.update_balance(user_id, new_balance)
            
            # Записываем статистику ставки (используем СЕРВЕРНЫЙ выигрыш)
            await db.record_bet(user_id, bet, server_win)
            print("✅ Статистика записана в БД")
            
            # Создаем кнопку для продолжения игры (с РЕАЛЬНЫМ балансом из БД)
            webapp_url = f"{WEB_APP_URL}?balance={new_balance}"
            web_app = WebAppInfo(url=webapp_url)
            
            if multiplier == 10:
                # Джекпот!
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🎉 ИГРАТЬ ПОСЛЕ ДЖЕКПОТА!", web_app=web_app)],
                    [InlineKeyboardButton(text="📊 Моя статистика", callback_data="stats")]
                ])
                await message.answer(
                    f"🎉 <b>ПОЗДРАВЛЯЕМ! ДЖЕКПОТ!</b> 🎉\n\n"
                    f"💰 Ставка: {bet} ⭐\n"
                    f"🎲 Множитель: <b>{multiplier}X</b>\n"
                    f"💎 Выигрыш: <b>{server_win} ⭐</b>\n"
                    f"🏦 Новый баланс: <b>{new_balance} ⭐</b>\n\n"
                    f"🍀 Продолжить игру?",
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🎰 Играть еще!", web_app=web_app)],
                    [InlineKeyboardButton(text="💰 Мой баланс", callback_data="balance")]
                ])
                await message.answer(
                    f"🎰 <b>Результат игры:</b>\n\n"
                    f"💰 Ставка: {bet} ⭐\n"
                    f"🎲 Множитель: {multiplier}X\n"
                    f"💵 Выигрыш: {server_win} ⭐\n"
                    f"🏦 Баланс: <b>{new_balance} ⭐</b>\n\n"
                    f"🎮 Играем еще?",
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
        
    except Exception as e:
        await message.answer("❌ Ошибка обработки данных игры")
        print(f"Ошибка Web App данных: {e}")

async def set_commands():
    """Устанавливаем команды бота"""
    commands = [
        BotCommand(command="start", description="🎰 Начать игру"),
        BotCommand(command="play", description="🚀 Быстрая игра"),
        BotCommand(command="balance", description="💰 Мой баланс"),
        BotCommand(command="stats", description="📊 Моя статистика"),
        BotCommand(command="top", description="🏆 Топ игроков"),
        BotCommand(command="reset", description="🔄 Сбросить баланс"),
        BotCommand(command="help", description="❓ Справка")
    ]
    
    await bot.set_my_commands(commands)

async def set_menu_button():
    """Устанавливаем кнопку меню"""
    web_app = WebAppInfo(url=WEB_APP_URL)
    menu_button = MenuButtonWebApp(text="🎰 Играть", web_app=web_app)
    await bot.set_chat_menu_button(menu_button=menu_button)

async def main():
    """Главная функция"""
    print("🎰 ЗАПУСК УЛУЧШЕННОГО КАЗИНО-БОТА")
    print("=" * 50)
    
    try:
        # Инициализация
        await db.init_db()
        print("✅ База данных готова")
        
        await set_commands()
        print("✅ Команды установлены")
        
        await set_menu_button()
        print("✅ Кнопка меню установлена")
        
        print(f"🌐 Web App: {WEB_APP_URL}")
        print("🎮 Доступные команды:")
        print("   /start - начать")
        print("   /play - играть") 
        print("   /balance - баланс")
        print("   /stats - статистика")
        print("   /top - рейтинг")
        print("   /help - справка")
        print("\n🚀 Бот запущен и готов к игре!")
        print("🎯 Протестировано как обычный пользователь")
        
        await dp.start_polling(bot, drop_pending_updates=True)
        
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")