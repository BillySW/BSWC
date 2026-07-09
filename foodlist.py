# foodlist.py - ПОЛНАЯ ВЕРСИЯ
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor
from db import get_monsters_food, get_food
from squares import FoodSquare
from config import FL_DIR, ELEMENTS
from base_list import BaseList

class FoodCard(QFrame):
    def __init__(self, mon):
        super().__init__()
        self.mid, self.name = mon[0], mon[1]
        self.setStyleSheet("background:#2a2a2a; border-radius:5px;")
        self.setFixedSize(110, 300)

        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setAlignment(Qt.AlignCenter)

        # Имя
        nm = QLabel(self.name[:14])
        nm.setAlignment(Qt.AlignCenter)
        nm.setStyleSheet("font-size:8px;color:#ccc;background:transparent;padding:2px 0;")
        nm.setWordWrap(True)
        nm.setFixedHeight(30)
        lay.addWidget(nm)

        # Ряд с картинками и квадратами
        row = QHBoxLayout()
        row.setSpacing(0)

        pics = QVBoxLayout()
        pics.setSpacing(0)

        squares = QVBoxLayout()
        squares.setSpacing(0)

        states, locks = get_food(self.mid)

        for i, el in enumerate(ELEMENTS):
            # Картинка
            img = QLabel()
            img.setFixedSize(50, 50)
            img_path = os.path.join(FL_DIR, f"{self.name}_{el}.png")
            pix = QPixmap(img_path)
            if pix.isNull():
                pix = QPixmap(50, 50)
                pix.fill(QColor("#666"))
            else:
                pix = pix.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            img.setPixmap(pix)
            pics.addWidget(img)

            # Квадрат состояния
            sq = FoodSquare(el, self.mid)
            sq.set(states[i], bool(locks[i]))
            squares.addWidget(sq)

        row.addLayout(pics)
        row.addLayout(squares)
        lay.addLayout(row)

class FoodList(BaseList):
    def __init__(self):
        super().__init__()

    def refresh(self):
        self.clear()

        mons = get_monsters_food()
        if not mons:
            lbl = QLabel("No monsters found. Sync with mobs.txt in Options")
            lbl.setStyleSheet("color:#888;font-size:14px;")
            lbl.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(lbl)
            return

        cur_update = None
        row_widget = None
        row_layout = None

        for mon in mons:
            update = mon[3]

            if update != cur_update:
                cur_update = update
                row_widget = None
                lbl = QLabel(f"  {update}")
                lbl.setStyleSheet("color:#f1c40f;font-size:11px;font-weight:bold;background:transparent;padding:8px 4px;")
                self.layout.addWidget(lbl)

            if row_widget is None:
                row_widget = QWidget()
                row_widget.setStyleSheet("background:transparent;")
                row_layout = QHBoxLayout(row_widget)
                row_layout.setSpacing(0)
                row_layout.setContentsMargins(0, 0, 0, 0)
                row_layout.setAlignment(Qt.AlignLeft)
                self.layout.addWidget(row_widget)

            row_layout.addWidget(FoodCard(mon))

            if row_layout.count() >= 9:
                row_widget = None
