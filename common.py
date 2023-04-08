# Общие объекты и методы
from PyQt5.QtGui import QIcon, QFont, QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QMessageBox

# Сообщение об ошибке
def input_error(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Неверно введены данные')
    msg.setInformativeText(text)
    msg.setWindowTitle('Ошибка')
    msg.setWindowIcon(QIcon('warning.png'))
    msg.exec()


# Информационное окно
def info(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText('Сведения о работе программы:')
    msg.setInformativeText(text)
    msg.setWindowTitle('Сведения')
    msg.setWindowIcon(QIcon('info.png'))
    msg.exec()

# Основной шрифт, валидаторы проверяющие тип ввода
f = QFont("Times", 10)
only_int = QIntValidator()
only_float = QDoubleValidator()
only_float.setNotation(QDoubleValidator.StandardNotation)
only_float.setRange(float(0), float(2), 6)

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']