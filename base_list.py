# base_list.py - БАЗОВЫЙ КЛАСС ДЛЯ ВСЕХ СПИСКОВ
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt

class BaseList(QWidget):
    """Базовый класс для всех списков с прокруткой"""

    def __init__(self):
        super().__init__()
        self.scroll = None
        self.content = None
        self.layout = None
        self._setup_ui()

    def _setup_ui(self):
        """Настройка UI - скролл область и контент"""
        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("border:none;background:#1e1e1e;")

        self.content = QWidget()
        self.content.setStyleSheet("background:#1e1e1e;")
        self.layout = QVBoxLayout(self.content)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.content)
        main_lay.addWidget(self.scroll)

    def clear(self):
        """Очистка всех виджетов в списке"""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()

    def refresh(self):
        """Метод для переопределения в наследниках"""
        self.clear()
        self._load_data()

    def _load_data(self):
        """Загрузка данных - переопределяется в наследниках"""
        pass

    def scroll_to_top(self):
        """Прокрутка вверх"""
        if self.scroll and self.scroll.verticalScrollBar():
            self.scroll.verticalScrollBar().setValue(0)

    def scroll_to_bottom(self):
        """Прокрутка вниз"""
        if self.scroll and self.scroll.verticalScrollBar():
            self.scroll.verticalScrollBar().setValue(
                self.scroll.verticalScrollBar().maximum()
            )
