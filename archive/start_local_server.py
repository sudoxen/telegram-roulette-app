#!/usr/bin/env python3
"""
🌐 ЛОКАЛЬНЫЙ СЕРВЕР ДЛЯ ТЕСТИРОВАНИЯ WEB APP
Запускает локальный сервер для тестирования Web App
"""

import http.server
import socketserver
import os
import webbrowser
from threading import Thread
import time

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Отключаем кэширование
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def start_server():
    """Запуск локального сервера"""
    PORT = 8000
    
    # Меняем рабочую директорию
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🌐 Сервер запущен на http://localhost:{PORT}")
        print(f"📱 Тестовый Web App: http://localhost:{PORT}/test_webapp.html")
        print("🔗 Для остановки нажмите Ctrl+C")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")

if __name__ == "__main__":
    print("🚀 ЗАПУСК ЛОКАЛЬНОГО СЕРВЕРА")
    print("=" * 40)
    start_server()