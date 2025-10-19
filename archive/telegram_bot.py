import asyncio
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp, BotCommand
from aiogram.filters import Command
from database import db

# 🔑 ТОКЕН ОТ BOTFATHER
BOT_TOKEN = "8211492486:AAEdPWoquZmjHdDaf0e-lqLrkjn57K8q-gM"

# 🌐 URL вашего Web App на GitHub Pages
WEB_APP_URL = "https://sudoxen.github.io/telegram-roulette-app/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message):
    """Команда /start - приветствие и запуск Web App"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Создаем или получаем пользователя в базе данных
    user = await db.get_or_create_user(user_id, username, first_name)
    balance = user['balance']
    
    # Создаем кнопку с Web App с передачей баланса
    webapp_url = f"{WEB_APP_URL}?balance={balance}&user_id={user_id}"
    web_app = WebAppInfo(url=webapp_url)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Играть в рулетку", web_app=web_app)],
        [InlineKeyboardButton(text="💰 Баланс", callback_data="balance")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")]
    ])
    
    await message.answer(
        f"🎉 Привет, {first_name}!\n\n"
        f"Добро пожаловать в казино-бот! 🎰\n"
        f"У вас {balance} ⭐ для игры\n\n"
        f"🎮 Нажмите кнопку ниже, чтобы открыть рулетку:",
        reply_markup=keyboard
    )

@dp.message(Command("webapp"))
async def webapp_command(message):
    """Команда /webapp - быстрый запуск Web App"""
    user_id = message.from_user.id
    balance = await db.get_balance(user_id)
    
    webapp_url = f"{WEB_APP_URL}?balance={balance}&user_id={user_id}"
    web_app = WebAppInfo(url=webapp_url)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Запустить рулетку", web_app=web_app)]
    ])
    
    await message.answer(
        "🎯 Запуск казино-приложения:",
        reply_markup=keyboard
    )

@dp.message(Command("balance"))
async def balance_command(message):
    """Команда /balance - показать баланс"""
    user_id = message.from_user.id
    balance = await db.get_balance(user_id)
    
    await message.answer(
        f"💰 Ваш баланс: {balance} ⭐\n\n"
        f"💡 Минимальная ставка: 200 ⭐\n"
        f"🎲 Множители: 1X, 10X"
    )

@dp.message(Command("help"))
async def help_command(message):
    """Команда /help - справка"""
    help_text = """
🎰 <b>Как играть в рулетку:</b>

1️⃣ Нажмите кнопку "🎰 Играть"
2️⃣ Сделайте ставку 200 ⭐
3️⃣ Крутите рулетку и ждите результат
4️⃣ Выигрывайте с множителями 1X или 10X!

💰 <b>Команды:</b>
/balance - показать баланс
/stats - показать статистику
/top - топ игроков
/webapp - играть в рулетку
/reset - сбросить баланс (0 ⭐)
/help - эта справка

🍀 Удачи в игре!
"""
    
    await message.answer(help_text, parse_mode="HTML")

@dp.message(Command("stats"))
async def stats_command(message):
    """Команда /stats - показать статистику"""
    user_id = message.from_user.id
    stats = await db.get_user_stats(user_id)
    
    if stats:
        profit_emoji = "📈" if stats['profit'] >= 0 else "📉"
        await message.answer(
            f"📊 <b>Ваша статистика:</b>\n\n"
            f"💰 Баланс: {stats['balance']} ⭐\n"
            f"🎯 Общих ставок: {stats['total_bets']} ⭐\n"
            f"🏆 Общих выигрышей: {stats['total_wins']} ⭐\n"
            f"{profit_emoji} Прибыль/убыток: {stats['profit']} ⭐\n"
            f"📅 В игре с: {stats['created_at'][:10]}",
            parse_mode="HTML"
        )
    else:
        await message.answer("📊 Статистика недоступна")

@dp.message(Command("top"))
async def top_command(message):
    """Команда /top - топ игроков"""
    top_users = await db.get_top_users(10)
    
    if top_users:
        text = "🏆 <b>Топ-10 игроков по балансу:</b>\n\n"
        for i, user in enumerate(top_users, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}️⃣"
            name = user['first_name'] or user['username'] or f"User {user['user_id']}"
            profit = user['total_wins'] - user['total_bets']
            profit_emoji = "📈" if profit >= 0 else "📉"
            text += f"{emoji} {name}\n💰 {user['balance']} ⭐ {profit_emoji} {profit:+d}\n\n"
        
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer("🏆 Топ игроков пуст")

@dp.message(Command("reset"))
async def reset_command(message):
    """Команда /reset - сбросить баланс"""
    user_id = message.from_user.id
    await db.reset_user_balance(user_id, 0)
    
    await message.answer(
        "🔄 <b>Баланс сброшен!</b>\n\n"
        "💰 Ваш новый баланс: 0 ⭐\n"
        "🎮 Удачи в новых играх!",
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "balance")
async def balance_callback(callback):
    """Обработчик кнопки баланса"""
    user_id = callback.from_user.id
    balance = await db.get_balance(user_id)
    
    await callback.answer(f"💰 Ваш баланс: {balance} ⭐", show_alert=True)

@dp.callback_query(F.data == "stats")
async def stats_callback(callback):
    """Обработчик кнопки статистики"""
    user_id = callback.from_user.id
    stats = await db.get_user_stats(user_id)
    
    if stats:
        profit_emoji = "📈" if stats['profit'] >= 0 else "📉"
        stats_text = (
            f"📊 Ваша статистика:\n\n"
            f"💰 Баланс: {stats['balance']} ⭐\n"
            f"🎯 Общих ставок: {stats['total_bets']} ⭐\n"
            f"🏆 Общих выигрышей: {stats['total_wins']} ⭐\n"
            f"{profit_emoji} Прибыль/убыток: {stats['profit']} ⭐\n"
            f"📅 В игре с: {stats['created_at'][:10]}"
        )
    else:
        stats_text = "📊 Статистика недоступна"
    
    await callback.answer(stats_text, show_alert=True)

# 📨 Обработка данных от Web App
@dp.message(F.web_app_data)
async def web_app_data(message):
    """Обработка данных от Web App"""
    try:
        # Парсим данные от Web App
        data = json.loads(message.web_app_data.data)
        user_id = message.from_user.id
        
        if data.get('action') == 'get_balance':
            # Запрос баланса от Web App
            current_balance = await db.get_balance(user_id)
            await message.answer(
                f"💰 Ваш текущий баланс: {current_balance} ⭐\n"
                f"🔄 Если баланс в Web App неправильный, закройте и откройте игру заново."
            )
        
        elif data.get('action') == 'bet_result':
            # Обновляем баланс пользователя
            new_balance = data.get('balance', 0)
            await db.update_balance(user_id, new_balance)
            
            bet = data.get('bet', 0)
            multiplier = data.get('multiplier', 1)
            win = data.get('win', 0)
            
            # Записываем статистику ставки
            await db.record_bet(user_id, bet, win)
            
            if multiplier == 10:
                # Джекпот!
                await message.answer(
                    f"🎉 ПОЗДРАВЛЯЕМ! ДЖЕКПОТ! 🎉\n\n"
                    f"💰 Ставка: {bet} ⭐\n"
                    f"🎲 Множитель: {multiplier}X\n"
                    f"💎 Выигрыш: {win} ⭐\n"
                    f"🏦 Новый баланс: {new_balance} ⭐"
                )
            else:
                await message.answer(
                    f"🎰 Результат игры:\n\n"
                    f"💰 Ставка: {bet} ⭐\n"
                    f"🎲 Множитель: {multiplier}X\n"
                    f"💵 Выигрыш: {win} ⭐\n"
                    f"🏦 Баланс: {new_balance} ⭐"
                )
        
    except Exception as e:
        await message.answer("❌ Ошибка обработки данных игры")
        print(f"Ошибка Web App данных: {e}")

async def set_commands():
    """Устанавливаем команды бота"""
    commands = [
        BotCommand(command="start", description="🎰 Начать игру"),
        BotCommand(command="webapp", description="🚀 Открыть рулетку"),
        BotCommand(command="balance", description="💰 Показать баланс"),
        BotCommand(command="stats", description="📊 Статистика"),
        BotCommand(command="top", description="🏆 Топ игроков"),
        BotCommand(command="reset", description="🔄 Сбросить баланс"),
        BotCommand(command="help", description="❓ Помощь")
    ]
    
    await bot.set_my_commands(commands)

async def set_menu_button():
    """Устанавливаем кнопку меню для Web App"""
    web_app = WebAppInfo(url=WEB_APP_URL)
    menu_button = MenuButtonWebApp(text="🎰 Рулетка", web_app=web_app)
    await bot.set_chat_menu_button(menu_button=menu_button)

async def main():
    """Главная функция запуска бота"""
    print("🚀 Запуск казино-бота...")
    
    # Инициализируем базу данных
    await db.init_db()
    print("✅ База данных инициализирована!")
    
    # Устанавливаем команды и кнопку меню
    await set_commands()
    await set_menu_button()
    
    print("✅ Бот настроен и запущен!")
    print(f"🌐 Web App URL: {WEB_APP_URL}")
    print("💡 Не забудьте заменить BOT_TOKEN на ваш токен!")
    print("💾 Данные пользователей сохраняются в users.db")
    
    # Запускаем бота
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен")