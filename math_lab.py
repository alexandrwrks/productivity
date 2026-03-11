import networkx as nx
import matplotlib.pyplot as plt
# from random import randint

import numpy as np
import random

const_num = 5

# G = nx.Graph()

# G.add_nodes_from([1, 2, 3, 4, 5])

# G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5)])

# plt.figure(figsize=(8, 6))
# nx.draw(G, node_color='lightblue',  node_size=500, font_size=16, font_weight='bold')
# plt.title("Простой неоринтерончайый граф") 
# plt.show()
n = int(input('Размер матрицы: '))

A = [[0]*n for i in range(n)]
for i in range(n):
    for j in range(i+1, n):
        A[i][j] = random.randint(0, 1)
        A[j][i] = A[i][j]
    
for r in A:
    print(r)

A = np.array(A)
G = nx.from_numpy_array(A)
nx.draw(G, with_labels=True, font_size=10, linewidths=1, node_color='g')
M = nx.incidence_matrix(G, oriented=True)
print(M.todense())
plt.show()


# add_numbers_to_graph(massive)
# class Creategraph():
#     def __init__(self, num):
#         self.num = num
#         # self.create_matrix()
#         self.create_graph()

#     def create_matrix(self):
#         print("a1 | a2 | a3 | a4 | a5")
#         for i in range(self.num):
#             print(f"a{i+1} |", end=" ")
#             for i in range(self.num):
                
#                 num = random.randint(0, 3)
#                 print(num, "|", end="  ")
#             print()
        
#     def create_graph(self):

#         G = nx.Graph()

#         G.add_edge(1, 2, weight=4.7)
#         G.add_edges_from([(3, 4), (4, 5)], color="red")
#         G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight':8})])
#         G[1][2]['weight'] = 4.7
#         G.edges[1, 2]['weight'] = 4




# # cg.create_matrix(5)