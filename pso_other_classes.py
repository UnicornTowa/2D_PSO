from os import getcwd, path, remove

import numpy as np
import plotly.graph_objects as go
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QCloseEvent, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from plotly import io

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import pso
import common

# Класс окна отображающего график
class Draw3DWindow(QWidget):
    # Конструктор класса
    def __init__(self, parent=None, particles: list[pso.Particle] = None):
        # Инициализация окна и необходимых параметров
        super(Draw3DWindow, self).__init__(parent)
        self.setWindowTitle("Interactive graph")
        self.resize(800, 800)
        self.setWindowIcon(QIcon('plot.png'))
        self.filename = 'graph.html'
        self.particles = particles

        # Инициализация интерфейса для открытия html
        self.web_view = QWebEngineView()
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        self.setLayout(layout)

        self.draw_html()

    # Добавление на график точек из итоговой таблицы
    def add_points(self, fig: go.Figure) -> None:
        x = []
        y = []
        z = []
        for i in range(len(self.particles)):
            pos = self.particles[i].pos
            x.append(float(pos[0]))
            y.append(float(pos[1]))
            z.append(float(pso.ff(pos)))
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=7)))

    # Построение и отображение графика
    def draw_html(self) -> None:
        z = pso.fitness_function
        x1, x2, y1, y2 = pso.ranges.values()
        _x, _y = np.mgrid[x1:x2:10j * round(x2 - x1), y1:y2:10j * round(y2 - y1)]
        _z = np.zeros((10 * round(x2 - x1), 10 * round(y2 - y1)), dtype=float)
        i = 0
        for x in _x:
            j = 0
            for y in _y:
                _z[i][j] = z(x[i], y[j])
                j += 1
            i += 1
        fig = go.Figure(go.Surface(
            x=_x,
            y=_y,
            z=_z,
        ))

        if self.particles is not None:
            self.add_points(fig)

        # Построение графика в .html и открытие его в окне
        with open(self.filename, 'w') as f:
            f.write(io.to_html(fig))
        self.web_view.load(QUrl.fromLocalFile(getcwd() + '\\' + self.filename))

    # Деструктор, удаляющий созданный файл
    def closeEvent(self, a0: QCloseEvent) -> None:
        if path.isfile(self.filename):
            remove(self.filename)
        a0.accept()


# Класс окна в котором можно менять начальные границы
class RangesWindow(QWidget):
    def __init__(self, parent=None):
        super(RangesWindow, self).__init__(parent)
        self.setWindowTitle("Ranges input")
        self.resize(350, 275)
        self.setWindowIcon(QIcon('numbers.png'))

        # Шрифт, валидатор
        f = common.f
        only_int = common.only_int
        # Заголовок
        self.title = QLabel('Ввод пользовательских границ', self)
        self.title.setFont(QFont("Times", 10, QFont.Bold, QFont.StyleItalic))
        self.title.move(10, 10)
        # Метки и поля ввода
        self.x1_label = QLabel('X1:', self)
        self.x1_input = QLineEdit(self)
        self.x1_input.setText('-10')
        self.x1_input.setPlaceholderText('int')
        self.x1_input.setValidator(only_int)

        self.x2_label = QLabel('X2:', self)
        self.x2_input = QLineEdit(self)
        self.x2_input.setText('10')
        self.x2_input.setPlaceholderText('int')
        self.x2_input.setValidator(only_int)

        self.y1_label = QLabel('Y1:', self)
        self.y1_input = QLineEdit(self)
        self.y1_input.setText('-10')
        self.y1_input.setPlaceholderText('int')
        self.y1_input.setValidator(only_int)

        self.y2_label = QLabel('Y2:', self)
        self.y2_input = QLineEdit(self)
        self.y2_input.setText('10')
        self.y2_input.setPlaceholderText('int')
        self.y2_input.setValidator(only_int)

        self.x1_label.setFont(f)
        self.x2_label.setFont(f)
        self.y1_label.setFont(f)
        self.y2_label.setFont(f)
        self.x1_input.setFont(f)
        self.x2_input.setFont(f)
        self.y1_input.setFont(f)
        self.y2_input.setFont(f)

        self.x1_label.move(10, 80)
        self.x1_input.move(50, 80)
        self.x2_label.move(10, 110)
        self.x2_input.move(50, 110)
        self.y1_label.move(10, 140)
        self.y1_input.move(50, 140)
        self.y2_label.move(10, 170)
        self.y2_input.move(50, 170)
        # Кнопки сброса и установки границ
        self.set_button = QPushButton('Set', self)
        self.set_button.clicked.connect(self.set_ranges)
        self.set_button.setMinimumWidth(100)

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_ranges)
        self.reset_button.setMinimumWidth(100)

        self.set_button.move(10, 210)
        self.reset_button.move(130, 210)
        self.set_button.setFont(f)
        self.reset_button.setFont(f)

    # Функция, проверяющая корректность ввода и устанавливающая новые границы
    def set_ranges(self) -> None:
        x1 = int(self.x1_input.text())
        x2 = int(self.x2_input.text())
        y1 = int(self.y1_input.text())
        y2 = int(self.y2_input.text())
        if x1 >= x2 or y1 >= y2:
            common.input_error('Проверьте корректность границ')
        else:
            pso.set_ranges(x1, x2, y1, y2)

    # Функция сбрасывающая границы до исходных
    def reset_ranges(self) -> None:
        self.x1_input.setText('-10')
        self.x2_input.setText('10')
        self.y1_input.setText('-10')
        self.y2_input.setText('10')
        pso.reset_ranges()


class Draw2D(FigureCanvasQTAgg, QWidget):

    def __init__(self, parent=None, width=100, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(Draw2D, self).__init__(self.fig)