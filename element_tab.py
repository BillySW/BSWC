# element_tab.py
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QComboBox, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor, QIcon
from db import get_element_monsters, get_element_status, save_element_data
from config import HAVE_DIR, RUNES, RUNE_STATS, get_awakened_name
from base_list import BaseList


class StarButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(18, 18)
        self.setCheckable(True)
        self.setText("☆")
        self.setStyleSheet("""
            QPushButton { color: #555; font-size: 14px; border: none; background: transparent; padding: 0px; margin: 0px; }
            QPushButton:checked { color: #a855f7; }
            QPushButton:hover { color: #c084fc; }
        """)
    def setChecked(self, checked):
        super().setChecked(checked)
        self.setText("★" if checked else "☆")


class RuneComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(55)
        self.setFixedHeight(24)
        self.setStyleSheet("""
            QComboBox { background: #3d3d3d; color: #fff; font-size: 9px; padding: 2px; border: 1px solid #555; border-radius: 3px; }
            QComboBox::drop-down { border: none; width: 15px; }
            QComboBox QAbstractItemView { background: #3d3d3d; color: #fff; selection-background-color: #4a7aca; }
            QComboBox::item { height: 30px; padding: 2px; }
        """)
        self.load_runes()
    def load_runes(self):
        runes_dir = os.path.join(os.path.dirname(__file__), "runes")
        self.addItem("")
        for rune in RUNES:
            if rune:
                icon_path = os.path.join(runes_dir, f"{rune}.png")
                if os.path.exists(icon_path):
                    pix = QPixmap(icon_path)
                    if not pix.isNull():
                        pix = pix.scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.addItem(QIcon(pix), rune)
                        continue
                self.addItem(rune)


class ElementCard(QFrame):
    def __init__(self, mon, element):
        super().__init__()
        self.mid = mon[0]
        self.name_en = mon[1]
        self.element = element
        data = get_element_status(self.mid, element)

        self.setStyleSheet("""
            QFrame { background: #2a2a2a; border-radius: 8px; border: 1px solid #3d3d3d; }
            QFrame:hover { border: 1px solid #4a7aca; }
        """)
        self.setFixedSize(320, 205)
        main_lay = QVBoxLayout(self)
        main_lay.setSpacing(2)
        main_lay.setContentsMargins(8, 5, 8, 5)

        # === Строка 1: Имя + Звезды ===
        row1 = QHBoxLayout()
        row1.setSpacing(2)
        awakened_name = get_awakened_name(self.name_en, self.element)
        name_text = data.get("custom_name", awakened_name)
        self.name_label = QLabel(name_text)
        self.name_label.setStyleSheet("font-size:13px;font-weight:bold;color:#fff;background:transparent;")
        self.name_label.setFixedHeight(20)
        row1.addWidget(self.name_label)
        row1.addStretch()
        for _ in range(4):
            lbl = QLabel("★")
            lbl.setStyleSheet("color:#a855f7;font-size:14px;background:transparent;")
            row1.addWidget(lbl)
        self.star5 = StarButton()
        self.star5.setChecked(data.get("star5", False))
        self.star5.clicked.connect(self.on_star5_click)
        row1.addWidget(self.star5)
        self.star6 = StarButton()
        self.star6.setChecked(data.get("star6", False))
        self.star6.clicked.connect(self.on_star6_click)
        row1.addWidget(self.star6)
        main_lay.addLayout(row1)

        # === Строка 2: Картинка + Кнопки + Слоты ===
        row2 = QHBoxLayout()
        row2.setSpacing(6)
        row2.setAlignment(Qt.AlignTop)

        img = QLabel()
        img.setFixedSize(100, 100)
        img.setAlignment(Qt.AlignCenter)
        img_path = os.path.join(HAVE_DIR, f"have_{self.element}", f"{self.name_en}.png")
        pix = QPixmap(img_path)
        if pix.isNull():
            pix = QPixmap(100, 100); pix.fill(QColor("#444"))
        else:
            pix = pix.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img.setPixmap(pix)
        row2.addWidget(img)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(1)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(4)
        self.aw_btn = QPushButton()
        self.aw_btn.setFixedSize(50, 22)
        self.update_aw_btn(data.get("awakening", ""))
        self.aw_btn.clicked.connect(self.cycle_awakening)
        btn_layout.addWidget(self.aw_btn)
        self.sk_btn = QPushButton()
        self.sk_btn.setFixedSize(50, 22)
        self.update_sk_btn(data.get("skills", ""))
        self.sk_btn.clicked.connect(self.toggle_skills)
        btn_layout.addWidget(self.sk_btn)
        self.art_btn = QPushButton()
        self.art_btn.setFixedSize(50, 22)
        self.update_art_btn(data.get("artifacts", ""))
        self.art_btn.clicked.connect(self.toggle_artifacts)
        btn_layout.addWidget(self.art_btn)
        btn_layout.addStretch()
        right_layout.addLayout(btn_layout)

        nums_layout = QHBoxLayout()
        nums_layout.setSpacing(0)
        for slot_num in [2, 4, 6]:
            lbl = QLabel(str(slot_num))
            lbl.setStyleSheet("color:#888;font-size:11px;font-weight:bold;background:transparent;")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedWidth(55)
            nums_layout.addWidget(lbl)
            if slot_num != 6: nums_layout.addSpacing(4)
        nums_layout.addStretch()
        right_layout.addLayout(nums_layout)

        self.slot2_rune = RuneComboBox()
        self.slot4_rune = RuneComboBox()
        self.slot6_rune = RuneComboBox()
        runes_layout = QHBoxLayout()
        runes_layout.setSpacing(0)
        for cb, slot_num in [(self.slot2_rune, 2), (self.slot4_rune, 4), (self.slot6_rune, 6)]:
            cb.setCurrentText(data.get(f"slot{slot_num}_rune", ""))
            runes_layout.addWidget(cb)
            if slot_num != 6: runes_layout.addSpacing(4)
        runes_layout.addStretch()
        right_layout.addLayout(runes_layout)

        self.slot2_stat = QComboBox()
        self.slot4_stat = QComboBox()
        self.slot6_stat = QComboBox()
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(0)
        for cb, slot_num in [(self.slot2_stat, 2), (self.slot4_stat, 4), (self.slot6_stat, 6)]:
            cb.addItems(RUNE_STATS)
            cb.setFixedWidth(55)
            cb.setFixedHeight(24)
            cb.setStyleSheet("background:#3d3d3d;color:#fff;font-size:8px;padding:2px;border:1px solid #555;border-radius:3px;")
            cb.setCurrentText(data.get(f"slot{slot_num}", ""))
            stats_layout.addWidget(cb)
            if slot_num != 6: stats_layout.addSpacing(4)
        stats_layout.addStretch()
        right_layout.addLayout(stats_layout)

        row2.addLayout(right_layout)
        main_lay.addLayout(row2)

        # === Строка 3: Три руны под картинкой ===
        self.rune1_cb = RuneComboBox()
        self.rune2_cb = RuneComboBox()
        self.rune3_cb = RuneComboBox()
        self.rune1_cb.setCurrentText(data.get("rune1", ""))
        self.rune2_cb.setCurrentText(data.get("rune2", ""))
        self.rune3_cb.setCurrentText(data.get("rune3", ""))

        row3 = QHBoxLayout()
        row3.setSpacing(4)
        row3.setAlignment(Qt.AlignLeft)
        row3.addSpacing(104)
        row3.addWidget(self.rune1_cb)
        row3.addWidget(self.rune2_cb)
        row3.addWidget(self.rune3_cb)
        row3.addStretch()
        main_lay.addLayout(row3)

        # Подключаем сигналы ПОСЛЕ загрузки значений из БД
        self._saving = False
        for cb in [self.slot2_rune, self.slot4_rune, self.slot6_rune,
                   self.slot2_stat, self.slot4_stat, self.slot6_stat,
                   self.rune1_cb, self.rune2_cb, self.rune3_cb]:
            cb.currentTextChanged.connect(self.save_data)

    def on_star5_click(self):
        checked = self.star5.isChecked()
        self.star5.setChecked(checked)
        if not checked: self.star6.setChecked(False)
        data = get_element_status(self.mid, self.element)
        data["star5"] = checked
        data["star6"] = self.star6.isChecked()
        save_element_data(self.mid, self.element, data)

    def on_star6_click(self):
        checked = self.star6.isChecked()
        self.star6.setChecked(checked)
        if checked: self.star5.setChecked(True)
        data = get_element_status(self.mid, self.element)
        data["star5"] = self.star5.isChecked()
        data["star6"] = checked
        save_element_data(self.mid, self.element, data)

    def update_aw_btn(self, state):
        colors = {"": "#555", "no": "#e74c3c", "yes": "#1abc9c"}
        self.aw_btn.setText("2A")
        self.aw_btn.setStyleSheet(f"background:{colors.get(state,'#555')};color:#fff;font-size:8px;font-weight:bold;border:none;border-radius:3px;padding:0 4px;")

    def update_sk_btn(self, state):
        color = "#1abc9c" if state == "yes" else "#e74c3c"
        self.sk_btn.setText("Sk")
        self.sk_btn.setStyleSheet(f"background:{color};color:#fff;font-size:8px;font-weight:bold;border:none;border-radius:3px;padding:0 4px;")

    def update_art_btn(self, state):
        color = "#1abc9c" if state == "yes" else "#e74c3c"
        self.art_btn.setText("Art")
        self.art_btn.setStyleSheet(f"background:{color};color:#fff;font-size:8px;font-weight:bold;border:none;border-radius:3px;padding:0 4px;")

    def cycle_awakening(self):
        data = get_element_status(self.mid, self.element)
        states = {"": "no", "no": "yes", "yes": ""}
        data["awakening"] = states.get(data.get("awakening", ""), "no")
        self.update_aw_btn(data["awakening"])
        save_element_data(self.mid, self.element, data)

    def toggle_skills(self):
        data = get_element_status(self.mid, self.element)
        data["skills"] = "" if data.get("skills") == "yes" else "yes"
        self.update_sk_btn(data["skills"])
        save_element_data(self.mid, self.element, data)

    def toggle_artifacts(self):
        data = get_element_status(self.mid, self.element)
        data["artifacts"] = "" if data.get("artifacts") == "yes" else "yes"
        self.update_art_btn(data["artifacts"])
        save_element_data(self.mid, self.element, data)

    def save_data(self):
        if self._saving:
            return
        self._saving = True
        try:
            data = get_element_status(self.mid, self.element)
            data.update({
                "custom_name": self.name_label.text(),
                "slot2_rune": self.slot2_rune.currentText(),
                "slot4_rune": self.slot4_rune.currentText(),
                "slot6_rune": self.slot6_rune.currentText(),
                "slot2": self.slot2_stat.currentText(),
                "slot4": self.slot4_stat.currentText(),
                "slot6": self.slot6_stat.currentText(),
                "rune1": self.rune1_cb.currentText(),
                "rune2": self.rune2_cb.currentText(),
                "rune3": self.rune3_cb.currentText(),
                "star5": self.star5.isChecked(),
                "star6": self.star6.isChecked(),
            })
            save_element_data(self.mid, self.element, data)
        finally:
            self._saving = False


class ElementTab(BaseList):
    def __init__(self, element):
        super().__init__()
        self.element = element
        self.layout.setSpacing(4)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setAlignment(Qt.AlignTop)

    def refresh(self):
        self.clear()
        mons = get_element_monsters(self.element)
        if not mons:
            lbl = QLabel(f"No monsters marked as HAVE for {self.element.capitalize()}")
            lbl.setStyleSheet("color:#888;font-size:14px;")
            lbl.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(lbl)
            return
        row_widget = None
        row_layout = None
        cards_in_row = 0
        for mon in mons:
            if row_widget is None:
                row_widget = QWidget()
                row_widget.setStyleSheet("background:transparent;")
                row_layout = QHBoxLayout(row_widget)
                row_layout.setSpacing(4)
                row_layout.setContentsMargins(0, 0, 0, 0)
                row_layout.setAlignment(Qt.AlignLeft)
                self.layout.addWidget(row_widget)
            row_layout.addWidget(ElementCard(mon, self.element))
            cards_in_row += 1
            if cards_in_row >= 3:
                row_widget = None
                cards_in_row = 0
        self.layout.addStretch()
