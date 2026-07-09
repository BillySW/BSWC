# main.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt
from tirlist import TirList
from foodlist import FoodList
from options import Options
from element_tab import ElementTab
from search import SearchTab
from db import sync_txt, init_db

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BSWC - Billy's Summoners War Collector")
        self.setFixedSize(1024, 768)

        # Главный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Поисковая строка
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(10, 5, 10, 5)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search monsters... (Ctrl+F)")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: #3d3d3d;
                color: #fff;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #4a7aca;
            }
        """)
        self.search_input.textChanged.connect(self.on_search)
        search_layout.addWidget(self.search_input)

        # Кнопка сброса поиска
        clear_btn = QPushButton("✕")
        clear_btn.setFixedSize(30, 30)
        clear_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #888;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #fff;
            }
        """)
        clear_btn.clicked.connect(lambda: self.search_input.clear())
        search_layout.addWidget(clear_btn)

        main_layout.addLayout(search_layout)

        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                background: #2d2d2d;
                border: none;
            }
        """)

        # Инициализация вкладок
        self.tir = TirList()
        self.food = FoodList()
        self.tab_water = ElementTab("water")
        self.tab_fire = ElementTab("fire")
        self.tab_wind = ElementTab("wind")
        self.tab_light = ElementTab("light")
        self.tab_dark = ElementTab("dark")
        self.search_tab = SearchTab()
        self.opt = Options(self)

        # Список вкладок
        tabs = [
            (self.tir, "📊 TirList"),
            (self.food, "🍖 FoodList"),
            (self.tab_water, "💧 Water"),
            (self.tab_fire, "🔥 Fire"),
            (self.tab_wind, "🍃 Wind"),
            (self.tab_light, "✨ Light"),
            (self.tab_dark, "🌑 Dark"),
            (self.search_tab, "🔍 Search"),
            (self.opt, "⚙️ Options"),
        ]

        for w, n in tabs:
            w.setStyleSheet("background:#2d2d2d;")
            self.tabs.addTab(w, n)

        main_layout.addWidget(self.tabs)

        # Перехват нажатий клавиш
        self.tabs.keyPressEvent = self.key_press

    def key_press(self, e):
        """Обработка нажатий клавиш"""
        current = self.tabs.currentWidget()

        # Стрелки для навигации по вкладкам
        if e.key() == Qt.Key_Left:
            i = self.tabs.currentIndex()
            self.tabs.setCurrentIndex((i - 1) % self.tabs.count())
        elif e.key() == Qt.Key_Right:
            i = self.tabs.currentIndex()
            self.tabs.setCurrentIndex((i + 1) % self.tabs.count())

        # Стрелки для скролла
        elif e.key() == Qt.Key_Up:
            if hasattr(current, 'scroll') and current.scroll:
                bar = current.scroll.verticalScrollBar()
                bar.setValue(bar.value() - 50)
        elif e.key() == Qt.Key_Down:
            if hasattr(current, 'scroll') and current.scroll:
                bar = current.scroll.verticalScrollBar()
                bar.setValue(bar.value() + 50)

        # Цифры для быстрого переключения (1-9)
        elif e.key() >= Qt.Key_1 and e.key() <= Qt.Key_9:
            idx = e.key() - Qt.Key_1
            if idx < self.tabs.count():
                self.tabs.setCurrentIndex(idx)

        # Ctrl+F для поиска
        elif e.key() == Qt.Key_F and e.modifiers() & Qt.ControlModifier:
            self.tabs.setCurrentIndex(7)  # Вкладка поиска
            self.search_tab.search_input.setFocus()
            self.search_tab.search_input.selectAll()

        else:
            QTabWidget.keyPressEvent(self.tabs, e)

    def on_search(self, text):
        """Обработка поиска из главной строки"""
        if text.strip():
            self.tabs.setCurrentIndex(7)  # Переключаемся на поиск
            self.search_tab.search_input.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QMainWindow {
            background: #1e1e1e;
        }
        QTabWidget::pane {
            background: #2d2d2d;
            border: 1px solid #3d3d3d;
        }
        QTabBar::tab {
            background: #3d3d3d;
            color: #aaa;
            padding: 10px 20px;
            font-size: 13px;
            margin: 1px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
        QTabBar::tab:selected {
            background: #4a7aca;
            color: #fff;
        }
        QTabBar::tab:hover:!selected {
            background: #4d4d4d;
            color: #fff;
        }
        QScrollBar:vertical {
            background: #2d2d2d;
            width: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background: #4a7aca;
            border-radius: 6px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background: #5a8ada;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
    """)

    # Инициализация БД
    if not os.path.exists("swtracker.db"):
        init_db()

    # Синхронизация с mobs.txt
    if os.path.exists("mobs.txt"):
        sync_txt("mobs.txt")

    # Создаем окно
    w = MainWindow()

    # Обновляем все вкладки
    w.tir.refresh()
    w.food.refresh()
    w.tab_water.refresh()
    w.tab_fire.refresh()
    w.tab_wind.refresh()
    w.tab_light.refresh()
    w.tab_dark.refresh()

    w.show()
    sys.exit(app.exec())
