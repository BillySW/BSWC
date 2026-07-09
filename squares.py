# squares.py - ПРОВЕРЯЕМ ЧТО МЕТОД set() ЕСТЬ
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QFont
from db import save_status, save_food

class BaseSquare(QPushButton):
    """Базовый класс для всех квадратов с общей логикой"""
    def __init__(self, elem, mid, states, save_func):
        super().__init__()
        self.elem = elem
        self.mid = mid
        self.state = 0
        self.locked = False
        self.states = states
        self.save_func = save_func

        self.setFixedSize(50, 50)
        self.setStyleSheet("border:1px solid #555;background:transparent;")
        self.clicked.connect(self.click)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right)

    def set(self, state, locked=False):
        """Установить состояние квадрата - ОСНОВНОЙ МЕТОД"""
        self.state = state
        self.locked = locked
        self.update()

    def click(self):
        """Обработка левого клика - циклическое переключение"""
        if self.locked:
            return
        self.state = (self.state + 1) % len(self.states)
        self.save_func(self.mid, self.elem, self.state, self.locked)
        self.update()

    def right(self, pos):
        """Обработка правого клика - переключение locked"""
        self.locked = not self.locked
        self.save_func(self.mid, self.elem, self.state, self.locked)
        self.update()

    def paintEvent(self, e):
        """Отрисовка квадрата"""
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Отрисовка фона
        color, text = self.states[self.state]
        if color:
            p.setBrush(QColor(color))
            p.setPen(Qt.NoPen)
            p.drawRect(0, 0, 50, 50)

        # Отрисовка текста
        if text:
            p.setPen(QColor("#fff"))
            p.setFont(QFont("Arial", 6 if len(text) > 3 else 7, QFont.Bold))
            p.drawText(self.rect(), Qt.AlignCenter, text)

        # Иконка элемента если состояние 0
        icons = {'water': '💧', 'fire': '🔥', 'wind': '🍃', 'light': '✨', 'dark': '🌑'}
        if self.state == 0:
            p.setPen(QColor("#888"))
            p.setFont(QFont("Segoe UI Emoji", 14))
            p.drawText(self.rect(), Qt.AlignCenter, icons[self.elem])

        # Замок если locked
        if self.locked:
            p.setPen(QColor("#f39c12"))
            p.setFont(QFont("Segoe UI Emoji", 10))
            p.drawText(32, 0, 18, 16, Qt.AlignCenter, '🔒')

class ElementSquare(BaseSquare):
    """Квадрат для вкладки TirList"""
    STATES = [
        ("", ""),                    # 0 - пусто
        ("#1a1a1a", "FOOD"),        # 1 - FOOD
        ("#c0392b", "GOOD"),        # 2 - GOOD
        ("#1abc9c", "HAVE")         # 3 - HAVE
    ]

    def __init__(self, elem, mid):
        super().__init__(elem, mid, self.STATES, save_status)

class FoodSquare(BaseSquare):
    """Квадрат для вкладки FoodList"""
    STATES = [
        ("", ""),                    # 0 - пусто
        ("#c0392b", "FOOD"),        # 1 - FOOD
        ("#27ae60", "WAIT"),        # 2 - WAIT
        ("#2ecc71", "W+HEX"),       # 3 - W+HEX
        ("#2ecc71", "W+H2"),        # 4 - W+H2
        ("#2ecc71", "W+H3"),        # 5 - W+H3
        ("#f1c40f", "HEX"),         # 6 - HEX
        ("#f1c40f", "HX2"),         # 7 - HX2
        ("#f1c40f", "HX3")          # 8 - HX3
    ]

    def __init__(self, elem, mid):
        super().__init__(elem, mid, self.STATES, save_food)
