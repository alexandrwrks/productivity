import networkx as nx
import random
import matplotlib.pyplot as plt


class CreateGraph:
    def __init__(self):
        pass

    def create_simple_graph(self, n):
        """Создание простого связного графа"""
        matrix = [[0] * n for _ in range(n)]
        for i in range(n - 1):
            matrix[i][i + 1] = 1
            matrix[i + 1][i] = 1
        return matrix

    def create_full_graph(self, n):
        """Создание полного графа"""
        matrix = [[1] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0
        return matrix

    def create_graph_with_loops(self, n):
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


    def convert_incidence_matrix(self, matrix):
        """Функция для конвертации матриицы в инцидентную с учётом петель"""
        n = len(matrix)
        edges = []

        for i in range(n):
            for j in range(i, n):
                if matrix[i][j] > 0:
                    for k in range(matrix[i][j]):
                        edges.append((i, j))

        len_edges = len(edges)
        if len_edges == 0:
            return [[]]

        inc_matrix = [[0] * len_edges for _ in range(n)]

        for e, (v1, v2) in enumerate(edges):
            inc_matrix[v1][e] += 1
            inc_matrix[v2][e] += 1

        return inc_matrix

    def draw_graph(self, matrix, title='Граф'):
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
        nx.draw_networkx_nodes(G, pos, node_color='#87CEEB', node_size=800, edgecolors='darkblue', linewidths=2,
                               alpha=0.9)

        labels = {i: i + 1 for i in range(n)}
        nx.draw_networkx_labels(G, pos, labels, font_size=14, font_weight='bold', font_color='black')

        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

        return G


def main():
    graph_creator = CreateGraph()

    while True:
        print("\n" + "=" * 40)
        print("💕 ГЕНЕРАТОР ГРАФОВ")
        print("\n" + "=" * 40)
        print(" 1. Простой граф")
        print(" 2. Полный граф")
        print(" 3. Граф с петлями")
        print(" 4. Мульти граф")
        print(" 5. Выход")
        try:
            choice = int(input("💕 Выберите действие: "))
            if choice not in [1, 2, 3, 4, 5]:
                print("💕 Ошибка! Введите число от 1 до 5")
                continue
        except ValueError:
            print("💕 Ошибка! Введите число от 1 до 5")
            continue
 
        if choice == 5:
            print("💕 До свидания!")
            break

        try:
            n = int(input("💕 Введите размер матрицы - количество вершин(положительное число): "))
            if n <= 0:
                print("💕 Размер должен быть положительным числом!")
                continue
        except ValueError:
            print("💕 Ошибка! Введите целое положительное число")
            continue

        if choice == 1:
            matrix = graph_creator.create_simple_graph(n)
            print("\n💕 Матрица смежности: ")
            for row in matrix:
                print(' '.join(map(str, row)))

            inc_matrix = graph_creator.convert_incidence_matrix(matrix)
            if inc_matrix != [[]]:
                print("\n💕 Матрица инцендентности: ")
                for row in inc_matrix:
                    print(' '.join(map(str, row)))

            graph_creator.draw_graph(matrix, f"Простой граф ({n} вершин)")

        elif choice == 2:
            matrix = graph_creator.create_full_graph(n)
            print(f"💕 Количество рёбер: {n * (n - 1) // 2}")
            print("\n💕 Матрица смежности (полный граф): ")
            for row in matrix:
                print(' '.join(map(str, row)))

            inc_matrix = graph_creator.convert_incidence_matrix(matrix)
            if inc_matrix != [[]]:
                print("\n💕 Матрица инцидетности: ")
                for row in inc_matrix:
                    print(' '.join(map(str, row)))

            graph_creator.draw_graph(matrix, f"Полный граф ({n} вершин)")

        elif choice == 3:
            matrix = graph_creator.create_graph_with_loops(n)
            print("\n💕  Граф с петлями создан")
            print("\n💕 Матрица смежности (1 на диагонали = петля):")
            for row in matrix:
                print(' '.join(map(str, row)))

            inc_matrix = graph_creator.convert_incidence_matrix(matrix)
            if inc_matrix != [[]]:
                print("\n💕  Матрица инцидентности (петли учитываются):")
                for row in inc_matrix:
                    print(' '.join(map(str, row)))

            # Создаём граф с петлями
            G = nx.Graph()
            for i in range(n):
                for j in range(i, n):
                    if matrix[i][j] == 1:
                        G.add_edge(i, j)

            # Отрисовка графа с петлями
            plt.figure(figsize=(12, 8))
            pos = nx.circular_layout(G)

            # Рисуем только обычные рёбра (без петель)
            normal_edges = [(u, v) for u, v in G.edges() if u != v]
            nx.draw_networkx_edges(G, pos, edgelist=normal_edges, edge_color='gray', width=2, alpha=0.7)

            # Рисуем вершины
            nx.draw_networkx_nodes(G, pos, node_color='#87CEEB',
                                   node_size=800, edgecolors='darkblue',
                                   linewidths=2, alpha=0.9)

            # Добавляем петли
            for node in G.nodes():
                if G.has_edge(node, node):
                    x, y = pos[node]
                    circle = plt.Circle((x, y - 0.2), 0.2, fill=False,
                                        edgecolor='gray', linewidth=2)
                    plt.gca().add_patch(circle)

            # Подписи
            labels = {i: i + 1 for i in range(n)}
            nx.draw_networkx_labels(G, pos, labels, font_size=14,
                                    font_weight='bold')

            plt.title(f"Граф с петлями ({n} вершин)", fontsize=16, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
            plt.show()

        elif choice == 4:

            G = graph_creator.draw_graph(n)
            print(f"\n💕  Мультиграф создан!")
            print(f"💕 Вершины: {G.number_of_nodes()}")
            print(f"💕 Рёбра: {G.number_of_edges()}")

            adj_matrix = [[0] * n for _ in range(n)]
            for u, v in G.edges():
                adj_matrix[u][v] += 1
                if u != v:
                    adj_matrix[v][u] += 1

            print("\n💕  Матрица смежности (числа показывают количество рёбер):")
            for row in adj_matrix:
                print(' '.join(map(str, row)))

            edges = list(G.edges())
            if edges:
                inc_matrix = [[0] * len(edges) for _ in range(n)]
                for e, (u, v) in enumerate(edges):
                    inc_matrix[u][e] += 1
                    if u != v:
                        inc_matrix[v][e] += 1

                print("\n💕  Матрица инцидентности:")
                for row in inc_matrix:
                    print(' '.join(map(str, row)))

            # Показываем все рёбра
            if G.number_of_edges() > 0:
                print("\n💕 Список рёбер:")
                edge_dict = {}
                for u, v, key in G.edges(keys=True):
                    edge_key = tuple(sorted([u, v]))
                    if edge_key not in edge_dict:
                        edge_dict[edge_key] = []
                    edge_dict[edge_key].append(key + 1)

                for (u, v), keys in edge_dict.items():
                    print(f"💕 {u + 1} — {v + 1}: {len(keys)} ребро(а)")

                graph_creator.draw_graph(G, f"Мультиграф ({n} вершин)")

if __name__ == "__main__":
    main()