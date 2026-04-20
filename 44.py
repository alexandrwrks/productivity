import networkx as nx
import random
import matplotlib.pyplot as plt

def create_simple_graph(n):
    """Создание простого связного графа"""
    matrix = [[0] * n for _ in range(n)]
    for i in range(n-1):
        matrix[i][i+1]=1
        matrix[i+1][i]=1
    for i in range(n):
        for j in range(i+2, n):
            if random.random() < 0.2:
                matrix[i][j] = 1
                matrix[j][i] = 1
    return matrix


def create_full_graph(n):
    """Создание полного графа"""
    matrix = [[1] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0
    return matrix


def create_graph_with_loops(n):
    """Создание связного графа с петлями"""
    matrix = [[0] * n for _ in range(n)]

    # Сначала гарантируем связность: цепочка 1-2-3-...-n
    for i in range(n - 1):
        matrix[i][i + 1] = 1
        matrix[i + 1][i] = 1

    # Потом случайно добавляем остальные рёбра
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] == 0:
                matrix[i][j] = random.randint(0, 1)
                matrix[j][i] = matrix[i][j]

    # Отдельно добавляем петли
    for i in range(n):
        matrix[i][i] = random.choice([0, 1, 1, 1])

    return matrix


def create_multi_graph(n):
    """Создание связного мульти графа"""
    G = nx.MultiGraph()
    G.add_nodes_from(range(n))

    # Сначала гарантируем связность: цепочка 1-2-3-...-n
    for i in range(n - 1):
        G.add_edge(i, i + 1)

    # Потом добавляем случайные кратные рёбра
    for i in range(n):
        for j in range(i + 1, n):
            num_edges = random.randint(0, 2)
            for _ in range(num_edges):
                G.add_edge(i, j)
    return G

def convert_to_edge_list(matrix):
    """Преобразование матрицы смежности в список ребер"""
    n = len(matrix)
    edges = []
    for i in range(n):
        for j in range(i, n):
            if matrix[i][j] > 0:
                if i == j:
                    for _ in range(matrix[i][j]):
                        edges.append((i, i))
                else:
                    for _ in range(matrix[i][j]):
                        edges.append((i, j))
    return edges

def convert_incidence_matrix(matrix):
    """Конвертация матрицы смежности в инцидентную (без петель)"""
    n = len(matrix)
    edges = []

    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] == 1:
                edges.append((i, j))

    len_edges = len(edges)
    if len_edges == 0:
        return [[]]

    inc_matrix = [[0] * len_edges for _ in range(n)]

    for e, (v1, v2) in enumerate(edges):
        inc_matrix[v1][e] = 1
        inc_matrix[v2][e] = 1

    return inc_matrix

def convert_incidence_matrix_with_loops(matrix):
    """Конвертация матрицы смежности в инцидентную с учетом петель"""
    n = len(matrix)
    edges = []

    # Собираем ВСЕ ребра, включая петли
    for i in range(n):
        for j in range(i, n):
            if matrix[i][j] > 0:
                for k in range(matrix[i][j]):
                    edges.append((i, j))
    len_edges = len(edges)
    if len_edges == 0:
        return [[]]

    inc_matrix = [[0] * len(edges) for _ in range(n)]

    for e, (v1, v2) in enumerate(edges):
        if v1 == v2:
            inc_matrix[v1][e] += 2
        else:
            inc_matrix[v1][e] += 1
            inc_matrix[v2][e] += 1

    return inc_matrix



def draw_graph(matrix, title='Граф'):
    """Функция для отрисовки графа"""
    n = len(matrix)
    G = nx.Graph()

    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] > 0:
                for k in range(matrix[i][j]):
                    G.add_edge(i, j)

    plt.figure(figsize=(12, 8))

    pos = nx.spring_layout(G, k=3, iterations=50)

    nx.draw_networkx_edges(G, pos, edge_color='#555555', width=2, alpha=0.7)
    nx.draw_networkx_nodes(G, pos, node_color='#87CEEB', node_size=800,
                           edgecolors='darkblue', linewidths=2, alpha=0.9)

    labels = {i: i + 1 for i in range(n)}
    nx.draw_networkx_labels(G, pos, labels, font_size=14, font_weight='bold', font_color='black')

    plt.title(title, fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    # Анализ графа (только для простого)
    if "петлями" not in title and "Мульти" not in title and "Полный" not in title:
        analyze_graph(matrix)

    return G


def draw_multi_graph(G, title='Мультиграф'):
    """Отрисовка мультиграфа"""
    plt.figure(figsize=(12, 8))

    pos = nx.spring_layout(G)
    edges = G.edges()

    if edges:
        nx.draw_networkx_edges(G, pos, edge_color='#555555',
                               width=2, connectionstyle='arc3,rad=0.1', alpha=0.7)

    nx.draw_networkx_nodes(G, pos, node_color='lightgreen',
                           node_size=800, edgecolors='darkgreen',
                           linewidths=2, alpha=0.9)

    labels = {i: i + 1 for i in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=14, font_weight='bold')

    plt.axis('off')
    plt.tight_layout()
    plt.show()
    max_values_rows = []
    # создаем матрицу смежности из графа
    n = G.number_of_nodes()
    adj_matrix = [[0] * n for _ in range(n)]

    # Заполняем матрицу смежности
    for u, v in G.edges():
        adj_matrix[u][v] += 1
        if u != v:
            adj_matrix[v][u] += 1

def draw_graph_with_loops(matrix, title='Граф с петлями'):
    """Отрисовка графа с петлями"""
    n = len(matrix)

    # Создаём граф с петлями
    G = nx.Graph()
    for i in range(n):
        G.add_node(i)

    for i in range(n):
        for j in range(i, n):
            if matrix[i][j] == 1 and i != j:
                G.add_edge(i, j)

    plt.figure(figsize=(12, 8))
    pos = nx.circular_layout(G)

    # Рисуем обычные рёбра
    normal_edges = [(u, v) for u, v in G.edges() if u != v]
    if normal_edges:
        nx.draw_networkx_edges(G, pos, edgelist=normal_edges,
                               edge_color='gray', width=2, alpha=0.7)

    # Рисуем вершины
    nx.draw_networkx_nodes(G, pos, node_color='#87CEEB',
                           node_size=800, edgecolors='darkblue',
                           linewidths=2, alpha=0.9)

    # Добавляем петли
    for i in range(n):
        if matrix[i][i] == 1:
            x, y = pos[i]
            circle = plt.Circle((x, y - 0.2), 0.2, fill=False,
                                edgecolor='red', linewidth=2)
            plt.gca().add_patch(circle)
            # plt.text(x + 0.2, y - 0.3, ' ', fontsize=8, color='red')


    # Подписи
    labels = {i: i + 1 for i in range(n)}
    nx.draw_networkx_labels(G, pos, labels, font_size=14, font_weight='bold')

    plt.title(title, fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()





def compute_distance_matrix(matrix):
    """Матрица расстояний (метрик)"""
    n = len(matrix)
    # Копируем матрицу смежности
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        for j in range(n):
            if matrix[i][j] == 1:
                dist[i][j] = 1

    # Алгоритм Флойда-Уоршелла
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def analyze_graph(matrix):
    """Радиус, диаметр, центр, периферия"""
    dist = compute_distance_matrix(matrix)
    n = len(matrix)

    # Эксцентриситеты
    ecc = [max([dist[i][j] for j in range(n) if j != i]) for i in range(n)]

    radius = min(ecc)
    diameter = max(ecc)
    center = [i + 1 for i, e in enumerate(ecc) if e == radius]
    periphery = [i + 1 for i, e in enumerate(ecc) if e == diameter]

    # Вывод матрицы метрик
    print("\nМатрица метрик (расстояний):")
    for row in dist:
        print(' '.join([f'{int(x):2}' if x != float('inf') else ' ∞' for x in row]))

    print(f"\nРадиус: {radius}")
    print(f"Диаметр: {diameter}")
    print(f"Центральные вершины: {center}")
    print(f"Периферийные вершины: {periphery}")


def main():
    while True:
        print("\n" + "=" * 40)
        print("ГЕНЕРАТОР ГРАФОВ")
        print("=" * 40)
        print("1. Простой граф")
        print("2. Полный граф")
        print("3. Граф с петлями")
        print("4. Мульти граф")
        print("5. Выход")

        try:
            choice = int(input("Выберите действие: "))
            if choice not in [1, 2, 3, 4, 5]:
                print("Ошибка! Введите число от 1 до 5")
                continue
        except ValueError:
            print("Ошибка! Введите число от 1 до 5")
            continue

        if choice == 5:
            print("До свидания!")
            break

        try:
            n = int(input("Введите количество вершин (положительное число): "))
            if n <= 0:
                print("Размер должен быть положительным числом!")
                continue
        except ValueError:
            print("Ошибка! Введите целое положительное число")
            continue

        # Простой граф
        if choice == 1:
            matrix = create_simple_graph(n)
            print("\nМатрица смежности: ")
            for row in matrix:
                print(' '.join(map(str, row)))

            inc_matrix = convert_incidence_matrix(matrix)
            if inc_matrix != [[]]:
                print("\nМатрица инцидентности: ")
                for row in inc_matrix:
                    print(' '.join(map(str, row)))

            draw_graph(matrix, f"Простой граф ({n} вершин)")

        # Полный граф
        elif choice == 2:
            matrix = create_full_graph(n)
            print("\nМатрица смежности (полный граф): ")
            for row in matrix:
                print(' '.join(map(str, row)))

            inc_matrix = convert_incidence_matrix(matrix)
            if inc_matrix != [[]]:
                print("\nМатрица инцидентности: ")
                for row in inc_matrix:
                    print(' '.join(map(str, row)))

            draw_graph(matrix, f"Полный граф ({n} вершин)")


        # Граф с петлями
        elif choice == 3:
            #простой граф с петлями
            matrix = create_graph_with_loops(n)

            print(f"\nГраф с петлями создан!")

            print("\nМатрица смежности:")
            for row in matrix:
                print(' '.join(map(str, row)))

            # Список ребер
            edge_list = convert_to_edge_list(matrix)
            print(f"\nСПИСОК РЕБЕР: {edge_list}")

            # Матрица инцидентности
            inc_matrix = convert_incidence_matrix_with_loops(matrix)
            if inc_matrix != [[]]:
                print("\nМатрица инцидентности:")
                for row in inc_matrix:
                    print(' '.join(map(str, row)))

            # Отрисовка графа с петлями
            draw_graph_with_loops(matrix, f"Граф с петлями ({n} вершин)")

        # Мульти граф
        elif choice == 4:
            G = create_multi_graph(n)
            print(f"\nМультиграф создан!")
            print(f"Вершины: {G.number_of_nodes()}")
            print(f"Рёбра: {G.number_of_edges()}")

            adj_matrix = [[0] * n for _ in range(n)]
            for u, v in G.edges():
                adj_matrix[u][v] += 1
                if u != v:
                    adj_matrix[v][u] += 1

            print("\nМатрица смежности")
            for row in adj_matrix:
                print(' '.join(map(str, row)))

            edge_list = list(G.edges())
            print(f"\nСПИСОК РЕБЕР: {edge_list}")

            edges = list(G.edges())
            if edges:
                inc_matrix = [[0] * len(edges) for _ in range(n)]
                for e, (u, v) in enumerate(edges):
                    inc_matrix[u][e] += 1
                    if u != v:
                        inc_matrix[v][e] += 1

                print("\nМатрица инцидентности:")
                for row in inc_matrix:
                    print(' '.join(map(str, row)))

            draw_multi_graph(G, f"Мультиграф ({n} вершин)")


if __name__ == "__main__":
    main()