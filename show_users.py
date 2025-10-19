import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Получаем всех пользователей с правильными колонками
users = cursor.execute('''
    SELECT user_id, username, first_name, balance, total_bets, total_wins, created_at, updated_at 
    FROM users 
    ORDER BY created_at
''').fetchall()

print(f'\n🎰 ВСЕГО ПОЛЬЗОВАТЕЛЕЙ БОТА: {len(users)}\n')
print('='*100)

for user in users:
    user_id, username, first_name, balance, total_bets, total_wins, created_at, updated_at = user
    print(f'\n👤 Пользователь:')
    print(f'   ID: {user_id}')
    print(f'   Username: @{username if username else "не указан"}')
    print(f'   Имя: {first_name}')
    print(f'   💰 Баланс: {balance} ⭐')
    print(f'   🎲 Всего ставок: {total_bets}')
    print(f'   🏆 Всего выигрышей: {total_wins}')
    print(f'   📅 Зарегистрирован: {created_at}')
    print(f'   🔄 Последнее обновление: {updated_at}')
    print('-'*100)

conn.close()
