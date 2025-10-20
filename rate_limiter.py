"""
🛡️ ЗАЩИТА ОТ СПАМА (RATE LIMITING)
Ограничивает частоту запросов от пользователей
"""

import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=5, time_window=60):
        """
        Инициализация rate limiter
        
        Args:
            max_requests: Максимум запросов в окне
            time_window: Временное окно в секундах
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.user_requests = defaultdict(list)  # {user_id: [timestamp1, timestamp2, ...]}
    
    def is_allowed(self, user_id: int) -> bool:
        """
        Проверяет, разрешён ли запрос от пользователя
        
        Args:
            user_id: ID пользователя
            
        Returns:
            True если запрос разрешён, False если превышен лимит
        """
        current_time = time.time()
        
        # Удаляем старые запросы за пределами временного окна
        self.user_requests[user_id] = [
            timestamp for timestamp in self.user_requests[user_id]
            if current_time - timestamp < self.time_window
        ]
        
        # Проверяем лимит
        if len(self.user_requests[user_id]) >= self.max_requests:
            return False
        
        # Добавляем текущий запрос
        self.user_requests[user_id].append(current_time)
        return True
    
    def get_remaining_time(self, user_id: int) -> int:
        """
        Возвращает время до разблокировки в секундах
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Секунды до разблокировки
        """
        if user_id not in self.user_requests or not self.user_requests[user_id]:
            return 0
        
        oldest_request = min(self.user_requests[user_id])
        current_time = time.time()
        remaining = self.time_window - (current_time - oldest_request)
        
        return max(0, int(remaining))

# Глобальный инстанс rate limiter
# 5 игр в минуту = максимум
game_rate_limiter = RateLimiter(max_requests=5, time_window=60)

# 10 команд в минуту
command_rate_limiter = RateLimiter(max_requests=10, time_window=60)
