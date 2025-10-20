import aiosqlite
import asyncio
from typing import Optional

class UserDatabase:
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
    
    async def init_db(self):
        """Инициализация базы данных и создание таблицы пользователей"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    balance INTEGER DEFAULT 0,
                    total_bets INTEGER DEFAULT 0,
                    total_wins INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()
    
    async def get_user(self, user_id: int) -> Optional[dict]:
        """Получить информацию о пользователе"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM users WHERE user_id = ?", 
                (user_id,)
            )
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def create_user(self, user_id: int, username: str = None, first_name: str = None) -> dict:
        """Создать нового пользователя с начальным балансом 1000 ⭐"""
        async with aiosqlite.connect(self.db_path) as db:
            # 🎁 Стартовый бонус: 1000 звёзд для новых игроков!
            initial_balance = 1000
            await db.execute("""
                INSERT INTO users (user_id, username, first_name, balance)
                VALUES (?, ?, ?, ?)
            """, (user_id, username, first_name, initial_balance))
            await db.commit()
            
            # Возвращаем созданного пользователя
            return await self.get_user(user_id)
    
    async def get_or_create_user(self, user_id: int, username: str = None, first_name: str = None) -> dict:
        """Получить пользователя или создать нового"""
        user = await self.get_user(user_id)
        if not user:
            user = await self.create_user(user_id, username, first_name)
        return user
    
    async def get_balance(self, user_id: int) -> int:
        """Получить баланс пользователя"""
        user = await self.get_user(user_id)
        return user['balance'] if user else 0
    
    async def update_balance(self, user_id: int, new_balance: int):
        """Обновить баланс пользователя с защитой от отрицательных значений"""
        # 🛡️ ЗАЩИТА: Баланс не может быть отрицательным!
        if new_balance < 0:
            print(f"⚠️ ПРЕДУПРЕЖДЕНИЕ: Попытка установить отрицательный баланс {new_balance} для пользователя {user_id}")
            new_balance = 0
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE users 
                SET balance = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE user_id = ?
            """, (new_balance, user_id))
            await db.commit()
    
    async def add_balance(self, user_id: int, amount: int) -> int:
        """Добавить/отнять к балансу пользователя"""
        current_balance = await self.get_balance(user_id)
        new_balance = max(0, current_balance + amount)  # Баланс не может быть отрицательным
        await self.update_balance(user_id, new_balance)
        return new_balance
    
    async def record_bet(self, user_id: int, bet_amount: int, win_amount: int):
        """Записать информацию о ставке и выигрыше"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE users 
                SET total_bets = total_bets + ?, 
                    total_wins = total_wins + ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (bet_amount, win_amount, user_id))
            await db.commit()
    
    async def get_user_stats(self, user_id: int) -> dict:
        """Получить статистику пользователя"""
        user = await self.get_user(user_id)
        if not user:
            return None
        
        return {
            'balance': user['balance'],
            'total_bets': user['total_bets'],
            'total_wins': user['total_wins'],
            'profit': user['total_wins'] - user['total_bets'],
            'created_at': user['created_at']
        }
    
    async def get_top_users(self, limit: int = 10) -> list:
        """Получить топ пользователей по балансу"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT user_id, username, first_name, balance, total_wins, total_bets
                FROM users 
                ORDER BY balance DESC 
                LIMIT ?
            """, (limit,))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def reset_user_balance(self, user_id: int, new_balance: int = 0):
        """Сбросить баланс пользователя"""
        await self.update_balance(user_id, new_balance)

# Создаем глобальный экземпляр базы данных
db = UserDatabase()