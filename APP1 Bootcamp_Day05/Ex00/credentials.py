from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import json

# WSGI-приложение для обработки HTTP-запросов
def application(environ, start_response):
    """
    WSGI-приложение, обрабатывающее запросы и возвращающее JSON-ответ с "credentials" для указанного вида.
    """
    # Словарь соответствий видов и их "credentials"
    species_dict = {
        "Cyberman": "John Lumic",
        "Dalek": "Davros",
        "Judoon": "Shadow Proclamation Convention 15 Enforcer",
        "Human": "Leonardo da Vinci",
        "Ood": "Klineman Halpen",
        "Silence": "Tasha Lem",
        "Slitheen": "Coca-Cola salesman",
        "Sontaran": "General Staal",
        "Time Lord": "Rassilon",
        "Weeping Angel": "The Division Representative",
        "Zygon": "Broton"
    }
    
    # Получение параметров запроса из URL
    query = parse_qs(environ.get('QUERY_STRING', ''))
    # Извлекаем параметр species (вид), если он есть, иначе None
    species = query.get("species", [None])[0]
    
    # Определяем, есть ли вид в нашем словаре
    if species and species in species_dict:
        response_body = json.dumps({"credentials": species_dict[species]})
        status = "200 OK"  # Если вид найден, возвращаем статус 200
    else:
        response_body = json.dumps({"credentials": "Unknown"})
        status = "404 Not Found"  # Если вид не найден, возвращаем статус 404
    
    # Заголовки ответа, указываем, что это JSON
    headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    
    # Отправляем статус и заголовки
    start_response(status, headers)
    # Возвращаем тело ответа в виде байтов
    return [response_body.encode('utf-8')]

# Запуск сервера при прямом выполнении скрипта
if __name__ == "__main__":
    # Создаем сервер, слушающий порт 8888
    with make_server('', 8888, application) as server:
        print("Serving on port 8888...")
        # Запускаем сервер в бесконечном цикле ожидания запросов
        server.serve_forever()