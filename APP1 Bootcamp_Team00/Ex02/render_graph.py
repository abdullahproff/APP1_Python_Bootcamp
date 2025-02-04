import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

# Шаг 1: Чтение данных из JSON-файла
def read_graph_from_file(file_path):
    """
    Чтение графа из JSON-файла.
    Предполагается, что файл содержит список связей в формате:
    {"nodes": ["Page1", "Page2", ...], "edges": [{"from": "Page1", "to": "Page2"}, ...]}
    """
    graph = nx.DiGraph()
    with open(file_path, 'r') as file:
        data = json.load(file)  # Загружаем JSON-данные
        nodes = data.get("nodes", [])
        edges = data.get("edges", [])
        graph.add_nodes_from(nodes)  # Добавляем все узлы сразу
        for edge in edges:
            source = edge.get("from")
            target = edge.get("to")
            if source and target:
                graph.add_edge(source, target)
    return graph

# Шаг 2: Визуализация графа в PNG
def render_graph_png(graph, output_file='wiki_graph.png'):
    """
    Визуализация графа в виде PNG-изображения.
    Размер узла зависит от количества входящих связей.
    """
    plt.figure(figsize=(12, 12))
    pos = nx.circular_layout(graph)  # Используем circular_layout вместо spring_layout
    node_sizes = [graph.in_degree(node) * 100 for node in graph.nodes()]
    nx.draw(graph, pos, with_labels=True, node_size=node_sizes, node_color='skyblue', font_size=10, font_weight='bold')
    plt.savefig(output_file)
    plt.close()

# Шаг 3: Визуализация графа в HTML (интерактивная)
def render_graph_html(graph, output_file='wiki_graph.html'):
    """
    Визуализация графа в виде интерактивной HTML-страницы.
    """
    net = Network(notebook=True, directed=True)
    net.from_nx(graph)
    net.show(output_file)

# Шаг 4: Основная функция
def main():
    # Получение пути к файлу из переменной окружения
    wiki_file = os.getenv('WIKI_FILE')
    if not wiki_file:
        raise ValueError("Переменная окружения WIKI_FILE не установлена.")

    # Чтение графа из файла
    graph = read_graph_from_file(wiki_file)

    # Очистка графа (удаление петель и дубликатов)
    graph.remove_edges_from(nx.selfloop_edges(graph))
    graph = nx.DiGraph(graph)

    # Визуализация графа в PNG
    render_graph_png(graph)

    # Визуализация графа в HTML (опционально)
    render_graph_html(graph)

if __name__ == "__main__":
    main()