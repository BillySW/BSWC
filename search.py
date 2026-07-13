# search.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame
from PySide6.QtCore import Qt, QTimer
from db import get_all_monsters, get_status
from squares import ElementSquare
from config import COLLAB_MONSTERS, ELEMENTS


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

        stars_lbl = QLabel("⭐" * min(self.stars, 6))
        stars_lbl.setStyleSheet("color:#f1c40f;font-size:14px;")
        lay.addWidget(stars_lbl)

        name_lbl = QLabel()
        if search_text.lower() in self.name.lower():
            text = self.name
            idx = text.lower().find(search_text.lower())
            highlighted = (
                f"{text[:idx]}"
                f"<span style='color:#4a7aca;font-weight:bold;'>"
                f"{text[idx:idx + len(search_text)]}</span>"
                f"{text[idx + len(search_text):]}"
            )
            name_lbl.setText(highlighted)
            name_lbl.setStyleSheet("font-size:14px;font-weight:bold;color:#fff;")
        else:
            name_lbl.setText(self.name)
            name_lbl.setStyleSheet("font-size:14px;color:#fff;")
        lay.addWidget(name_lbl)

        lay.addStretch()

        states, locks = get_status(self.mid)
        flags = COLLAB_MONSTERS.get(self.name, [1, 1, 1, 1, 1])

        for j, el in enumerate(ELEMENTS):
            if flags[j]:
                sq = ElementSquare(el, self.mid)
                sq.set(states[j], bool(locks[j]))
                sq.setFixedSize(40, 40)
                lay.addWidget(sq)


class SearchTab(QWidget):
    """Вкладка с результатами поиска (строка ввода — в шапке окна)"""

    def __init__(self):
        super().__init__()
        self._query = ""

        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(0, 0, 0, 0)

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

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.do_search)

        self.all_monsters = get_all_monsters()
        self.show_welcome()

    def set_query(self, text):
        """Обновить запрос и перерисовать результаты (вызывается из MainWindow)."""
        self._query = text
        if text.strip():
            self.timer.start(300)
        else:
            self.timer.stop()
            self.show_welcome()

    def reload_monsters(self):
        """Перезагрузить список монстров после sync/import."""
        self.all_monsters = get_all_monsters()
        if self._query.strip():
            self.do_search()

    def show_welcome(self):
        self._clear_results()
        lbl = QLabel(
            "🔍 Use the search bar above to find monsters\n\n"
            "Tips:\n"
            "• Ctrl+F — focus search\n"
            "• Results update as you type\n"
            "• Click squares to update status"
        )
        lbl.setStyleSheet("color:#888;font-size:14px;padding:20px;")
        lbl.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(lbl)

    def _clear_results(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def do_search(self):
        text = self._query.strip()
        self._clear_results()

        if not text:
            self.show_welcome()
            return

        results = [mon for mon in self.all_monsters if text.lower() in mon[1].lower()]

        if not results:
            lbl = QLabel(f"❌ No monsters found for '{text}'")
            lbl.setStyleSheet("color:#e74c3c;font-size:14px;padding:20px;")
            lbl.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(lbl)
            return

        results_label = QLabel(f"Found {len(results)} monster(s) for '{text}':")
        results_label.setStyleSheet("color:#aaa;font-size:12px;padding:5px;")
        self.layout.addWidget(results_label)

        for mon in results:
            self.layout.addWidget(SearchResultCard(mon, text))
