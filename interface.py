import sys
import networkx as nx
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QPushButton, QLabel, 
                             QSpinBox, QGroupBox, QMessageBox)
from PyQt5.QtCore import Qt

class GraphCanvas(FigureCanvas):
    """Класс для отображения графов matplotlib в PyQt"""
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(8, 6))
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)

class GraphViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Настройка главного окна
        self.setWindowTitle("Просмотрщик графов")
        self.setGeometry(100, 100, 900, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout(central_widget)
        
        # Верхняя панель с элементами управления
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        
        # Группа выбора графа
        graph_group = QGroupBox("Параметры графа")
        graph_layout = QHBoxLayout(graph_group)
        
        # Метка для выбора графа
        label = QLabel("Тип графа:")
        graph_layout.addWidget(label)
        
        # ComboBox для выбора графа
        self.graph_selector = QComboBox()
        self.graph_selector.addItems([
            "Простой граф",
            "Полный граф",
            "Граф с петлями",
            "Мультиграф"
        ])
        self.graph_selector.currentIndexChanged.connect(self.update_graph)
        graph_layout.addWidget(self.graph_selector)
        
        # Метка для количества вершин
        vertices_label = QLabel("Кол-во вершин:")
        graph_layout.addWidget(vertices_label)
        
        # SpinBox для выбора количества вершин
        self.vertices_spin = QSpinBox()
        self.vertices_spin.setRange(2, 10)  # Ограничим до 10 для наглядности
        self.vertices_spin.setValue(5)
        self.vertices_spin.valueChanged.connect(self.update_graph)
        graph_layout.addWidget(self.vertices_spin)
        
        # Добавляем группу в основной layout
        control_layout.addWidget(graph_group)
        
        # Растягивающийся промежуток
        control_layout.addStretch()
        
        # Кнопка выхода
        self.exit_button = QPushButton("Выход")
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setFixedSize(100, 30)
        control_layout.addWidget(self.exit_button)
        
        # Добавляем панель управления в главный layout
        main_layout.addWidget(control_panel)
        
        # Создаем холст для графика
        self.canvas = GraphCanvas()
        main_layout.addWidget(self.canvas)
        
        # Отображаем первый граф
        self.update_graph()
        
    def create_simple_graph(self, n):
        """Создание простого графа"""
        G = nx.Graph()
        G.add_nodes_from(range(n))
        
        # Добавляем несколько случайных ребер (не все возможные)
        import random
        random.seed(42)  # Для воспроизводимости
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.4:  # 40% вероятность ребра
                    edges.append((i, j))
        G.add_edges_from(edges)
        
        pos = nx.spring_layout(G)
        self.canvas.axes.clear()
        nx.draw(G, pos, ax=self.canvas.axes, with_labels=True, 
                node_color='lightblue', node_size=500, 
                font_size=10, font_weight='bold',
                edge_color='gray')
        self.canvas.axes.set_title(f"Простой граф с {n} вершинами")
        
    def create_complete_graph(self, n):
        """Создание полного графа K_n"""
        G = nx.complete_graph(n)
        pos = nx.spring_layout(G)
        self.canvas.axes.clear()
        nx.draw(G, pos, ax=self.canvas.axes, with_labels=True, 
                node_color='lightgreen', node_size=500, 
                font_size=10, font_weight='bold',
                edge_color='darkgreen')
        self.canvas.axes.set_title(f"Полный граф K{n}")
        
    def create_graph_with_loops(self, n):
        """Создание графа с петлями"""
        G = nx.Graph()
        G.add_nodes_from(range(n))
        
        # Добавляем обычные ребра
        import random
        random.seed(42)
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.3:
                    G.add_edge(i, j)
        
        # В networkx нет прямой поддержки петель, поэтому создадим их вручную
        pos = nx.spring_layout(G)
        self.canvas.axes.clear()
        
        # Рисуем вершины
        nx.draw_networkx_nodes(G, pos, ax=self.canvas.axes, 
                              node_color='lightcoral', node_size=500)
        
        # Рисуем обычные ребра
        nx.draw_networkx_edges(G, pos, ax=self.canvas.axes, edge_color='gray')
        
        # Рисуем петли (вручную, как маленькие круги вокруг вершин)
        for node in G.nodes():
            if random.random() < 0.3:  # 30% вероятность петли
                x, y = pos[node]
                circle = plt.Circle((x, y-0.1), 0.1, fill=False, 
                                   edgecolor='red', linewidth=2)
                self.canvas.axes.add_patch(circle)
                # Добавляем стрелку или метку для петли
                self.canvas.axes.annotate('', xy=(x, y-0.1), xytext=(x, y),
                                        arrowprops=dict(arrowstyle='->', 
                                                       color='red', lw=1))
        
        # Рисуем подписи вершин
        nx.draw_networkx_labels(G, pos, ax=self.canvas.axes, font_size=10)
        
        self.canvas.axes.set_title(f"Граф с петлями ({n} вершин)")
        self.canvas.axes.set_xlim(-1.5, 1.5)
        self.canvas.axes.set_ylim(-1.5, 1.5)
        
    def create_multigraph(self, n):
        """Создание мультиграфа (с кратными ребрами)"""
        G = nx.MultiGraph()
        G.add_nodes_from(range(n))
        
        # Добавляем кратные ребра
        import random
        random.seed(42)
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                # Случайное количество ребер между вершинами (0-3)
                num_edges = random.randint(0, 3)
                for _ in range(num_edges):
                    edges.append((i, j))
        G.add_edges_from(edges)
        
        pos = nx.spring_layout(G)
        self.canvas.axes.clear()
        
        # Рисуем вершины
        nx.draw_networkx_nodes(G, pos, ax=self.canvas.axes,
                              node_color='lightyellow', node_size=500)
        
        # Для мультиграфа рисуем кратные ребра со смещением
        from collections import Counter
        edge_count = Counter()
        
        for u, v in G.edges():
            if u < v:  # Считаем каждое направление отдельно
                edge_count[(u, v)] += 1
        
        # Рисуем кратные ребра
        for (u, v), count in edge_count.items():
            if count == 1:
                nx.draw_networkx_edges(G, pos, [(u, v)], ax=self.canvas.axes,
                                     edge_color='blue', width=1)
            else:
                # Для кратных ребер рисуем их с небольшим смещением
                rad = 0.1
                for i in range(count):
                    nx.draw_networkx_edges(G, pos, [(u, v)], ax=self.canvas.axes,
                                         edge_color='blue', width=1,
                                         connectionstyle=f'arc3,rad={rad * (i+1)}')
        
        # Рисуем подписи вершин
        nx.draw_networkx_labels(G, pos, ax=self.canvas.axes, font_size=10)
        
        self.canvas.axes.set_title(f"Мультиграф ({n} вершин)")
        
    def update_graph(self):
        """Обновление графа в соответствии с выбором"""
        # Получаем выбранный индекс и количество вершин
        current_index = self.graph_selector.currentIndex()
        n = self.vertices_spin.value()
        
        try:
            # Создаем соответствующий граф
            if current_index == 0:
                self.create_simple_graph(n)
            elif current_index == 1:
                self.create_complete_graph(n)
            elif current_index == 2:
                self.create_graph_with_loops(n)
            elif current_index == 3:
                self.create_multigraph(n)
            
            # Обновляем холст
            self.canvas.draw()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось создать граф: {str(e)}")

def main():
    app = QApplication(sys.argv)
    viewer = GraphViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()