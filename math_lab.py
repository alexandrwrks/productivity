import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
import sys

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.button_is_checked = True
        
        self.setWindowTitle("My app")

        button = QPushButton("Push Me")
        button.setCheckable(True)
        # button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)
        button.setChecked(self.button_is_checked)

        self.setFixedSize(QSize(400, 300))

        self.setCentralWidget(button)

    # def the_button_was_clicked(self):
    #     print("Clicked!")

    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked

        print(self.button_is_checked)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

# Ввод размера матрицы с клавиатуры
# n = int(input('Размер матрицы: '))

# def create(n):
#     matrix = [[0] * n for _ in range(n)]
#     for i in range(n - 1):
#         matrix[i][i + 1] = 1
#         matrix[i + 1][i] = 1
#     return matrix

# m = create(n)

# for row in m:
#     print(row)
# G = nx.Graph()
# for i in range(n):
#     for j in range(i + 1, n):
#         if m[i][j] == 1:
#             G.add_edge(i, j)

# # Рисуем граф
# plt.figure(figsize=(12, 4))

# # Располагаем вершины
# pos = {i: (i * 2, 0) for i in range(n)}

# # Рисуем рёбра (сделаем их потолще)
# # nx.draw_networkx_edges(G, pos, edge_color='#555555', width=3)

# # # Рисуем вершины (побольше и красивее)
# # nx.draw_networkx_nodes(G, pos, node_color='#87CEEB',  # небесно-голубой
# #                        node_size=1000, edgecolors='darkblue', linewidths=2)

# # # Рисуем подписи (крупным шрифтом)
# # labels = {i: i+1 for i in range(n)}
# # nx.draw_networkx_labels(G, pos, labels, font_size=16, font_weight='bold',
# #                         font_color='black')


# # plt.axis('off')
# # plt.tight_layout()
# # plt.show()

# # # Создаём случайную матрицу смежности
# # A = [[0] * n for i in range(n)]
# # for i in range(n):
# #     for j in range(i + 1, n):
# #         A[i][j] = random.randint(0, 1)
# #         A[j][i] = A[i][j]

# # Выводим матрицу смежности
# # print("\nМатрица смежности:")
# # for r in A:
# #     print(r)

# # Преобразуем в numpy array и создаём граф
# # A_np = np.array(A)
# # G = nx.from_numpy_array(A_np)

# # Рисуем граф
# plt.figure(figsize=(8, 6))
# nx.draw(G, with_labels=True, font_size=12, node_color='lightgreen',
#         node_size=600, font_weight='bold', edge_color='gray')
# plt.title(f"Граф с {n} вершинами")
# plt.show()

# def cmtb(adj_matrix):
#     n = len(adj_matrix)
#     edges = []

#     for i in range(n):
#         for j in range(i + 1, n):
#             if adj_matrix[i][j] == 1:
#                 edges.append((i, j))

#     n_edges = len(edges)
#     inc_matrix = [[0] * n_edges for _ in range(n)]

#     for e, (v1, v2) in enumerate(edges):
#         inc_matrix[v1][e] = 1
#         inc_matrix[v2][e] = 1

#     return inc_matrix

# t = cmtb(m)
# print('новая')
# for row in t:
#     print(row)