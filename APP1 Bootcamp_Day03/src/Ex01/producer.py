# Импортируем необходимые библиотеки: redis для подключения к Redis, 
# json для работы с JSON-форматом, 
# random для генерации случайных чисел, 
# logging для ведения логов 
# time для пауз между транзакциями
import redis
import json
import random
import logging
import time

# Настроим logging для отображения информации в консоли с уровня INFO
logging.basicConfig(level=logging.INFO)

# Подключаемся к Redis серверу (по умолчанию localhost:6379, db=0)
r = redis.Redis(host='localhost', port=6379, db=0)

# Функция для генерации случайной транзакции
def generate_transaction():
    # Генерируем случайный 10-значный номер аккаунта для отправителя
    from_account = random.randint(1000000000, 9999999999)
    # Генерируем случайный 10-значный номер аккаунта для получателя
    to_account = random.randint(1000000000, 9999999999)
    # Генерируем случайную сумму для транзакции
    amount = random.randint(1, 10000)  # Положительное число для суммы
    # Возвращаем сгенерированное сообщение в виде словаря
    return {
        "metadata": {
            "from": from_account,
            "to": to_account
        },
        "amount": amount
    }

# Главная функция, которая генерирует и отправляет сообщения в Redis
def main():
    while True:
        # Генерируем транзакцию
        transaction = generate_transaction()
        # Преобразуем транзакцию в формат JSON
        message = json.dumps(transaction)
        # Отправляем сообщение в канал 'transactions'
        r.publish('transactions', message)
        # Логируем опубликованное сообщение
        logging.info(f"Published message: {message}")
        # Задержка в 1 секунду между публикациями
        time.sleep(1)

# Основная точка входа программы
if __name__ == "__main__":
    # Запускаем основную функцию
    main()
