# hex_tab.py - КОМПАКТНАЯ ВЕРСИЯ: 5★ по 2, 4★ по 3 в ряд
import os
import re
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QPen
from config import FL_DIR
from base_list import BaseList
from db import get_hex_state, save_hex_state


def parse_hex_file(filepath):
    """Парсинг hex.txt"""
    if not os.path.exists(filepath):
        print(f"Файл {filepath} не найден!")
        return {'5star': [], '4star': []}

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    recipes = {'5star': [], '4star': []}
    full_lines = []
    current_line = ""

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if ':' in stripped and not re.match(r'^\d', stripped):
            if current_line:
                full_lines.append(current_line)
            current_line = stripped
        else:
            if current_line:
                current_line += " " + stripped

    if current_line:
        full_lines.append(current_line)

    for line in full_lines:
        has_subs = bool(re.search(r'\b(1[1-4]|2[1-4]|3[1-4]|4[1-4])\b', line))
        recipe = parse_recipe_line(line)
        if recipe:
            if has_subs:
                recipes['5star'].append(recipe)
            else:
                recipes['4star'].append(recipe)

    return recipes


def parse_recipe_line(line):
    """Парсинг одной строки рецепта"""
    line = line.rstrip('.').strip()
    if ':' not in line:
        return None

    target_part, parts_str = line.split(':', 1)
    target_name, target_element = parse_element(target_part.strip())
    if not target_name:
        return None

    pattern = r'(\d+)\s+(.+?)\s*\((\w+)\)'
    matches = re.findall(pattern, parts_str)

    materials_dict = {}

    for num_str, name, element in matches:
        num = int(num_str)
        name = name.strip()
        element = element.lower()

        if 1 <= num <= 4:
            materials_dict[num] = {
                'name': name,
                'element': element,
                'sub_materials': []
            }
        elif 11 <= num <= 44:
            parent_num = num // 10
            if parent_num in materials_dict:
                materials_dict[parent_num]['sub_materials'].append({
                    'name': name,
                    'element': element
                })

    materials = [materials_dict[k] for k in sorted(materials_dict.keys())]

    return {
        'name': target_name,
        'element': target_element,
        'materials': materials
    }


def parse_element(name_str):
    """Извлечь имя и стихию"""
    match = re.match(r'^(.+?)\s*\((\w+)\)\s*$', name_str.strip())
    if match:
        name = match.group(1).strip()
        element = match.group(2).strip().lower()
        return name, element
    return name_str.strip(), 'unknown'


HEX_FILE = os.path.join(os.path.dirname(__file__), "hex.txt")
FUSION_RECIPES = parse_hex_file(HEX_FILE)


class HexMonsterImage(QLabel):
    """Кликабельная картинка монстра"""

    def __init__(self, name, element, recipe_name, size=42):
        super().__init__()
        self.name = name
        self.element = element
        self.recipe_name = recipe_name
        self.size = size

        self.state = get_hex_state(recipe_name, name, element)
        self._pixmap_original = None
        self._pixmap_marked = None
        self._pixmap_hidden = None

        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.PointingHandCursor)

        self._load_pixmaps()
        self._update_display()

    def _load_pixmaps(self):
        filename = f"{self.name}_{self.element}.png"
        path = os.path.join(FL_DIR, filename)
        pix = QPixmap(path)

        if pix.isNull():
            alt = f"{self.name.replace(' ', '_')}_{self.element}.png"
            pix = QPixmap(os.path.join(FL_DIR, alt))

        if not pix.isNull():
            pix = pix.scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            pix = QPixmap(self.size, self.size)
            pix.fill(QColor("#444"))

        self._pixmap_original = pix

        self._pixmap_marked = QPixmap(pix)
        painter = QPainter(self._pixmap_marked)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#1abc9c"))
        painter.setPen(QPen(QColor("#fff"), 1))
        mark_size = max(10, self.size // 4)
        painter.drawEllipse(self.size - mark_size - 2, 2, mark_size, mark_size)
        painter.setPen(QPen(QColor("#fff"), 1))
        painter.setFont(QFont("Arial", max(6, self.size // 6), QFont.Bold))
        painter.drawText(self.size - mark_size - 2, 2, mark_size, mark_size, Qt.AlignCenter, "✓")
        painter.end()

        self._pixmap_hidden = QPixmap(self.size, self.size)
        self._pixmap_hidden.fill(QColor("#333"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.state = (self.state + 1) % 3
            save_hex_state(self.recipe_name, self.name, self.element, self.state)
            self._update_display()
            if hasattr(self, 'parent_recipe') and self.parent_recipe:
                self.parent_recipe.check_completion()
        super().mousePressEvent(event)

    def _update_display(self):
        if self.state == 0:
            self.setPixmap(self._pixmap_original)
        elif self.state == 1:
            self.setPixmap(self._pixmap_marked)
        else:
            self.setPixmap(self._pixmap_hidden)

    def is_marked(self):
        return self.state == 1


class HexRecipeWidget(QFrame):
    """Компактный виджет рецепта"""

    def __init__(self, recipe_data, stars=5):
        super().__init__()
        self.recipe_data = recipe_data
        self.stars = stars
        self.target_name = recipe_data["name"]
        self.target_element = recipe_data["element"]
        self.materials = recipe_data.get("materials", [])
        self.recipe_name = f"{stars}_{self.target_name}_{self.target_element}"

        self.all_images = {}
        self.target_image = None

        border = "#f1c40f" if stars == 5 else "#e67e22"
        self.setStyleSheet(f"""
            QFrame {{ background: #2a2a2a; border-radius: 6px; border: 1px solid {border}; }}
        """)

        self._build_ui()
        self.check_completion()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(6, 4, 6, 4)

        # Компактный заголовок
        stars_text = "⭐" * self.stars
        title = QLabel(f"{stars_text} {self.target_name} ({self.target_element})")
        title.setStyleSheet("color:#fff;font-size:10px;font-weight:bold;background:transparent;")
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        main_layout.addWidget(title)

        # Картинка цели
        target_layout = QHBoxLayout()
        target_layout.setAlignment(Qt.AlignCenter)
        self.target_image = HexMonsterImage(
            self.target_name, self.target_element, self.recipe_name, 44
        )
        self.target_image.parent_recipe = self
        self.all_images["target"] = self.target_image
        target_layout.addWidget(self.target_image)
        main_layout.addLayout(target_layout)

        if not self.materials:
            return

        # Стрелка
        arrow = QLabel("▼")
        arrow.setStyleSheet("color:#888;font-size:9px;background:transparent;")
        arrow.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(arrow)

        # Материалы в ряд
        materials_row = QHBoxLayout()
        materials_row.setSpacing(4)
        materials_row.setAlignment(Qt.AlignCenter)

        for i, mat in enumerate(self.materials):
            col = self._build_material_column(mat, i)
            materials_row.addLayout(col)

        main_layout.addLayout(materials_row)

    def _build_material_column(self, mat_data, index):
        """Столбик: имя → картинка → под-материалы"""
        name = mat_data["name"]
        element = mat_data["element"]
        subs = mat_data.get("sub_materials", [])

        col = QVBoxLayout()
        col.setSpacing(1)
        col.setAlignment(Qt.AlignTop)

        # Имя (обрезанное)
        short = name[:10] if len(name) > 10 else name
        lbl = QLabel(short)
        lbl.setStyleSheet("color:#ccc;font-size:6px;background:transparent;")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setFixedWidth(55)
        col.addWidget(lbl)

        # Картинка материала
        img_size = 38 if self.stars == 5 else 42
        img = HexMonsterImage(name, element, self.recipe_name, img_size)
        img.parent_recipe = self
        self.all_images[f"mat{index}"] = img
        img_layout = QHBoxLayout()
        img_layout.setAlignment(Qt.AlignCenter)
        img_layout.addWidget(img)
        col.addLayout(img_layout)

        # Под-материалы
        if subs:
            for j, sub in enumerate(subs):
                sub_img = HexMonsterImage(sub["name"], sub["element"], self.recipe_name, 26)
                sub_img.parent_recipe = self
                self.all_images[f"sub{index}_{j}"] = sub_img
                sub_row = QHBoxLayout()
                sub_row.setAlignment(Qt.AlignCenter)
                sub_row.addWidget(sub_img)
                col.addLayout(sub_row)

        return col

    def check_completion(self):
        if not self.target_image:
            return

        all_obtained = all(
            img.is_marked()
            for key, img in self.all_images.items()
            if key != "target"
        )

        if all_obtained and self.target_image.state != 1:
            self.target_image.state = 1
            self.target_image._update_display()
            save_hex_state(self.recipe_name, self.target_name, self.target_element, 1)
        elif not all_obtained and self.target_image.state == 1:
            self.target_image.state = 0
            self.target_image._update_display()
            save_hex_state(self.recipe_name, self.target_name, self.target_element, 0)


class HexTab(BaseList):
    """Вкладка HEX"""

    def __init__(self):
        super().__init__()
        self.layout.setSpacing(6)
        self.layout.setContentsMargins(4, 4, 4, 4)

    def refresh(self):
        self.clear()

        # 5★ рецепты — по 2 в ряд
        if FUSION_RECIPES.get('5star'):
            lbl = QLabel("═══ 5★ FUSION ═══")
            lbl.setStyleSheet("color:#f1c40f;font-size:12px;font-weight:bold;background:transparent;padding:4px;")
            lbl.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(lbl)

            recipes = FUSION_RECIPES['5star']
            for i in range(0, len(recipes), 3):
                row = QWidget()
                row.setStyleSheet("background:transparent;")
                row_layout = QHBoxLayout(row)
                row_layout.setSpacing(6)
                row_layout.setAlignment(Qt.AlignLeft)

                for j in range(2):
                    if i + j < len(recipes):
                        row_layout.addWidget(HexRecipeWidget(recipes[i + j], stars=5))

                self.layout.addWidget(row)

        # 4★ рецепты — по 3 в ряд
        if FUSION_RECIPES.get('4star'):
            lbl = QLabel("═══ 4★ FUSION ═══")
            lbl.setStyleSheet("color:#e67e22;font-size:12px;font-weight:bold;background:transparent;padding:4px;")
            lbl.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(lbl)

            recipes = FUSION_RECIPES['4star']
            for i in range(0, len(recipes), 3):
                row = QWidget()
                row.setStyleSheet("background:transparent;")
                row_layout = QHBoxLayout(row)
                row_layout.setSpacing(6)
                row_layout.setAlignment(Qt.AlignLeft)

                for j in range(3):
                    if i + j < len(recipes):
                        row_layout.addWidget(HexRecipeWidget(recipes[i + j], stars=4))

                self.layout.addWidget(row)

        self.layout.addStretch()
