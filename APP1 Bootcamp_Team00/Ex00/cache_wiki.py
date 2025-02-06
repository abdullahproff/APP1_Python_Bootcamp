import requests
from bs4 import BeautifulSoup
import json
import logging
import argparse
from urllib.parse import urljoin

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_links_from_page(url):
    """Извлекает все внутренние ссылки на Википедии из страницы."""
    try:
        if not url.startswith("https://"):
            url = urljoin("https://en.wikipedia.org/wiki/", url)
        response = requests.get(url, timeout=10)  # Тайм-аут для запроса
        response.raise_for_status()  # Проверяем, что запрос успешен
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Исключаем ссылки на файлы и специальные страницы
            if href.startswith('/wiki/') and ':' not in href:
                full_url = urljoin('https://en.wikipedia.org', href)
                links.add(full_url)
        return links
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе страницы {url}: {e}")
        return set()

def build_graph_dfs(start_url, max_depth, max_pages=1000):
    """Строит граф ссылок, начиная с заданной страницы, используя DFS."""
    graph = {"nodes": [], "edges": []}
    visited = set()
    nodes = set()

    def dfs(current_url, depth):
        """Рекурсивная функция для обхода в глубину."""
        if current_url in visited or len(visited) >= max_pages:
            return
        title_current = current_url.split('/')[-1] # Выделение заголовка из ссылки
        visited.add(current_url)
        nodes.add(title_current)
        logging.info(f"{len(visited)}. Посещена страница: {current_url} (глубина {depth})")

        if depth < max_depth:
            links = get_links_from_page(current_url)
            for link in links:
                if len(nodes) < max_pages and link not in visited:
                    title_link = link.split('/')[-1] # Выделение заголовка из ссылки
                    nodes.add(title_link)
                    edges = {"from": title_current, "to": title_link} # Добавление ребер в граф
                    if edges not in graph["edges"]:
                        graph["edges"].append(edges)
                    dfs(link, depth + 1)  # Рекурсивный вызов для следующего уровня

    dfs(start_url, 0)  # Начинаем обход с начальной страницы и глубины 0
    graph["nodes"] = list(nodes)
    if len(visited) < 20:
        logging.warning("Граф слишком мал. Попробуйте другую начальную страницу.")
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
    """Основная функция для запуска скрипта."""
    parser = argparse.ArgumentParser(description="Скачивает страницы Википедии и строит граф ссылок.")
    parser.add_argument('-p', '--page', type=str, default='https://en.wikipedia.org/wiki/Harry_Potter',
                        help="Начальная страница для парсинга.")
    parser.add_argument('-d', '--depth', type=int, default=3,
                        help="Максимальная глубина обхода ссылок.")
    parser.add_argument('-mp', '--max_pages', type=int, default=1000,
                        help="Максимальное количество ссылок для обработки.")
    args = parser.parse_args()

    logging.info(f"Начало парсинга с страницы: {args.page}")
    graph = build_graph_dfs(args.page, args.depth, args.max_pages)
    save_graph_to_json(graph)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Программа завершена пользователем.")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
