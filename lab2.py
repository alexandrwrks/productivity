import random
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx

class CreateGraph:
    def __init__(self):
        pass

    def create_simple_graph(self, n):
        """Создание простого графа."""
        matrix = [[0] * n for _ in range(n)]
        for i in range(n - 1):
            matrix[i][i + 1] = 1
            matrix[i + 1][i] = 1
        return matrix

    def create_full_graph(self, n):
        """Создание полного графа."""
        matrix = [[1] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0
        return matrix

    def create_graph_with_loops(self, n):
        """Создание графа с петлями."""
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    matrix[i][i] = random.choice([0, 1, 1, 1])
                else:
                    matrix[i][j] = random.randint(0, 1)
                    matrix[j][i] = matrix[i][j]
        return matrix

    def create_multi_graph(self, n):
        """Создание мультиграфа."""
        graph = nx.MultiGraph()
        graph.add_nodes_from(range(n))

        for i in range(n):
            for j in range(i + 1, n):
                num_edges = random.randint(0, 2)
                for _ in range(num_edges):
                    graph.add_edge(i, j)
        return graph

    def convert_incidence_matrix(self, matrix):
        """Функция для конвертации матрицы смежности в матрицу инцидентности."""
        n = len(matrix)
        edges = []

        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] == 1:
                    edges.append((i, j))

        edge_count = len(edges)
        if edge_count == 0:
            return [[]]

        inc_matrix = [[0] * edge_count for _ in range(n)]

        for e, (v1, v2) in enumerate(edges):
            inc_matrix[v1][e] = 1
            inc_matrix[v2][e] = 1

        return inc_matrix

    def draw_graph(self, matrix, title='Граф'):
        """Функция для отрисовки графа."""
        n = len(matrix)
        graph = nx.Graph()

        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] == 1:
                    graph.add_edge(i, j)

        plt.figure(figsize=(12, 8))

        pos = nx.spring_layout(graph, k=3, iterations=50)

        nx.draw_networkx_edges(graph, pos, edge_color='#555555', width=2, alpha=0.7)
        nx.draw_networkx_nodes(graph, pos, node_color='#87CEEB', node_size=800, edgecolors='darkblue', linewidths=2, alpha=0.9,)

        labels = {i: i + 1 for i in range(n)}
        nx.draw_networkx_labels(graph, pos, labels, font_size=14, font_weight='bold', font_color='black')

        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

        return graph

    def draw_multi_graph(self, graph: nx.Graph, title='Мультиграф'):
        """Отрисовка мультиграфа."""
        plt.figure(figsize=(12, 8))

        pos = nx.spring_layout(graph)
        edges = graph.edges()

        if edges:
            nx.draw_networkx_edges(
                graph,
                pos,
                edge_color='#555555',
                width=2,
                connectionstyle='arc3,rad=0.1',
                alpha=0.7,
            )

        nx.draw_networkx_nodes(
            graph,
            pos,
            node_color='lightgreen',
            node_size=800,
            edgecolors='darkgreen',
            linewidths=2,
            alpha=0.9,
        )

        labels = {i: i + 1 for i in graph.nodes()}
        nx.draw_networkx_labels(graph, pos, labels, font_size=14, font_weight='bold')

        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()


def print_matrix(matrix, title='Матрица'):
    print(f"\n{title}:")
    for row in matrix:
        formatted = []
        for value in row:
            if value is None:
                formatted.append('∞')
            else:
                formatted.append(str(value))
        print(' '.join(formatted))


def multiply_matrices(matrix_a, matrix_b):
    """Умножение двух квадратных матриц одинакового размера."""
    n = len(matrix_a)
    if n == 0 or n != len(matrix_b):
        raise ValueError('Матрицы должны быть квадратными и одного размера')

    for row in matrix_a:
        if len(row) != n:
            raise ValueError('Первая матрица не является квадратной')
    for row in matrix_b:
        if len(row) != n:
            raise ValueError('Вторая матрица не является квадратной')

    result = [[0] * n for _ in range(n)]

    for i in range(n):
        for k in range(n):
            if matrix_a[i][k] == 0:
                continue
            a_ik = matrix_a[i][k]
            for j in range(n):
                if matrix_b[k][j] != 0:
                    result[i][j] += a_ik * matrix_b[k][j]

    return result


def matrix_power(matrix, power):
    """Возведение квадратной матрицы в целую неотрицательную степень."""
    if power < 0:
        raise ValueError('Степень не может быть отрицательной')

    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError('Матрица должна быть квадратной')

    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = [row[:] for row in matrix]
    p = power

    while p > 0:
        if p % 2 == 1:
            result = multiply_matrices(result, base)
        base = multiply_matrices(base, base)
        p //= 2

    return result


def adjacency_to_neighbors(adjacency):
    """Преобразует матрицу смежности в список соседей (игнорируя петли)."""
    n = len(adjacency)
    if any(len(row) != n for row in adjacency):
        raise ValueError('Матрица смежности должна быть квадратной')

    neighbors = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and adjacency[i][j] > 0:
                neighbors[i].append(j)
    return neighbors


def build_metric_matrix(adjacency):
    """
    Строит матрицу метрик (кратчайших расстояний) по матрице смежности.
    Алгоритм: BFS от каждой вершины.
    Недостижимые пары вершин хранятся как None.
    """
    n = len(adjacency)
    if n == 0:
        return []

    neighbors = adjacency_to_neighbors(adjacency)
    metrics = [[None] * n for _ in range(n)]

    for start in range(n):
        metrics[start][start] = 0
        queue = deque([start])
        visited = [False] * n
        visited[start] = True

        while queue:
            vertex = queue.popleft()
            for nxt in neighbors[vertex]:
                if not visited[nxt]:
                    visited[nxt] = True
                    metrics[start][nxt] = metrics[start][vertex] + 1
                    queue.append(nxt)

    return metrics


def find_graph_characteristics(metric_matrix):
    """
    По матрице метрик находит:
    - эксцентриситеты вершин
    - радиус
    - диаметр
    - центральные вершины
    - периферийные вершины

    Если в строке матрицы метрик есть None (недостижимая вершина),
    эксцентриситет такой вершины считается None.
    """
    n = len(metric_matrix)
    if any(len(row) != n for row in metric_matrix):
        raise ValueError('Матрица метрик должна быть квадратной')

    eccentricities = []
    for row in metric_matrix:
        if any(value is None for value in row):
            eccentricities.append(None)
        else:
            eccentricities.append(max(row))

    finite_eccentricities = [e for e in eccentricities if e is not None]

    radius = min(finite_eccentricities) if finite_eccentricities else None
    diameter = max(finite_eccentricities) if finite_eccentricities else None

    central_vertices = [i + 1 for i, e in enumerate(eccentricities) if e == radius and e is not None]
    peripheral_vertices = [i + 1 for i, e in enumerate(eccentricities) if e == diameter and e is not None]

    return {
        'eccentricities': eccentricities,
        'radius': radius,
        'diameter': diameter,
        'central_vertices': central_vertices,
        'peripheral_vertices': peripheral_vertices,
    }


def print_characteristics(characteristics):
    def format_value(value):
        return '∞' if value is None else str(value)

    ecc_str = [format_value(e) for e in characteristics['eccentricities']]
    print('\nЭксцентриситеты вершин:', ecc_str)
    print('Радиус графа:', format_value(characteristics['radius']))
    print('Диаметр графа:', format_value(characteristics['diameter']))
    print('Центральные вершины:', characteristics['central_vertices'])
    print('Периферийные вершины:', characteristics['peripheral_vertices'])


def analyze_graph(matrix):
    print_matrix(matrix, 'Матрица смежности')
    metric_matrix = build_metric_matrix(matrix)
    print_matrix(metric_matrix, 'Матрица метрик')
    characteristics = find_graph_characteristics(metric_matrix)
    print_characteristics(characteristics)


def main():
    graph_creator = CreateGraph()

    while True:
        print('\n' + '=' * 40)
        print('ГЕНЕРАТОР ГРАФОВ')
        print('=' * 40)
        print('1. Простой граф')
        print('2. Полный граф')
        print('3. Граф с петлями')
        print('4. Мультиграф')
        print('5. Выход')

        try:
            choice = int(input('Выберите действие: '))
            if choice not in [1, 2, 3, 4, 5]:
                print('Ошибка! Введите число от 1 до 5')
                continue
        except ValueError:
            print('Ошибка! Введите число от 1 до 5')
            continue

        if choice == 5:
            print('Конец работы!')
            break

        try:
            n = int(input('Введите количество вершин (положительное целое число): '))
            if n <= 0:
                print('Количество вершин должно быть положительным числом!')
                continue
        except ValueError:
            print('Ошибка! Введите целое положительное число')
            continue

        if choice == 1:
            matrix = graph_creator.create_simple_graph(n)

            inc_matrix = graph_creator.convert_incidence_matrix(matrix)
            if inc_matrix != [[]]:
                print_matrix(inc_matrix, 'Матрица инцидентности')

            analyze_graph(matrix)
            graph_creator.draw_graph(matrix, f'Простой граф ({n} вершин)')

        elif choice == 2:
            matrix = graph_creator.create_full_graph(n)
            print(f'Количество рёбер: {n * (n - 1) // 2}')

            inc_matrix = graph_creator.convert_incidence_matrix(matrix)
            if inc_matrix != [[]]:
                print_matrix(inc_matrix, 'Матрица инцидентности')

            analyze_graph(matrix)
            graph_creator.draw_graph(matrix, f'Полный граф ({n} вершин)')

        elif choice == 3:
            matrix = graph_creator.create_graph_with_loops(n)
            print('\nГраф с петлями создан')

            inc_matrix = graph_creator.convert_incidence_matrix(matrix)
            if inc_matrix != [[]]:
                print_matrix(inc_matrix, 'Матрица инцидентности (петли не отображаются)')

            analyze_graph(matrix)

            graph = nx.Graph()
            for i in range(n):
                for j in range(i, n):
                    if matrix[i][j] == 1:
                        graph.add_edge(i, j)

            plt.figure(figsize=(12, 8))
            pos = nx.circular_layout(graph)
            nx.draw_networkx_edges(graph, pos, edge_color='gray', width=2, alpha=0.7)
            nx.draw_networkx_nodes(
                graph,
                pos,
                node_color='#87CEEB',
                node_size=800,
                edgecolors='darkblue',
                linewidths=2,
                alpha=0.9,
            )

            for node in graph.nodes():
                if graph.has_edge(node, node):
                    x, y = pos[node]
                    circle = plt.Circle((x, y - 0.2), 0.2, fill=False, edgecolor='gray', linewidth=2)
                    plt.gca().add_patch(circle)

            labels = {i: i + 1 for i in range(n)}
            nx.draw_networkx_labels(graph, pos, labels, font_size=14, font_weight='bold')

            plt.title(f'Граф с петлями ({n} вершин)', fontsize=16, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
            plt.show()

        elif choice == 4:
            graph = graph_creator.create_multi_graph(n)
            print('\nМультиграф создан!')
            print(f'Вершины: {graph.number_of_nodes()}')
            print(f'Рёбра: {graph.number_of_edges()}')

            adj_matrix = [[0] * n for _ in range(n)]
            for u, v in graph.edges():
                adj_matrix[u][v] += 1
                if u != v:
                    adj_matrix[v][u] += 1

            print_matrix(adj_matrix, 'Матрица смежности (числа = количество рёбер)')

            edges = list(graph.edges())
            if edges:
                inc_matrix = [[0] * len(edges) for _ in range(n)]
                for e, (u, v) in enumerate(edges):
                    inc_matrix[u][e] += 1
                    if u != v:
                        inc_matrix[v][e] += 1
                print_matrix(inc_matrix, 'Матрица инцидентности')

            analyze_graph(adj_matrix)
            graph_creator.draw_multi_graph(graph, f'Мультиграф ({n} вершин)')


if __name__ == '__main__':
    main()