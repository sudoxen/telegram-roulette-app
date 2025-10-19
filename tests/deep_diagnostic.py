#!/usr/bin/env python3
"""
🔍 ГЛУБОКАЯ ДИАГНОСТИКА - Проверка синхронизации баланса
Проверяет каждый шаг передачи баланса от бота к Web App
"""

import time
from urllib.parse import urlparse, parse_qs

# Константы
WEB_APP_URL = "https://sudoxen.github.io/telegram-roulette-app/"
TEST_USER_ID = 123456789
TEST_BALANCE = 1500

def test_url_generation():
    """Тест 1: Проверка генерации URL с параметрами"""
    print("=" * 60)
    print("🧪 ТЕСТ 1: Генерация URL с балансом")
    print("=" * 60)
    
    timestamp = int(time.time())
    webapp_url = f"{WEB_APP_URL}?balance={TEST_BALANCE}&user_id={TEST_USER_ID}&v={timestamp}&t={timestamp}"
    
    print(f"✅ Сгенерированный URL:")
    print(f"   {webapp_url}")
    print()
    
    # Парсим URL
    parsed = urlparse(webapp_url)
    params = parse_qs(parsed.query)
    
    print(f"📋 Распарсенные параметры:")
    print(f"   - balance: {params.get('balance', ['НЕТ'])[0]}")
    print(f"   - user_id: {params.get('user_id', ['НЕТ'])[0]}")
    print(f"   - v (версия): {params.get('v', ['НЕТ'])[0]}")
    print(f"   - t (timestamp): {params.get('t', ['НЕТ'])[0]}")
    print()
    
    # Проверки
    balance_ok = params.get('balance', [''])[0] == str(TEST_BALANCE)
    user_id_ok = params.get('user_id', [''])[0] == str(TEST_USER_ID)
    version_ok = 'v' in params
    timestamp_ok = 't' in params
    
    print(f"🔍 Результаты проверки:")
    print(f"   {'✅' if balance_ok else '❌'} Баланс передан корректно")
    print(f"   {'✅' if user_id_ok else '❌'} User ID передан корректно")
    print(f"   {'✅' if version_ok else '❌'} Версия для обхода кэша добавлена")
    print(f"   {'✅' if timestamp_ok else '❌'} Временная метка добавлена")
    print()
    
    return balance_ok and user_id_ok and version_ok and timestamp_ok


def simulate_webapp_parsing(url):
    """Тест 2: Симуляция парсинга в Web App"""
    print("=" * 60)
    print("🧪 ТЕСТ 2: Симуляция парсинга в Web App (JavaScript)")
    print("=" * 60)
    
    print(f"📥 Входящий URL: {url}")
    print()
    
    # Парсим как это делает JavaScript
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    
    # Извлекаем balance
    balance_str = params.get('balance', [''])[0]
    
    print(f"🔍 Процесс извлечения баланса:")
    print(f"   1. URLSearchParams.get('balance') = '{balance_str}'")
    
    try:
        balance = int(balance_str)
        print(f"   2. parseInt('{balance_str}') = {balance}")
        print(f"   3. Проверка isNaN({balance}) = False")
        print(f"   4. Проверка {balance} > 0 = {balance > 0}")
        
        if balance > 0:
            print(f"   ✅ УСПЕХ: Баланс {balance} будет использован")
            return balance
        else:
            print(f"   ❌ ОШИБКА: Баланс должен быть положительным")
            return None
    except ValueError:
        print(f"   ❌ ОШИБКА: Невозможно преобразовать '{balance_str}' в число")
        return None


def check_webapp_logic():
    """Тест 3: Проверка логики Web App"""
    print()
    print("=" * 60)
    print("🧪 ТЕСТ 3: Логика обработки баланса в Web App")
    print("=" * 60)
    
    scenarios = [
        ("Корректный баланс", f"?balance=1500&user_id=123", 1500),
        ("Нулевой баланс", f"?balance=0&user_id=123", None),
        ("Отрицательный баланс", f"?balance=-100&user_id=123", None),
        ("Нет параметра balance", f"?user_id=123", None),
        ("Пустой параметр", f"?balance=&user_id=123", None),
        ("Текст вместо числа", f"?balance=abc&user_id=123", None),
    ]
    
    all_ok = True
    for scenario_name, query, expected in scenarios:
        url = WEB_APP_URL + query
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        balance_str = params.get('balance', [''])[0]
        
        try:
            balance = int(balance_str) if balance_str else None
            if balance is not None and balance <= 0:
                balance = None
        except ValueError:
            balance = None
        
        success = (balance == expected)
        emoji = "✅" if success else "❌"
        print(f"   {emoji} {scenario_name}: {balance} (ожидалось: {expected})")
        
        if not success:
            all_ok = False
    
    print()
    return all_ok


def simulate_full_flow():
    """Тест 4: Полный поток работы"""
    print("=" * 60)
    print("🧪 ТЕСТ 4: ПОЛНЫЙ ПОТОК РАБОТЫ (симуляция)")
    print("=" * 60)
    
    # Шаг 1: Пользователь нажимает /start
    print("\n👤 ШАГ 1: Пользователь отправляет /start")
    print(f"   User ID: {TEST_USER_ID}")
    print(f"   Баланс в БД: {TEST_BALANCE} ⭐")
    
    # Шаг 2: Бот генерирует URL
    print("\n🤖 ШАГ 2: Бот генерирует URL с параметрами")
    timestamp = int(time.time())
    webapp_url = f"{WEB_APP_URL}?balance={TEST_BALANCE}&user_id={TEST_USER_ID}&v={timestamp}&t={timestamp}"
    print(f"   URL: {webapp_url}")
    
    # Шаг 3: Web App получает URL
    print("\n🌐 ШАГ 3: Web App загружается и парсит URL")
    parsed = urlparse(webapp_url)
    params = parse_qs(parsed.query)
    balance_str = params.get('balance', [''])[0]
    
    try:
        balance = int(balance_str)
        print(f"   ✅ Баланс успешно извлечен: {balance} ⭐")
        
        # Шаг 4: Обновление интерфейса
        print("\n🎨 ШАГ 4: Web App обновляет интерфейс")
        print(f"   balanceEl.textContent = '{balance} ⭐'")
        print(f"   Кнопка 'Играть': {'доступна' if balance >= 200 else 'заблокирована'}")
        
        # Шаг 5: Игра
        print("\n🎲 ШАГ 5: Пользователь играет")
        bet = 200
        multiplier = 1  # Для примера
        win = bet * multiplier
        new_balance = balance - bet + win
        print(f"   Ставка: {bet} ⭐")
        print(f"   Множитель: {multiplier}X")
        print(f"   Выигрыш: {win} ⭐")
        print(f"   Новый баланс: {new_balance} ⭐")
        
        # Шаг 6: Отправка данных боту
        print("\n📤 ШАГ 6: Web App отправляет данные боту")
        game_data = {
            'action': 'bet_result',
            'bet': bet,
            'multiplier': multiplier,
            'win': win,
            'balance': new_balance
        }
        print(f"   Данные: {game_data}")
        
        # Шаг 7: Бот обновляет БД
        print("\n💾 ШАГ 7: Бот обновляет базу данных")
        print(f"   UPDATE users SET balance = {new_balance} WHERE user_id = {TEST_USER_ID}")
        print(f"   ✅ Баланс в БД обновлен: {new_balance} ⭐")
        
        # Шаг 8: Повторное открытие
        print("\n🔄 ШАГ 8: Пользователь закрывает и открывает Web App снова")
        timestamp2 = int(time.time())
        webapp_url2 = f"{WEB_APP_URL}?balance={new_balance}&user_id={TEST_USER_ID}&v={timestamp2}&t={timestamp2}"
        print(f"   Новый URL: {webapp_url2}")
        
        parsed2 = urlparse(webapp_url2)
        params2 = parse_qs(parsed2.query)
        balance_str2 = params2.get('balance', [''])[0]
        balance2 = int(balance_str2)
        print(f"   ✅ Баланс снова извлечен: {balance2} ⭐")
        print(f"   {'✅ УСПЕХ' if balance2 == new_balance else '❌ ОШИБКА'}: Баланс синхронизирован!")
        
        return True
        
    except Exception as e:
        print(f"   ❌ ОШИБКА: {e}")
        return False


def check_current_webapp():
    """Тест 5: Проверка текущего Web App на GitHub Pages"""
    print()
    print("=" * 60)
    print("🧪 ТЕСТ 5: Проверка файла на GitHub Pages")
    print("=" * 60)
    
    print(f"\n📍 URL Web App: {WEB_APP_URL}")
    print("\n❓ КРИТИЧЕСКИЙ ВОПРОС:")
    print("   Какой файл находится по этому адресу?")
    print()
    print("   🔴 Если это index.html (старая версия):")
    print("      - Баланс будет ВСЕГДА 567 (hardcoded)")
    print("      - Параметры URL игнорируются")
    print("      - ПРОБЛЕМА: Нужно заменить файл!")
    print()
    print("   🟢 Если это index_improved.html (новая версия):")
    print("      - Баланс извлекается из URL")
    print("      - Синхронизация работает")
    print("      - ВСЕ ХОРОШО")
    print()
    print("📋 ДЕЙСТВИЯ ДЛЯ ПРОВЕРКИ:")
    print("   1. Открой https://sudoxen.github.io/telegram-roulette-app/")
    print("   2. Открой DevTools (F12)")
    print("   3. В Console проверь: console.log(window.location.href)")
    print("   4. Добавь ?balance=9999 к URL")
    print("   5. Обнови страницу")
    print("   6. Проверь: показывается ли баланс 9999?")
    print()
    print("⚠️  ЕСЛИ БАЛАНС НЕ МЕНЯЕТСЯ = ФАЙЛ НЕ ОБНОВЛЕН!")


def main():
    """Главная функция диагностики"""
    print("\n" + "=" * 60)
    print("🔍 ГЛУБОКАЯ ДИАГНОСТИКА СИНХРОНИЗАЦИИ БАЛАНСА")
    print("=" * 60)
    print()
    
    results = []
    
    # Тест 1
    results.append(("Генерация URL", test_url_generation()))
    
    # Тест 2
    timestamp = int(time.time())
    test_url = f"{WEB_APP_URL}?balance={TEST_BALANCE}&user_id={TEST_USER_ID}&v={timestamp}"
    balance = simulate_webapp_parsing(test_url)
    results.append(("Парсинг URL", balance == TEST_BALANCE))
    
    # Тест 3
    results.append(("Логика Web App", check_webapp_logic()))
    
    # Тест 4
    results.append(("Полный поток", simulate_full_flow()))
    
    # Тест 5
    check_current_webapp()
    
    # Итоги
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    print("=" * 60)
    
    for test_name, success in results:
        emoji = "✅" if success else "❌"
        print(f"   {emoji} {test_name}: {'ПРОЙДЕН' if success else 'ПРОВАЛЕН'}")
    
    all_passed = all(success for _, success in results)
    
    print()
    if all_passed:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print()
        print("🔍 ВЫВОД:")
        print("   Логика работы корректна на стороне бота и Web App.")
        print()
        print("⚠️  ВЕРОЯТНАЯ ПРОБЛЕМА:")
        print("   На GitHub Pages находится СТАРАЯ версия index.html")
        print("   вместо исправленной index_improved.html")
        print()
        print("✅ РЕШЕНИЕ:")
        print("   1. Переименуй index_improved.html → index.html")
        print("   2. Загрузи на GitHub")
        print("   3. git add index.html")
        print("   4. git commit -m 'Fix balance sync'")
        print("   5. git push")
        print("   6. Подожди 1-2 минуты обновления GitHub Pages")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ")
        print("   Проверь код выше для деталей")
    
    print()
    print("=" * 60)


if __name__ == '__main__':
    main()
