# tirlist.py - ПОЛНАЯ ВЕРСИЯ
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor
from db import get_monsters, get_status
from squares import ElementSquare
from config import TL_DIR, COLLAB_MONSTERS, ELEMENTS
from base_list import BaseList

class TirCard(QFrame):
    def __init__(self, mon):
        super().__init__()
        self.mid, self.name, self.stars = mon[0], mon[1], mon[2]
        self.setStyleSheet("background:#2a2a2a; border-radius:5px;")
        self.setFixedSize(62, 310)

        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setAlignment(Qt.AlignTop)

        # Имя монстра
        nm = QLabel(self.name[:12])
        nm.setAlignment(Qt.AlignCenter)
        nm.setStyleSheet("font-size:8px;color:#ccc;background:transparent;padding:2px 0;")
        nm.setWordWrap(True)
        nm.setFixedHeight(30)
        lay.addWidget(nm)

        # Картинка монстра
        img = QLabel()
        img.setFixedSize(50, 50)
        img_path = os.path.join(TL_DIR, f"{self.name}.png")
        pix = QPixmap(img_path)
        if pix.isNull():
            pix = QPixmap(50, 50)
            pix.fill(QColor("#444"))
        else:
            pix = pix.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img.setPixmap(pix)

        hh = QHBoxLayout()
        hh.addStretch()
        hh.addWidget(img)
        hh.addStretch()
        lay.addLayout(hh)

        # Получаем статусы
        states, locks = get_status(self.mid)

        # Определяем доступные элементы для этого монстра
        flags = COLLAB_MONSTERS.get(self.name, [1, 1, 1, 1, 1])

        # Добавляем квадраты для каждого элемента
        for j, el in enumerate(ELEMENTS):
            if flags[j]:
                sq = ElementSquare(el, self.mid)
                sq.set(states[j], bool(locks[j]))
                h = QHBoxLayout()
                h.addStretch()
                h.addWidget(sq)
                h.addStretch()
                lay.addLayout(h)
            else:
                # Для недоступных элементов добавляем пустой квадрат
                spacer = QLabel()
                spacer.setFixedSize(50, 50)
                spacer.setStyleSheet("background:transparent;")
                h = QHBoxLayout()
                h.addStretch()
                h.addWidget(spacer)
                h.addStretch()
                lay.addLayout(h)

        # Добавляем растяжку внизу
        lay.addStretch()

class TirList(BaseList):
    def __init__(self):
        super().__init__()
        self.layout.setSpacing(2)

    def refresh(self):
        self.clear()

        mons = get_monsters()
        if not mons:
            lbl = QLabel("No monsters found. Sync with mobs.txt in Options")
            lbl.setStyleSheet("color:#888;font-size:14px;")
            lbl.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(lbl)
            return

        # Группируем по звездам от 2 до 5
        stars_groups = {2: [], 3: [], 4: [], 5: []}
        for mon in mons:
            stars = mon[2]
            if stars in stars_groups:
                stars_groups[stars].append(mon)
            else:
                stars_groups[3].append(mon)

        # Проходим по звездам от 2 до 5
        for stars in [2, 3, 4, 5]:
            group = stars_groups.get(stars, [])
            if not group:
                continue

            # Заголовок звезд
            stars_text = "⭐" * stars
            stars_lbl = QLabel(stars_text)
            stars_lbl.setStyleSheet(f"color:#f1c40f;font-size:14px;font-weight:bold;background:transparent;padding:5px 10px;")
            self.layout.addWidget(stars_lbl)

            # Разбиваем на ряды по 14 карточек
            row_widget = None
            row_layout = None
            cards_in_row = 0

            for mon in group:
                if row_widget is None:
                    row_widget = QWidget()
                    row_widget.setStyleSheet("background:transparent;")
                    row_layout = QHBoxLayout(row_widget)
                    row_layout.setSpacing(2)
                    row_layout.setContentsMargins(2, 2, 2, 2)
                    row_layout.setAlignment(Qt.AlignLeft)
                    self.layout.addWidget(row_widget)

                row_layout.addWidget(TirCard(mon))
                cards_in_row += 1

                if cards_in_row >= 14:
                    row_widget = None
                    cards_in_row = 0

            # Отступ после группы
            spacer = QLabel()
            spacer.setFixedHeight(10)
            self.layout.addWidget(spacer)
