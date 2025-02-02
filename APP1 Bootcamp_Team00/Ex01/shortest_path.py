# Импорт необходимых модулей
import os  # Для работы с файловой системой и переменными окружения
import sys  # Для завершения программы в случае ошибок
import argparse  # Для обработки аргументов командной строки
from collections import deque  # Для использования очереди в алгоритме BFS

# Функция для загрузки графа из файла
def load_graph(file_path):
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        print("database not found")  # Если файл не найден, выводим сообщение
        sys.exit(1)  # Завершаем программу с кодом ошибки 1
    
    # Создаем пустой словарь для хранения графа
    graph = {}
    # Открываем файл для чтения
    with open(file_path, 'r') as file:
        # Читаем файл построчно
        for line in file:
            # Удаляем лишние пробелы и разбиваем строку по разделителю ' -> '
            parts = line.strip().split(' -> ')
            # Проверяем, что строка содержит два элемента (начало и конец ребра)
            if len(parts) == 2:
                from_node, to_node = parts  # Извлекаем начальную и конечную вершины
                # Если начальная вершина еще не в графе, добавляем ее
                if from_node not in graph:
                    graph[from_node] = []
                # Добавляем конечную вершину в список соседей начальной вершины
                graph[from_node].append(to_node)
    # Возвращаем построенный граф
    return graph

# Функция для поиска кратчайшего пути с использованием BFS
def find_shortest_path(graph, start, end, non_directed=False):
    # Проверяем, существуют ли начальная и конечная вершины в графе
    if start not in graph or end not in graph:
        return None  # Если нет, возвращаем None
    
    # Создаем очередь для BFS, инициализируем ее начальной вершиной и путем
    queue = deque()
    queue.append((start, [start]))  # Очередь содержит кортежи (текущая вершина, путь до нее)
    
    # Основной цикл BFS
    while queue:
        # Извлекаем текущую вершину и путь до нее из очереди
        current_node, path = queue.popleft()
        
        # Если текущая вершина совпадает с конечной, возвращаем путь
        if current_node == end:
            return path
        
        # Перебираем всех соседей текущей вершины
        for neighbor in graph.get(current_node, []):
            # Если сосед еще не посещен, добавляем его в очередь
            if neighbor not in path:
                queue.append((neighbor, path + [neighbor]))
        
        # Если граф ненаправленный, добавляем обратные ребра
        if non_directed:
            # Перебираем все вершины и их соседей
            for node, neighbors in graph.items():
                # Если текущая вершина является соседом другой вершины и эта вершина еще не посещена
                if current_node in neighbors and node not in path:
                    # Добавляем вершину в очередь
                    queue.append((node, path + [node]))
    
    # Если путь не найден, возвращаем None
    return None

# Основная функция программы
def main():
    # Создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Find the shortest path between two pages in a serialized graph.")
    # Добавляем аргумент --from для указания начальной вершины
    parser.add_argument('--from', dest='start', required=True, help="The starting page.")
    # Добавляем аргумент --to для указания конечной вершины
    parser.add_argument('--to', dest='end', required=True, help="The ending page.")
    # Добавляем аргумент --non-directed для указания, что граф ненаправленный
    parser.add_argument('--non-directed', action='store_true', help="Treat the graph as non-directed.")
    # Добавляем аргумент -v для включения подробного вывода пути
    parser.add_argument('-v', action='store_true', help="Enable verbose logging of the found path.")
    
    # Парсим аргументы командной строки
    args = parser.parse_args()
    
    # Получаем путь к файлу базы данных из переменной окружения WIKI_FILE
    wiki_file = os.getenv('WIKI_FILE')
    # Если переменная окружения не установлена, выводим сообщение и завершаем программу
    if not wiki_file:
        print("WIKI_FILE environment variable not set.")
        sys.exit(1)
    
    # Загружаем граф из файла
    graph = load_graph(wiki_file)
    # Ищем кратчайший путь между начальной и конечной вершинами
    path = find_shortest_path(graph, args.start, args.end, args.non_directed)
    
    # Если путь найден
    if path:
        # Если включен подробный вывод, выводим путь
        if args.v:
            print(" -> ".join(path))
        # Выводим длину пути (количество ребер)
        print(len(path) - 1)
    else:
        # Если путь не найден, выводим сообщение
        print("path not found")

# Точка входа в программу
if __name__ == "__main__":
    main()