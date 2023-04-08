import random
import sys
from functools import partial
# noinspection PyUnresolvedReferences
from math import *
from random import randint

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QCheckBox, QMainWindow

import common
import pso
import pso_other_classes


# Расстояние между точками
def pho(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2)

# Основной класс
class MainWindow(QMainWindow):
    # Конструктор класса
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('particle.png'))  # Иконка

        # Рой
        self.swarm = pso.PSO()

        # Текстовые поля
        self.params = QLabel('Parameters', self)
        self.params.setFont(QFont("Times", 10, QFont.Bold, QFont.StyleItalic))
        self.params.move(10, 10)
        self.params.setFixedWidth(150)

        self.graph_label = QLabel('Output graph', self)
        self.graph_label.setFont(QFont("Times", 10, QFont.Bold, QFont.StyleItalic))
        self.graph_label.move(450, 10)
        self.graph_label.setFixedWidth(150)

        self.control = QLabel('Control', self)
        self.control.setFont(QFont("Times", 10, QFont.Bold, QFont.StyleItalic))
        self.control.move(10, 240)
        self.control.setFixedWidth(150)

        self.iters_label = QLabel('Iterations', self)
        self.iters_label.setFont(QFont("Times", 10, QFont.Bold, QFont.StyleItalic))
        self.iters_label.move(10, 310)
        self.iters_label.setFixedWidth(150)

        self.output = QLabel('Output', self)
        self.output.setFont(QFont("Times", 10, QFont.Bold, QFont.StyleItalic))
        self.output.move(10, 380)
        self.output.setFixedWidth(150)

        # Ввод пользовательской функции
        self.fitness_label = QLabel('Input function:', self)
        self.fitness_label.setFixedWidth(200)
        self.fitness_label.move(10, 40)
        self.fitness_input = QLineEdit(self)
        self.fitness_input.setText('x**2+3*y**2+2*x*y')
        self.fitness_input.setPlaceholderText('Input your f(x, y)')
        self.fitness_input.setReadOnly(True)
        self.fitness_input.move(160, 40)
        self.fitness_input.setMinimumWidth(250)

        # Создание меток и полей ввода для параметров
        self.num_of_particles_label = QLabel('Num of particles:', self)
        self.num_of_particles_label.setFixedWidth(200)
        self.num_of_particles_input = QLineEdit(self)
        self.num_of_particles_input.setText('100')
        self.num_of_particles_input.setFixedWidth(150)
        self.num_of_particles_input.setPlaceholderText('int, >=2')
        self.num_of_particles_input.setValidator(common.only_int)

        self.omega_label = QLabel('Inertia rate:', self)
        self.omega_label.setFixedWidth(200)
        self.omega_input = QLineEdit(self)
        self.omega_input.setPlaceholderText('float, [0, 2]')
        self.omega_input.setText('0.5')
        self.omega_input.setFixedWidth(150)
        self.omega_input.setValidator(common.only_float)

        self.phi_p_label = QLabel('Cognitive rate:', self)
        self.phi_p_label.setFixedWidth(200)
        self.phi_p_input = QLineEdit(self)
        self.phi_p_input.setText('1')
        self.phi_p_input.setPlaceholderText('float, [0, 2]')
        self.phi_p_input.setFixedWidth(150)
        self.phi_p_input.setValidator(common.only_float)

        self.phi_g_label = QLabel('Social rate:', self)
        self.phi_g_label.setFixedWidth(200)
        self.phi_g_input = QLineEdit(self)
        self.phi_g_input.setText('1')
        self.phi_g_input.setPlaceholderText('float, [0, 2]')
        self.phi_g_input.setFixedWidth(150)
        self.phi_g_input.setValidator(common.only_float)

        # Создание чекбоксов
        self.edit_checkbox = QCheckBox('I want custom function (test, slower)', self)
        self.edit_checkbox.setFont(common.f)
        self.edit_checkbox.setFixedWidth(370)
        self.edit_checkbox.toggled.connect(self.edit_on_clicked)

        # Создание кнопок
        self.reset_button = QPushButton('Reset params', self)
        self.reset_button.clicked.connect(self.reset_params)
        self.reset_button.setMinimumWidth(100)

        self.ranges_button = QPushButton('Change ranges', self)
        self.ranges_button.clicked.connect(self.set_ranges)
        self.ranges_window = None

        self.draw_button = QPushButton('Draw 3D', self)
        self.draw_button.setToolTip('Note: slow for complicated functions')
        self.draw_button.clicked.connect(self.draw_3d)
        self.draw_window = None

        self.run1_button = QPushButton('+1', self)
        self.run1_button.clicked.connect(partial(self.iters, 1))
        self.run10_button = QPushButton('+10', self)
        self.run10_button.clicked.connect(partial(self.iters, 10))
        self.run100_button = QPushButton('+100', self)
        self.run100_button.clicked.connect(partial(self.iters, 100))
        self.run1000_button = QPushButton('+1000', self)
        self.run1000_button.clicked.connect(partial(self.iters, 1000))
        self.run_new_button = QPushButton('New run', self)
        self.run_new_button.clicked.connect(partial(self.iters, 0))

        # Расположение элементов ввода на окне
        self.num_of_particles_label.move(10, 80)
        self.num_of_particles_input.move(160, 80)

        self.omega_label.move(10, 110)
        self.omega_input.move(160, 110)

        self.phi_p_label.move(10, 140)
        self.phi_p_input.move(160, 140)

        self.phi_g_label.move(10, 170)
        self.phi_g_input.move(160, 170)

        self.edit_checkbox.move(10, 205)

        self.reset_button.move(10, 270)
        self.reset_button.setFixedWidth(150)
        self.ranges_button.move(160, 270)
        self.ranges_button.setFixedWidth(150)
        self.draw_button.move(310, 270)
        self.draw_button.setFixedWidth(120)

        self.run1_button.move(10, 340)
        self.run1_button.setFixedWidth(80)
        self.run10_button.move(90, 340)
        self.run10_button.setFixedWidth(80)
        self.run100_button.move(170, 340)
        self.run100_button.setFixedWidth(80)
        self.run1000_button.move(250, 340)
        self.run1000_button.setFixedWidth(80)
        self.run_new_button.move(330, 340)
        self.run_new_button.setFixedWidth(100)


        # Вывод результатов
        self.best_sol = QLabel('f(x, y):', self)
        self.best_sol.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.best_sol_coord = QLabel('x:\ny:', self)
        self.best_sol_coord.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.iters = QLabel('Iterations finished: 0', self)
        self.best_sol.setMinimumWidth(350)
        self.best_sol_coord.setMinimumWidth(350)
        self.best_sol_coord.setMinimumHeight(55)
        self.iters.setMinimumWidth(300)

        self.best_sol.setFont(common.f)
        self.best_sol_coord.setFont(common.f)
        self.iters.setFont(common.f)

        self.best_sol.move(10, 410)
        self.best_sol_coord.move(10, 440)
        self.iters.move(10, 500)

        # Установка шрифтов
        self.fitness_input.setFont(common.f)
        self.fitness_label.setFont(common.f)
        self.num_of_particles_input.setFont(common.f)
        self.num_of_particles_label.setFont(common.f)
        self.omega_label.setFont(common.f)
        self.omega_input.setFont(common.f)
        self.phi_p_input.setFont(common.f)
        self.phi_p_label.setFont(common.f)
        self.phi_g_input.setFont(common.f)
        self.phi_g_label.setFont(common.f)
        self.reset_button.setFont(common.f)
        self.draw_button.setFont(common.f)
        self.ranges_button.setFont(common.f)
        self.run1_button.setFont(common.f)
        self.run10_button.setFont(common.f)
        self.run100_button.setFont(common.f)
        self.run1000_button.setFont(common.f)
        self.run_new_button.setFont(common.f)

        self.canvas = pso_other_classes.Draw2D(width=5, height=4, dpi=100)
        self.canvas.fig.tight_layout()
        self.canvas.move(450, 45)
        self.canvas.setFixedSize(500, 500)
        self.layout().addWidget(self.canvas)
        self.update_contour()
        self.scat = self.update_graph()

        # Установка размеров окна и заголовка
        self.resize(1000, 550)
        self.setWindowTitle('PSO Algorithm')


    def update_contour(self):
        x1, x2, y1, y2 = pso.ranges.values()
        self.canvas.axes.cla()
        self.canvas.axes.set_xlim(x1, x2)
        self.canvas.axes.set_ylim(y1, y2)
        x, y = np.mgrid[x1:x2:10j * round(x2 - x1), y1:y2:10j * round(y2 - y1)]
        z = np.vectorize(pso.fitness_function)(x, y)
        self.canvas.axes.contour(x, y, z, alpha=0.5)
        self.canvas.draw()


    def update_graph(self, scat=None):
        if scat:
            scat.remove()
        num_of_particles = self.swarm.swarm.size
        x_s = np.empty((1, num_of_particles), dtype=float)
        y_s = np.empty((1, num_of_particles), dtype=float)
        for i in range(num_of_particles):
            pos = self.swarm.swarm[0][i].pos
            x_s[0][i] = (pos[0])
            y_s[0][i] = (pos[1])
        new_scat = self.canvas.axes.scatter(x_s, y_s, c=random.choice(common.colors))
        self.canvas.draw()
        return new_scat


    # Запуск алгоритма
    def iters(self, count: int):
        if not self.set_params():
            return
        if count == 0:
            if self.edit_checkbox.isChecked() and not self.set_custom_ff():
                return
            self.swarm.reset()
            self.update_contour()
        else:
            self.swarm.pso(count)
        self.set_res(*self.swarm.get_res())
        self.scat = self.update_graph(self.scat)

    # Установка границ
    def set_ranges(self):
        self.ranges_window = pso_other_classes.RangesWindow()
        self.ranges_window.show()

    # Построение графика
    def draw_3d(self):
        self.draw_window = pso_other_classes.Draw3DWindow(particles=self.swarm.swarm[0])
        self.draw_window.show()


    # Сброс параметров
    def reset_params(self):
        self.num_of_particles_input.setText('100')
        self.omega_input.setText('0.5')
        self.phi_p_input.setText('1')
        self.phi_g_input.setText('1')
        self.edit_checkbox.setChecked(False)


    # Переключатель использования кастомной функции
    def edit_on_clicked(self):
        if self.edit_checkbox.isChecked():
            self.fitness_input.setReadOnly(False)
            self.fitness_input.clear()
        if not self.edit_checkbox.isChecked():
            self.fitness_input.setReadOnly(True)
            self.fitness_input.setText('x**2+3*y**2+2*x*y')
            pso.reset_ff()

    # Присвоение значений полям в блоке результатов
    def set_res(self, ff, sol, i):
        self.best_sol.setText('f(x,y): ' + str(ff))
        self.best_sol_coord.setText('x:       ' + str(sol[0]) + '\ny:       ' + str(sol[1]))
        self.iters.setText('Iterations finished: ' + str(i))

    # Установка кастомной функции
    def set_custom_ff(self):
        # Проверка кастомной функции на комплексность и выполнимость
        try:
            expr = str(self.fitness_input.text())

            def test_func(x, y):
                return eval(expr)

            x1, x2, y1, y2 = pso.ranges.values()
            for _ in range(10):
                a = randint(x1, x2)
                b = randint(y1, y2)
                if isinstance(test_func(a, b), complex):
                    common.input_error('Введена комплексная функция')
                    print('complex at ', a, b)
                    return 0
            pso.fitness_function = lambda x, y: test_func(x, y)
            return 1
        except ZeroDivisionError:
            common.input_error('Ошибка, деление на 0')
            return 0
        except SyntaxError:
            common.input_error('Некорректная функция')
            return 0
        except NameError:
            common.input_error('Использована недоступная функция')
            return 0
        except TypeError:
            common.input_error('Неправильный синтаксис')
            return 0
        except ValueError:
            common.input_error('Некорректная функция')
            return 0

    # Установка параметров из полей ввода
    def set_params(self):
        # Получение параметров из полей ввода с проверкой
        try:
            num_of_particles = int(self.num_of_particles_input.text())
            omega = float(self.omega_input.text())
            phi_p = float(self.phi_p_input.text())
            phi_g = float(self.phi_g_input.text())
        except ValueError:
            common.input_error('Проверьте правильность введенных параметров')
            return 0
        # Присвоение параметров
        try:
            pso.set_args(num_of_particles, omega, phi_p, phi_g)
            return 1
        except ValueError as error:
            common.input_error(str(error))
            return 0

# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
