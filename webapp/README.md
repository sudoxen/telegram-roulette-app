# 🎨 Web App - Новый дизайн

Telegram Web App для казино-рулетки в светлой теме.

## Цветовая схема

### Основные цвета

```css
:root {
    --bg-1: #ffffff;           /* Белый фон */
    --bg-2: #e6f7ff;           /* Очень светло-голубой градиент */
    --accent-blue: #00aaff;    /* Основной голубой акцент */
    --accent-deep: #0077cc;    /* Глубокий голубой для теней */
    --gold: #ffd700;           /* Золотой для джекпота */
    --text-dark: #01303f;      /* Темно-синий текст */
}
```

### Где используются

| Элемент | Цвет | Применение |
|---------|------|------------|
| Фон | `linear-gradient(white → light blue)` | Основной фон |
| Баланс | `Золотой градиент` | Бадж с балансом ⭐ |
| Рулетка бордер | `Голубой #00aaff` | Обводка колеса |
| Рулетка секторы | `Светло-голубой ↔ Золотой` | Чередующиеся сектора |
| Кнопка "Играть" | `Голубой → Темно-голубой` | Градиент кнопки |
| Результат | `Золотой` (джекпот) / `Голубой` (обычный) | Текст результата |

## 📐 Структура

```html
<body>
  <!-- Анимированный фон -->
  <div class="background-animation"></div>
  
  <!-- Статус подключения -->
  <div class="connection-status" id="status">🔗 Подключение...</div>
  
  <!-- Баланс -->
  <div class="balance-container" id="balance">0 ⭐</div>
  
  <!-- Результат игры -->
  <div class="result-display" id="result"></div>
  
  <!-- Рулетка -->
  <div class="roulette-container" id="roulette">
    <div class="roulette-pointer"></div>
    <div class="roulette-center">🎰</div>
  </div>
  
  <!-- Кнопка игры -->
  <button class="play-button" id="playBtn">🎲 ИГРАТЬ (200⭐)</button>
  
  <!-- Информация -->
  <div class="bet-info">...</div>
</body>
```

## 🎯 Основные элементы

### 1. Рулетка (220x220px)

- **Секторы:** 20 штук (чередование светло-голубой/золотой)
- **Анимация вращения:** 2.5s cubic-bezier
- **Указатель:** Голубой треугольник сверху
- **Центр:** Белый круг с голубой обводкой

### 2. Баланс (правый верхний угол)

- **Фон:** Градиент от кремового к золотому
- **Тень:** Мягкая золотая тень
- **Текст:** Темно-синий, жирный

### 3. Кнопка "Играть"

- **Состояние активное:** Голубой градиент
- **Hover:** Увеличение 1.03x + усиленная тень
- **Disabled:** Серый фон без тени

### 4. Результат

- **Обычный выигрыш:** Голубой текст/бордер
- **Джекпот 10X:** Золотой текст/бордер + пульсация

## 📱 Адаптивность

```css
@media (max-width: 350px) {
    .roulette-container {
        width: 180px;
        height: 180px;
    }
    
    .balance-container {
        font-size: 16px;
        padding: 8px 16px;
    }
    
    .play-button {
        padding: 15px 30px;
        font-size: 16px;
    }
}
```

## 🔄 Синхронизация баланса

Web App получает баланс из URL параметров:

```javascript
// URL от бота
https://sudoxen.github.io/telegram-roulette-app/?balance=500&user_id=123&v=1729350000

// Парсинг в JS
const urlParams = new URLSearchParams(window.location.search);
const balance = parseInt(urlParams.get('balance')) || 0;
```

### Fallback механизм

1. **Приоритет 1:** URL параметр `?balance=XXX`
2. **Приоритет 2:** localStorage (`casino_balance`)
3. **Приоритет 3:** Дефолтное значение `0`

## 🎮 Игровая логика

```javascript
// Множители (10% шанс джекпота)
const multipliers = [1, 1, 1, 1, 1, 1, 1, 1, 1, 10];

// Случайный выбор
const multiplier = multipliers[Math.floor(Math.random() * 10)];

// Расчет
const bet = 200;
const win = bet * multiplier;
const newBalance = balance - bet + win;

// Отправка боту
tg.sendData(JSON.stringify({
    action: 'bet_result',
    bet: bet,
    multiplier: multiplier,
    win: win,
    balance: newBalance
}));
```

## 🎨 Анимации

### Вращение рулетки

```css
@keyframes spin {
    0% { transform: translate(-50%, -50%) rotate(0deg); }
    100% { transform: translate(-50%, -50%) rotate(1440deg); }
}

.spinning {
    animation: spin 2.5s cubic-bezier(0.23, 1, 0.320, 1);
}
```

### Джекпот эффект

```css
@keyframes jackpot {
    0%, 100% { 
        box-shadow: 0 0 40px rgba(255, 215, 0, 0.8);
        border-color: var(--gold);
    }
    50% { 
        box-shadow: 0 0 80px rgba(255, 215, 0, 1);
        border-color: #ffed4e;
    }
}

.jackpot-effect {
    animation: jackpot 0.5s ease-in-out 6;
}
```

### Пульсация фона

```css
@keyframes pulse {
    0%, 100% { opacity: 0.25; }
    50% { opacity: 0.6; }
}

.background-animation {
    animation: pulse 6s ease-in-out infinite;
}
```

## 🧪 Локальное тестирование

### Вариант 1: Python HTTP сервер

```bash
cd c:\Users\dbobi\Desktop\тгбот
python -m http.server 8000
```

Открой: `http://localhost:8000/index.html?balance=1000`

### Вариант 2: Live Server (VS Code)

1. Установи расширение "Live Server"
2. Правый клик на `index.html` → "Open with Live Server"
3. Добавь `?balance=1000` к URL

### Вариант 3: Прямое открытие

```
file:///c:/Users/dbobi/Desktop/тгбот/index.html?balance=1000
```

⚠️ Telegram Web App API не будет работать локально, но дизайн можно проверить.

## 🔧 Отладка

### DevTools Console

```javascript
// Проверить баланс
console.log('Balance:', balance);

// Принудительно установить баланс
updateBalance(5000);

// Проверить URL параметры
console.log('URL:', window.location.href);
console.log('Params:', Object.fromEntries(new URLSearchParams(location.search)));

// Telegram WebApp доступен?
console.log('tg:', window.Telegram?.WebApp);
```

## 📦 Деплой на GitHub Pages

```bash
# Убедись что index.html в корне репозитория
git add index.html
git commit -m "Update webapp design: white/blue/gold palette"
git push origin master

# Подожди 1-2 минуты
# Проверь: https://sudoxen.github.io/telegram-roulette-app/
```

### Очистка кэша

Если старая версия всё ещё показывается:

1. **Ctrl+Shift+Del** → Очистить кэш
2. **Ctrl+F5** → Жесткая перезагрузка
3. **Режим инкогнито** → Проверка без кэша
4. **Параметр ?v=timestamp** → Автоматический обход (бот делает это)

## 🐛 Решение проблем

### Баланс не обновляется

```javascript
// Проверь в console
console.log('Balance from URL:', new URLSearchParams(location.search).get('balance'));
console.log('Current balance:', balance);
```

### Кнопка заблокирована

Баланс меньше 200 ⭐:

```javascript
// Принудительно разблокировать для теста
updateBalance(1000);
```

### Telegram WebApp не работает

Только в Telegram клиенте! Для локального теста:

```javascript
// Mock для отладки
window.Telegram = {
    WebApp: {
        expand: () => console.log('expand'),
        sendData: (data) => console.log('sendData:', data)
    }
};
```

---

**Версия:** 2.0 (белый/голубой/золотой)  
**Дата:** 19 октября 2025
