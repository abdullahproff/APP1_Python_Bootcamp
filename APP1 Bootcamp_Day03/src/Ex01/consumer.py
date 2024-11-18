# Импортируем необходимые библиотеки: 
# redis для подключения к Redis, 
# json для работы с JSON-форматом, 
# argparse для обработки аргументов командной строки 
# logging для ведения логов
import redis
import json
import argparse
import logging

# Настроим logging для отображения информации в консоли с уровня INFO
logging.basicConfig(level=logging.INFO)

# Подключаемся к Redis серверу (по умолчанию localhost:6379, db=0)
r = redis.Redis(host='localhost', port=6379, db=0)

# Создаем объект pubsub для подписки на канал
p = r.pubsub()

# Подписываемся на канал 'transactions', чтобы получать сообщения о транзакциях
p.subscribe('transactions')

# Функция для обработки полученных сообщений
def process_transaction(message, bad_accounts):
    # Декодируем JSON-сообщение из байтов в Python-объект
    data = json.loads(message['data'])
    
    # Извлекаем номера аккаунтов отправителя и получателя, а также сумму
    from_account = data['metadata']['from']
    to_account = data['metadata']['to']
    amount = data['amount']
    
    # Проверяем, если получатель в списке плохих аккаунтов и сумма положительная, меняем местами отправителя и получателя
    if to_account in bad_accounts and amount > 0:
        data['metadata']['from'], data['metadata']['to'] = to_account, from_account
        # Логируем изменение транзакции
        logging.info(f"Modified transaction: {json.dumps(data)}")
    
    # Возвращаем обработанное сообщение
    return data

# Главная функция, которая принимает список плохих аккаунтов и слушает канал Redis
def main(bad_accounts):
    # Прослушиваем сообщения в канале
    for message in p.listen():
        # Проверяем, что тип сообщения - это фактические данные (не информация о канале)
        if message['type'] == 'message':
            # Обрабатываем транзакцию и выводим результат
            transaction = process_transaction(message, bad_accounts)
            # Выводим транзакцию в консоль в формате JSON
            print(json.dumps(transaction))

# Основная точка входа программы
if __name__ == "__main__":
    # Настроим парсер командной строки для получения списка плохих аккаунтов
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--evil-accounts', type=str, required=True, help='Comma separated list of bad guy accounts')
    args = parser.parse_args()
    
    # Преобразуем список плохих аккаунтов из строки в список целых чисел
    bad_accounts = [int(account) for account in args.evil_accounts.split(',')]
    
    # Запускаем основную функцию
    main(bad_accounts)

# Поскольку producer.py генерирует случайные номера аккаунтов 
# вероятность того, что producer выдаст номера, 
# которые будут переданы на consumer.py низкая либо требует долгого ожидания 
# поэтому рекомендую передать сообщение напрямую в поток Redis, 
# например, в одном окне терминала запускается команда: redis-cli
# затем сообщение с нужными данными, которые будут переданы в consumer.py
# PUBLISH transactions '{"metadata": {"from": 1111111111, "to": 2222222222}, "amount": 5000}'
# во втором окне запускаем скрипт python3 consumer.py -e 1111111111,2222222222
# и в выводе получаем: INFO:root:Modified transaction: {"metadata": {"from": 2222222222, "to": 1111111111}, "amount": 5000}
# {"metadata": {"from": 2222222222, "to": 1111111111}, "amount": 5000}
# что подтверждает правильность работы скриптов.