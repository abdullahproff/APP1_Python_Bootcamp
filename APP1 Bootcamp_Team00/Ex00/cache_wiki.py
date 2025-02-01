import requests
from bs4 import BeautifulSoup
import json
import logging
import argparse
from urllib.parse import urljoin, unquote

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_links_from_page(url):
    """Извлекает все внутренние ссылки на Википедии из страницы."""
    try:
        response = requests.get(url, timeout=10)  # Добавляем тайм-аут для запроса
        response.raise_for_status()  # Проверяем, что запрос успешен
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/wiki/') and ':' not in href:  # Исключаем ссылки на файлы и специальные страницы
                full_url = urljoin('https://en.wikipedia.org', href)
                links.add(full_url)
        return links
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе страницы {url}: {e}")
        return set()

def build_graph(start_url, max_depth, max_pages=1000):
    """Строит граф ссылок, начиная с заданной страницы."""
    graph = {}
    visited = set()
    queue = [(start_url, 0)]  # Очередь для BFS: (url, текущая глубина)

    try:
        while queue and len(visited) < max_pages:
            current_url, depth = queue.pop(0)
            if current_url in visited:
                continue
            visited.add(current_url)
            logging.info(f"Посещена страница: {current_url} (глубина {depth})")
            graph[current_url] = []

            if depth < max_depth:
                links = get_links_from_page(current_url)
                for link in links:
                    if link not in visited:
                        queue.append((link, depth + 1))
                    graph[current_url].append(link)

    except KeyboardInterrupt:
        logging.info("Программа прервана пользователем. Сохранение текущего графа...")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")

    return graph

def save_graph_to_json(graph, filename='wiki.json'):
    """Сохраняет граф в JSON-файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(graph, f, ensure_ascii=False, indent=4)
        logging.info(f"Граф сохранён в файл {filename}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении графа: {e}")

def main():
    parser = argparse.ArgumentParser(description="Скачивает страницы Википедии и строит граф ссылок.")
    parser.add_argument('-p', '--page', type=str, default='https://en.wikipedia.org/wiki/Harry_Potter',
                        help="Начальная страница для парсинга.")
    parser.add_argument('-d', '--depth', type=int, default=3,
                        help="Максимальная глубина обхода ссылок.")
    args = parser.parse_args()

    logging.info(f"Начало парсинга с страницы: {args.page}")
    graph = build_graph(args.page, args.depth)
    if len(graph) < 20:
        logging.warning("Граф слишком мал. Попробуйте другую начальную страницу.")
    save_graph_to_json(graph)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Программа завершена пользователем.")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")