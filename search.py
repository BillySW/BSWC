# search.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QFrame
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPixmap
from db import get_all_monsters, get_status
from squares import ElementSquare
from config import TL_DIR, COLLAB_MONSTERS, ELEMENTS

class SearchResultCard(QFrame):
    """Карточка результата поиска"""
    def __init__(self, mon, search_text):
        super().__init__()
        self.mid = mon[0]
        self.name = mon[1]
        self.stars = mon[2]

        self.setStyleSheet("""
            QFrame {
                background: #2a2a2a;
                border-radius: 8px;
            }
            QFrame:hover {
                background: #333333;
            }
        """)
        self.setFixedHeight(80)

        lay = QHBoxLayout(self)
        lay.setSpacing(10)
        lay.setContentsMargins(10, 5, 10, 5)

        # Звезды
        stars_lbl = QLabel("⭐" * min(self.stars, 6))
        stars_lbl.setStyleSheet("color:#f1c40f;font-size:14px;")
        lay.addWidget(stars_lbl)

        # Имя (с подсветкой поиска)
        name_lbl = QLabel()
        if search_text.lower() in self.name.lower():
            # Подсветка найденного текста
            text = self.name
            idx = text.lower().find(search_text.lower())
            highlighted = f"{text[:idx]}<span style='color:#4a7aca;font-weight:bold;'>{text[idx:idx+len(search_text)]}</span>{text[idx+len(search_text):]}"
            name_lbl.setText(highlighted)
            name_lbl.setStyleSheet("font-size:14px;font-weight:bold;color:#fff;")
        else:
            name_lbl.setText(self.name)
            name_lbl.setStyleSheet("font-size:14px;color:#fff;")
        lay.addWidget(name_lbl)

        lay.addStretch()

        # Элементальные квадраты
        states, locks = get_status(self.mid)
        flags = COLLAB_MONSTERS.get(self.name, [1, 1, 1, 1, 1])

        for j, el in enumerate(ELEMENTS):
            if flags[j]:
                sq = ElementSquare(el, self.mid)
                sq.set(states[j], bool(locks[j]))
                sq.setFixedSize(40, 40)
                lay.addWidget(sq)

class SearchTab(QWidget):
    """Вкладка с результатами поиска"""
    def __init__(self):
        super().__init__()
        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(0, 0, 0, 0)

        # Строка поиска
        search_row = QHBoxLayout()
        search_row.setContentsMargins(10, 10, 10, 10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search monsters... (Ctrl+F to focus)")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: #3d3d3d;
                color: #fff;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #4a7aca;
            }
        """)
        self.search_input.textChanged.connect(self.search)
        search_row.addWidget(self.search_input)

        clear_btn = QPushButton("✕")
        clear_btn.setFixedSize(30, 30)
        clear_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #888;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                color: #fff;
            }
        """)
        clear_btn.clicked.connect(lambda: self.search_input.clear())
        search_row.addWidget(clear_btn)

        main_lay.addLayout(search_row)

        # Результаты
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border:none;background:#1e1e1e;")

        self.content = QWidget()
        self.content.setStyleSheet("background:#1e1e1e;")
        self.layout = QVBoxLayout(self.content)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.content)
        main_lay.addWidget(self.scroll)

        # Таймер для задержки поиска
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.do_search)

        # Все монстры
        self.all_monsters = get_all_monsters()

        # Показываем приветствие
        self.show_welcome()

    def show_welcome(self):
        """Показать приветственное сообщение"""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        lbl = QLabel("🔍 Type to search monsters...\n\n"
                    "Tips:\n"
                    "• Search by name\n"
                    "• Results are highlighted\n"
                    "• Click squares to update status")
        lbl.setStyleSheet("color:#888;font-size:14px;padding:20px;")
        lbl.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(lbl)

    def search(self, text):
        """Запуск поиска с задержкой"""
        self.timer.start(300)  # Задержка 300ms

    def do_search(self):
        """Выполнение поиска"""
        text = self.search_input.text().strip()

        # Очищаем результаты
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not text:
            self.show_welcome()
            return

        # Ищем монстров
        results = []
        for mon in self.all_monsters:
            name = mon[1]
            if text.lower() in name.lower():
                results.append(mon)

        if not results:
            lbl = QLabel(f"❌ No monsters found for '{text}'")
            lbl.setStyleSheet("color:#e74c3c;font-size:14px;padding:20px;")
            lbl.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(lbl)
            return

        # Показываем результаты
        results_label = QLabel(f"Found {len(results)} monster(s) for '{text}':")
        results_label.setStyleSheet("color:#aaa;font-size:12px;padding:5px;")
        self.layout.addWidget(results_label)

        for mon in results:
            self.layout.addWidget(SearchResultCard(mon, text))
