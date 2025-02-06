import json
import os
import argparse
from collections import deque

def load_graph():
    """Загружает граф из JSON-файла, путь к которому указан в переменной WIKI_FILE."""
    wiki_file = os.getenv("WIKI_FILE")  # Читаем путь из переменной окружения

    if not wiki_file or not os.path.exists(wiki_file):
        print("database not found")
        exit(1)

    with open(wiki_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    graph = {node: [] for node in data["nodes"]}
    for edge in data["edges"]:
        graph[edge["from"]].append(edge["to"])

    return graph

def find_shortest_path(graph, start, target, non_directed=False):
    """Находит кратчайший путь с помощью BFS (поиск в ширину)."""
    if start not in graph or target not in graph:
        return None  # Если узлов нет в графе

    queue = deque([(start, [start])])  # Очередь вида (текущий узел, путь до него)
    visited = set()  # Посещённые узлы

    while queue:
        node, path = queue.popleft()

        if node == target:
            return path  # Если дошли до цели — возвращаем путь

        if node in visited:
            continue

        visited.add(node)

        neighbors = graph[node]
        if non_directed:  # Если граф неориентированный, добавляем обратные связи
            for n, links in graph.items():
                if node in links:
                    neighbors.append(n)

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None  # Если пути нет

def main():
    """Парсит аргументы командной строки, загружает граф и ищет кратчайший путь."""
    parser = argparse.ArgumentParser(description="Find the shortest path between two Wikipedia pages.")
    parser.add_argument("--from", dest="start", required=True, help="Start page")
    parser.add_argument("--to", dest="target", required=True, help="Target page")
    parser.add_argument("--non-directed", action="store_true", help="Use bidirectional edges")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show path")

    args = parser.parse_args()
    graph = load_graph()

    path = find_shortest_path(graph, args.start, args.target, args.non_directed)

    if path:
        if args.verbose:
            print(" -> ".join(path))  # Выводим путь, если включен -v
        print(len(path) - 1)  # Выводим длину пути
    else:
        print("path not found")

if __name__ == "__main__":
    main()