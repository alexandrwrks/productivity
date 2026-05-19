import random
import heapq
import matplotlib.pyplot as plt
import networkx as nx


class CreateGraph:
    def __init__(self):
        pass

    def create_simple_graph(self, n):
        # Создает случайный простой связный граф на n вершинах
        matrix = [[0] * n for _ in range(n)]

        for v in range(1, n):
            u = random.randint(0, v - 1)
            matrix[u][v] = 1
            matrix[v][u] = 1

        return matrix

    def create_full_graph(self, n):
        # Создает полный граф на n вершинах
        matrix = [[1] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0
        return matrix

    def create_graph_with_loops(self, n):
        # Создает случайный неориентированный граф с возможными петлями
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
        # Создает случайный мультиграф с 0-2 параллельными ребрами
        graph = nx.MultiGraph()
        graph.add_nodes_from(range(n))

        for i in range(n):
            for j in range(i + 1, n):
                num_edges = random.randint(0, 2)
                for _ in range(num_edges):
                    graph.add_edge(i, j)
        return graph

    def convert_incidence_matrix(self, matrix):
        # Преобразует матрицу смежности в матрицу инцидентности
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
        # Отрисовывает граф по матрице смежности
        n = len(matrix)
        graph = nx.Graph()

        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] == 1:
                    graph.add_edge(i, j)

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(graph, k=3, iterations=50)

        nx.draw_networkx_edges(graph, pos, edge_color='#555555', width=2, alpha=0.7)
        nx.draw_networkx_nodes(
            graph,
            pos,
            node_color='#87CEEB',
            node_size=800,
            edgecolors='darkblue',
            linewidths=2,
            alpha=0.9,
        )

        labels = {i: i + 1 for i in range(n)}
        nx.draw_networkx_labels(graph, pos, labels, font_size=14, font_weight='bold', font_color='black')

        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

        return graph

    def draw_multi_graph(self, graph: nx.Graph, title='Мультиграф'):
        # Отрисовывает мультиграф
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
    # Печатаем матрицу в консоль
    print(f"\n{title}:")
    for row in matrix:
        formatted = []
        for value in row:
            if value is None:
                formatted.append('∞')
            else:
                formatted.append(str(value))
        print(' '.join(formatted))


def print_metric_matrix(metric_matrix):
    # Печатаем матрицу метрик
    print_matrix(metric_matrix, 'Матрица метрик')


def multiply_matrices(matrix_a, matrix_b):
    # Умножение двух квадратных матриц
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
    # Возведение квадратной матрицы в целую неотрицательную степень
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


def build_metric_matrix(adjacency):
    # Строим матрицу кратчайших расстояний по матрице смежности
    # Ищем расстояния через последовательный просмотр степеней матрицы
    n = len(adjacency)
    if n == 0:
        return []
    if any(len(row) != n for row in adjacency):
        raise ValueError('Матрица смежности должна быть квадратной')

    metrics = [[None] * n for _ in range(n)]
    for i in range(n):
        metrics[i][i] = 0

    # Булева матрица смежности (петли не влияют на расстояния между разными вершинами).
    adjacency_bool = [
        [1 if i != j and adjacency[i][j] > 0 else 0 for j in range(n)]
        for i in range(n)
    ]

    current_power = [row[:] for row in adjacency_bool]
    

    for distance in range(1, n):
        change = False
        for i in range(n):
            for j in range(n):
                if i != j and metrics[i][j] is None and current_power[i][j] > 0:
                    metrics[i][j] = distance
                    change = True
                    
        if all(metrics[i][j] is not None for i in range(n) for j in range(n)):
            break

        if not change:
            break

        current_power = multiply_matrices(current_power, adjacency)

    return metrics


def find_graph_characteristics(metric_matrix):
    # По матрице метрик находим радиус, диаметр, центр и периферию
    n = len(metric_matrix)
    if any(len(row) != n for row in metric_matrix):
        raise ValueError('Матрица метрик должна быть квадратной')

    eccentricities = []
    for row in metric_matrix:
        if any(value is None for value in row):
            eccentricities.append(None)
        else:
            eccentricities.append(max(row))

    finite = [e for e in eccentricities if e is not None]

    radius = min(finite) if finite else None
    diameter = max(finite) if finite else None

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
    # Печатаем характеристики графа
    def format_value(value):
        return '∞' if value is None else str(value)

    ecc_str = [format_value(e) for e in characteristics['eccentricities']]
    print('\nЭксцентриситеты вершин:', ecc_str)
    print('Радиус графа:', format_value(characteristics['radius']))
    print('Диаметр графа:', format_value(characteristics['diameter']))
    print('Центральные вершины:', characteristics['central_vertices'])
    print('Периферийные вершины:', characteristics['peripheral_vertices'])


def analyze_graph(matrix):
    # Анализ для 2 лабораторной
    print_matrix(matrix, 'Матрица смежности')
    metric_matrix = build_metric_matrix(matrix)
    print_metric_matrix(metric_matrix)
    characteristics = find_graph_characteristics(metric_matrix)
    print_characteristics(characteristics)


# -----------------------------
# ФУНКЦИИ 3 ЛАБОРАТОРНОЙ
# -----------------------------

def to_simple_adjacency(adjacency):
    # Преобразуем матрицу смежности в булеву (0/1)
    n = len(adjacency)
    if any(len(row) != n for row in adjacency):
        raise ValueError('Матрица смежности должна быть квадратной')
    return [[1 if adjacency[i][j] > 0 else 0 for j in range(n)] for i in range(n)]


def find_maximum_independent_sets(adjacency):
    # Ищем максимальные пустые подграфы (независимые множества)
    n = len(adjacency)
    if any(len(row) != n for row in adjacency):
        raise ValueError('Матрица смежности должна быть квадратной')

    conflict = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                conflict[i][j] = adjacency[i][i] > 0
            else:
                conflict[i][j] = adjacency[i][j] > 0 or adjacency[j][i] > 0

    degrees = [sum(1 for j in range(n) if i != j and conflict[i][j]) for i in range(n)]
    order = sorted(range(n), key=lambda v: degrees[v], reverse=True)

    best_size = 0
    best_sets = []

    def dfs(pos, chosen):
        nonlocal best_size, best_sets

        if len(chosen) + (n - pos) < best_size:
            return

        if pos == n:
            size = len(chosen)
            if size > best_size:
                best_size = size
                best_sets = [chosen[:]]
            elif size == best_size:
                best_sets.append(chosen[:])
            return

        v = order[pos]

        can_take = not conflict[v][v]
        if can_take:
            for u in chosen:
                if conflict[v][u]:
                    can_take = False
                    break

        if can_take:
            chosen.append(v)
            dfs(pos + 1, chosen)
            chosen.pop()

        dfs(pos + 1, chosen)

    dfs(0, [])

    normalized = []
    seen = set()
    for subset in best_sets:
        one_based = tuple(sorted(v + 1 for v in subset))
        if one_based not in seen:
            seen.add(one_based)
            normalized.append(list(one_based))

    normalized.sort()
    return normalized, best_size


def color_graph_exact(adjacency):
    # Точная раскраска графа: хроматическое число и цвета вершин
    n = len(adjacency)
    if any(len(row) != n for row in adjacency):
        raise ValueError('Матрица смежности должна быть квадратной')

    for i in range(n):
        if adjacency[i][i] > 0:
            return None, None

    neighbors = [set() for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and (adjacency[i][j] > 0 or adjacency[j][i] > 0):
                neighbors[i].add(j)

    degrees = [len(neighbors[i]) for i in range(n)]

    colors = [-1] * n
    best_count = n + 1
    best_coloring = None

    def pick_vertex():
        uncolored = [v for v in range(n) if colors[v] == -1]
        if not uncolored:
            return None

        def saturation(v):
            return len({colors[u] for u in neighbors[v] if colors[u] != -1})

        return max(uncolored, key=lambda v: (saturation(v), degrees[v]))

    def dfs(used_colors):
        nonlocal best_count, best_coloring

        if used_colors >= best_count:
            return

        v = pick_vertex()
        if v is None:
            best_count = used_colors
            best_coloring = colors[:]
            return

        forbidden = {colors[u] for u in neighbors[v] if colors[u] != -1}

        for c in range(used_colors):
            if c in forbidden:
                continue
            colors[v] = c
            dfs(used_colors)
            colors[v] = -1

        colors[v] = used_colors
        dfs(used_colors + 1)
        colors[v] = -1

    dfs(0)
    return best_count, best_coloring


def print_coloring_result(chromatic_number, colors):
    # Печатаем хроматическое число и классы вершин по цветам
    if chromatic_number is None or colors is None:
        print('\nГраф содержит петли, поэтому правильная раскраска невозможна.')
        return

    print(f'\nХроматическое число графа: {chromatic_number}')
    classes = {}
    for v, color in enumerate(colors, start=1):
        classes.setdefault(color + 1, []).append(v)

    for color in sorted(classes):
        print(f'Цвет {color}: вершины {classes[color]}')


def draw_colored_graph(adjacency, colors=None, title='Раскрашенный граф'):
    # Отрисовываем раскрашенный граф
    n = len(adjacency)
    graph = nx.Graph()
    graph.add_nodes_from(range(n))

    for i in range(n):
        for j in range(i + 1, n):
            if adjacency[i][j] > 0 or adjacency[j][i] > 0:
                graph.add_edge(i, j)

    if colors is None:
        node_colors = ['lightgray'] * n
    else:
        palette = [
            '#FF6B6B', '#4ECDC4', '#FFD166', '#6A4C93', '#06D6A0', '#118AB2',
            '#F77F00', '#8338EC', '#3A86FF', '#8AC926', '#EF476F', '#2A9D8F',
        ]
        node_colors = [palette[c % len(palette)] for c in colors]

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=42)
    nx.draw_networkx_edges(graph, pos, edge_color='#666666', width=2, alpha=0.8)
    nx.draw_networkx_nodes(
        graph,
        pos,
        node_color=node_colors,
        node_size=900,
        edgecolors='black',
        linewidths=1.8,
    )
    labels = {i: i + 1 for i in range(n)}
    nx.draw_networkx_labels(graph, pos, labels, font_size=14, font_weight='bold')
    plt.title(title, fontsize=17, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def analyze_graph_lab3(matrix):
    # Анализ для 3 лабораторной
    simple_adj = to_simple_adjacency(matrix)

    max_sets, max_size = find_maximum_independent_sets(simple_adj)
    print(f'\nМаксимальный пустой подграф: размер {max_size}')
    print('Множества вершин:')
    for idx, subset in enumerate(max_sets, start=1):
        print(f'{idx}. {subset}')

    chromatic_number, colors = color_graph_exact(simple_adj)
    print_coloring_result(chromatic_number, colors)

    if chromatic_number is None:
        draw_colored_graph(simple_adj, None, 'Граф (раскраска невозможна из-за петель)')
    else:
        draw_colored_graph(simple_adj, colors, f'Раскрашенный граф, хроматическое число = {chromatic_number}')

# Функции для 4 ЛАБЫ

def dijkstra_shortest_path(adjacency, start_vertex, end_vertex):
    # Алгоритм Дейкстры: кратчайший путь между двумя вершинами (нумерация вершин с 1)
    n = len(adjacency)
    if n == 0:
        return None, []

    if any(len(row) != n for row in adjacency):
        raise ValueError('Матрица смежности должна быть квадратной')

    if not (1 <= start_vertex <= n and 1 <= end_vertex <= n):
        raise ValueError(f'Номера вершин должны быть от 1 до {n}')

    start = start_vertex - 1
    end = end_vertex - 1

    dist = [float('inf')] * n
    parent = [-1] * n
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        current_dist, v = heapq.heappop(heap)
        if current_dist > dist[v]:
            continue

        if v == end:
            break

        for to in range(n):
            # В не взвешенном графе считаем вес каждого существующего ребра равным 1
            if v != to and adjacency[v][to] > 0:
                candidate = current_dist + 1
                if candidate < dist[to]:
                    dist[to] = candidate
                    parent[to] = v
                    heapq.heappush(heap, (candidate, to))

    if dist[end] == float('inf'):
        return None, []

    path = []
    cur = end
    while cur != -1:
        path.append(cur + 1)
        cur = parent[cur]
    path.reverse()
    return dist[end], path


def run_dijkstra_for_matrix(matrix):
    # Запрашиваем 2 вершины и выводим результат Дейкстры
    n = len(matrix)
    if n == 0:
        print('\nГраф пуст, алгоритм Дейкстры не применим.')
        return

    print('\nАлгоритм Дейкстры')
    print(f'Введите номера вершин от 1 до {n}')

    try:
        start_vertex = int(input('Начальная вершина: '))
        end_vertex = int(input('Конечная вершина: '))
    except ValueError:
        print('Ошибка! Нужно ввести целые номера вершин.')
        return

    try:
        distance, path = dijkstra_shortest_path(matrix, start_vertex, end_vertex)
    except ValueError as error:
        print(f'Ошибка! {error}')
        return

    if distance is None:
        print(f'Путь между вершинами {start_vertex} и {end_vertex} отсутствует.')
    else:
        print(f'Кратчайшее расстояние: {distance}')
        print(f'Кратчайший путь: {path}')

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
            analyze_graph_lab3(matrix)
            run_dijkstra_for_matrix(matrix)

        elif choice == 2:
            matrix = graph_creator.create_full_graph(n)
            print(f'Количество рёбер: {n * (n - 1) // 2}')

            inc_matrix = graph_creator.convert_incidence_matrix(matrix)
            if inc_matrix != [[]]:
                print_matrix(inc_matrix, 'Матрица инцидентности')

            analyze_graph(matrix)
            analyze_graph_lab3(matrix)
            run_dijkstra_for_matrix(matrix)

        elif choice == 3:
            matrix = graph_creator.create_graph_with_loops(n)
            print('\nГраф с петлями создан')

            inc_matrix = graph_creator.convert_incidence_matrix(matrix)
            if inc_matrix != [[]]:
                print_matrix(inc_matrix, 'Матрица инцидентности (петли не отображаются)')

            analyze_graph(matrix)
            analyze_graph_lab3(matrix)
            run_dijkstra_for_matrix(matrix)

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
            analyze_graph_lab3(adj_matrix)
            run_dijkstra_for_matrix(adj_matrix)


if __name__ == '__main__':
    main()

