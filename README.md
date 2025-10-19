# 🎰 Telegram Casino Roulette Bot# 🎰 Telegram Roulette Web App



Telegram-бот с веб-приложением для игры в рулетку. Новый дизайн в белых, голубых и золотых тонах.Игра-рулетка для Telegram Web App с красивым интерфейсом, анимациями и полноценной базой данных для хранения балансов пользователей.



## 🎨 Цветовая палитра## ✨ Особенности



```css- 🎮 Игровая механика рулетки

--bg-1: #ffffff;           /* Белый фон */- ⭐ Система баланса и ставок  

--bg-2: #e6f7ff;           /* Очень светло-голубой */- 🎲 Множители 1X и 10X

--accent-blue: #00aaff;    /* Основной голубой */- 💾 **SQLite база данных для сохранения балансов**

--accent-deep: #0077cc;    /* Глубокий голубой */- 📊 **Статистика игроков и топ-лидеры**

--gold: #ffd700;           /* Золотой */- 🔄 **Персистентное сохранение данных между сессиями**

--text-dark: #01303f;      /* Темно-синий текст */- 📱 Адаптивный дизайн для мобильных

```- 🔗 Интеграция с Telegram Bot API

- 💚 Стильный неоновый интерфейс

## 📁 Структура проекта

## 🚀 Демо

```

тгбот/**Живая версия:** [https://sudoxen.github.io/telegram-roulette-app/](https://sudoxen.github.io/telegram-roulette-app/)

├── index.html                    # Web App для GitHub Pages ⭐

├── casino_bot_improved.py        # Основной бот## 🛠️ Технологии

├── database.py                   # База данных SQLite

├── users.db                      # БД пользователей- HTML5

│- CSS3 (анимации, градиенты)

├── webapp/                       # Web App файлы- JavaScript

│   └── index.html                # Копия для разработки- Telegram Web App API

│

├── archive/                      # Старые версии## 📱 Использование в Telegram боте

│   ├── telegram_bot.py

│   ├── index_improved.html1. Создайте бота через @BotFather

│   └── ...2. Используйте URL: `https://sudoxen.github.io/telegram-roulette-app/`

│3. Настройте Web App в боте

├── docs/                         # Документация

│   ├── README.md## 📂 Структура проекта

│   ├── SETUP_GUIDE.txt

│   ├── GITHUB_PAGES_FIX.md```

│   └── ...├── index.html              # Основной файл Web App

│├── telegram_bot.py         # Python код бота с базой данных

└── tests/                        # Тестовые скрипты├── database.py             # Модуль для работы с SQLite БД

    ├── test_database.py├── requirements.txt        # Зависимости Python (включая aiosqlite)

    ├── test_bot.py├── users.db               # База данных SQLite (создается автоматически)

    └── ...├── test_database.py       # Тестовый скрипт для проверки БД

```├── DATABASE_README.md     # Документация по базе данных

└── README.md              # Этот файл

## 🚀 Быстрый старт```



### 1. Установка зависимостей## 🎯 Новые команды бота



```bash- `/start` - Приветствие и создание аккаунта

pip install -r docs/requirements.txt- `/balance` - Показать текущий баланс

```- `/stats` - Показать личную статистику

- `/top` - Топ-10 игроков по балансу

### 2. Запуск бота- `/reset` - Сбросить баланс до 1000 звезд

- `/webapp` - Открыть игру

```bash- `/help` - Справка по командам

python casino_bot_improved.py

```## 💾 База данных



### 3. Локальная проверка Web AppБот использует SQLite для хранения:

- Балансов пользователей

```bash- Статистики ставок и выигрышей

python archive/start_local_server.py- Информации о пользователях

# Открой http://localhost:8000 в браузере- Истории игр

```

**Все данные сохраняются между перезапусками бота!**

## 🌐 GitHub Pages

## 🚀 Установка и запуск

Web App доступен по адресу:

**https://sudoxen.github.io/telegram-roulette-app/**1. Установить зависимости:

```bash

### Обновление на GitHub Pagespip install -r requirements.txt

```

```bash

git add index.html2. Заменить `BOT_TOKEN` в `telegram_bot.py` на токен от @BotFather

git commit -m "Update web app design"

git push origin master3. Запустить бота:

``````bash

python telegram_bot.py

Изменения появятся через 1-2 минуты.```



## 📱 Telegram BotБаза данных создастся автоматически при первом запуске.



**Бот:** [@wintonnerbot](https://t.me/wintonnerbot)## 🧪 Тестирование



### Команды:Запустить тесты базы данных:

```bash

- `/start` - Начать игруpython test_database.py

- `/play` - Быстрая игра```

- `/balance` - Показать баланс (текущий: 0 ⭐)

- `/stats` - Статистика## 🎯 Реализованные улучшения

- `/top` - Топ игроков

- `/reset` - Сбросить баланс на 0- [x] ✅ База данных пользователей

- `/help` - Справка- [x] ✅ Система статистики

- [x] ✅ Таблица лидеров

## 🎮 Игровая механика- [x] ✅ Персистентное хранение данных

- [ ] Система достижений

- **Начальный баланс:** 0 ⭐- [ ] Больше игровых режимов

- **Минимальная ставка:** 200 ⭐- [ ] Звуковые эффекты

- **Множители:** 1X (200 ⭐), 10X (2000 ⭐ ДЖЕКПОТ)

- **Шанс джекпота:** 10%---



⚠️ **Важно:** Для игры нужно пополнить баланс (минимум 200 ⭐)Создано с ❤️ для Telegram

## 🛠️ Технологии

- **Backend:** Python 3.10+
  - `aiogram 3.2.0` - Telegram Bot API
  - `aiosqlite 0.19.0` - Async SQLite
  
- **Frontend:** HTML5 + CSS3 + Vanilla JS
  - Telegram Web App API
  - CSS Variables для темизации
  - Responsive design

## 📊 База данных

SQLite база с таблицей `users`:

| Поле | Тип | Описание |
|------|-----|----------|
| `user_id` | INTEGER | Telegram ID (PRIMARY KEY) |
| `username` | TEXT | @username |
| `first_name` | TEXT | Имя пользователя |
| `balance` | INTEGER | Баланс в звездах (default: 0) |
| `total_bets` | INTEGER | Общая сумма ставок |
| `total_wins` | INTEGER | Общая сумма выигрышей |
| `created_at` | TIMESTAMP | Дата регистрации |
| `updated_at` | TIMESTAMP | Последнее обновление |

## 🔧 Конфигурация

⚠️ **ВАЖНО:** Токен бота хранится в файле `.env` (не загружается в Git!)

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=ваш_токен_от_BotFather
WEB_APP_URL=https://sudoxen.github.io/telegram-roulette-app/app.html
```

Пример доступен в файле `.env.example`

## 📝 Changelog

### v2.0 - Новый дизайн (19.10.2025)
- ✅ Обновлена цветовая палитра (белый/голубой/золотой)
- ✅ Улучшена структура проекта
- ✅ Исправлена синхронизация баланса
- ✅ Организованы файлы по папкам

### v1.0 - Исходная версия
- Базовая функциональность
- Темная тема (розовый/зеленый)

## 🐛 Известные проблемы

1. **Баланс 0 блокирует игру**
   - Решение: Добавить команду пополнения или изменить начальный баланс
   
2. **GitHub Pages кэширование**
   - Решение: Используется параметр `?v=timestamp` для обхода кэша

## 📖 Дополнительная документация

- [Настройка GitHub Pages](docs/GITHUB_PAGES_FIX.md)
- [Инструкция по установке](docs/SETUP_GUIDE.txt)
- [Исправление синхронизации баланса](docs/BALANCE_ZERO_CHANGES.md)
- [Отчет о тестировании](docs/USER_TESTING_REPORT.md)

## 📄 Лицензия

MIT License - свободное использование

## 👨‍💻 Автор

Created with ❤️ by sudoxen

---

**Последнее обновление:** 19 октября 2025
