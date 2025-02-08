import sys
import requests
import os  # Добавляем импорт модуля os

SERVER_URL = 'http://localhost:8888'  # Адрес сервера

# Загрузка файла на сервер
def upload_file(filepath):
    if not os.path.exists(filepath):  # Проверяем, существует ли файл
        print(f"Error: File '{filepath}' not found.")
        return
    
    with open(filepath, 'rb') as file:
        files = {'file': file}
        response = requests.post(f'{SERVER_URL}/upload', files=files)
        print(response.text)  # Выводим ответ сервера

# Получение списка файлов
def list_files():
    response = requests.get(f'{SERVER_URL}/files')  # Запрос к маршруту /files
    if response.status_code == 200:
        files = response.json()  # Получаем список файлов из JSON
        print("Files on server:")
        for file in files:
            print(file)
    else:
        print("Error: Could not retrieve file list.")

# Основная логика
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python screwdriver.py <command> [args]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'upload':
        if len(sys.argv) < 3:
            print("Usage: python screwdriver.py upload /path/to/file.mp3")
            sys.exit(1)
        upload_file(sys.argv[2])
    elif command == 'list':
        list_files()
    else:
        print("Unknown command")