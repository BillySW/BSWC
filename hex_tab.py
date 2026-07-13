# hex_tab.py - ВКЛАДКА HEX (ФЬЮЖН / СЛИЯНИЕ) С СОХРАНЕНИЕМ В БД
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QGridLayout
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QPen
from config import ELEMENTS, ELEMENT_ICONS, HL_DIR
from base_list import BaseList
from db import get_hex_state, save_hex_state  # <-- ИМПОРТ ИЗ db.py


# ============================================================
#  ВСЕ РЕЦЕПТЫ ФЬЮЖНА
# ============================================================

# 4★ базовые (фармятся в сценариях / данжах)
BASE_4STAR = {
    "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander", "Yeti"],
    "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander", "Yeti"],
    "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander", "Yeti"],
    "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander", "Yeti"],
    "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander", "Yeti"],
}

# 3★ базовые
BASE_3STAR = {
    "Fire": ["Harpy", "Elemental", "Fairy", "Golem", "Griffon", "High Elemental",
             "Imp Champion", "Inferno", "Living Armor", "Lizardman", "Mummy",
             "Serpent", "Taoist", "Viking", "Warbear", "Werewolf"],
    "Water": ["Harpy", "Elemental", "Fairy", "Golem", "Griffon", "High Elemental",
              "Imp Champion", "Inferno", "Living Armor", "Lizardman", "Mummy",
              "Serpent", "Taoist", "Viking", "Warbear", "Werewolf"],
    "Wind": ["Harpy", "Elemental", "Fairy", "Golem", "Griffon", "High Elemental",
             "Imp Champion", "Inferno", "Living Armor", "Lizardman", "Mummy",
             "Serpent", "Taoist", "Viking", "Warbear", "Werewolf"],
    "Light": ["Harpy", "Elemental", "Fairy", "Golem", "Griffon", "High Elemental",
              "Imp Champion", "Inferno", "Living Armor", "Lizardman", "Mummy",
              "Serpent", "Taoist", "Viking", "Warbear", "Werewolf"],
    "Dark": ["Harpy", "Elemental", "Fairy", "Golem", "Griffon", "High Elemental",
             "Imp Champion", "Inferno", "Living Armor", "Lizardman", "Mummy",
             "Serpent", "Taoist", "Viking", "Warbear", "Werewolf"],
}

# 2★ базовые
BASE_2STAR = {
    "Fire": ["Forest Keeper", "Ghost", "Harpu", "Howl", "Imp", "Maned Boar",
             "Mimick", "Mushroom", "Sandman", "Skull Soldier", "Slime", "Surprise Box"],
    "Water": ["Forest Keeper", "Ghost", "Harpu", "Howl", "Imp", "Maned Boar",
              "Mimick", "Mushroom", "Sandman", "Skull Soldier", "Slime", "Surprise Box"],
    "Wind": ["Forest Keeper", "Ghost", "Harpu", "Howl", "Imp", "Maned Boar",
             "Mimick", "Mushroom", "Sandman", "Skull Soldier", "Slime", "Surprise Box"],
    "Light": ["Forest Keeper", "Ghost", "Harpu", "Howl", "Imp", "Maned Boar",
              "Mimick", "Mushroom", "Sandman", "Skull Soldier", "Slime", "Surprise Box"],
    "Dark": ["Forest Keeper", "Ghost", "Harpu", "Howl", "Imp", "Maned Boar",
             "Mimick", "Mushroom", "Sandman", "Skull Soldier", "Slime", "Surprise Box"],
}

# Полные рецепты 5★
FUSION_RECIPES = {
    "Veromos": {
        "element": "dark",
        "awakened": "Veromos",
        "materials": {
            "Kumae": {"element": "dark", "stars": 3, "awakened": "Kumae", "family": "Yeti"},
            "Akia": {"element": "fire", "stars": 4, "awakened": "Akia", "family": "Succubus"},
            "Argen": {"element": "wind", "stars": 4, "awakened": "Argen", "family": "Vampire"},
            "Mikene": {"element": "water", "stars": 4, "awakened": "Mikene", "family": "Undine"},
        }
    },
    "Sigmarus": {
        "element": "water",
        "awakened": "Sigmarus",
        "materials": {
            "Susano": {"element": "water", "stars": 4, "awakened": "Susano", "family": "Ninja"},
            "Jojo": {"element": "fire", "stars": 4, "awakened": "Jojo", "family": "Joker"},
            "Arang": {"element": "wind", "stars": 4, "awakened": "Arang", "family": "Nine-tailed Fox"},
            "Lulu": {"element": "water", "stars": 3, "awakened": "Lulu", "family": "Howl"},
        }
    },
    "Katarina": {
        "element": "wind",
        "awakened": "Katarina",
        "materials": {
            "Baretta": {"element": "fire", "stars": 4, "awakened": "Baretta", "family": "Sylph"},
            "Shimitae": {"element": "wind", "stars": 4, "awakened": "Shimitae", "family": "Sylph"},
            "Liesel": {"element": "water", "stars": 4, "awakened": "Liesel", "family": "Vampire"},
            "Taru": {"element": "light", "stars": 3, "awakened": "Taru", "family": "Imp"},
        }
    },
    "Jeanne": {
        "element": "light",
        "awakened": "Jeanne",
        "materials": {
            "Raoq": {"element": "fire", "stars": 3, "awakened": "Raoq", "family": "Inugami"},
            "Fria": {"element": "fire", "stars": 4, "awakened": "Fria", "family": "Sylphid"},
            "Tyron": {"element": "water", "stars": 4, "awakened": "Tyron", "family": "Sylph"},
            "Eintau": {"element": "wind", "stars": 3, "awakened": "Eintau", "family": "Minotauros"},
        }
    },
    "Xiong Fei": {
        "element": "fire",
        "awakened": "Xiong Fei",
        "materials": {
            "Ling Ling": {"element": "wind", "stars": 4, "awakened": "Ling Ling", "family": "Kung Fu Girl"},
            "Hong Hua": {"element": "fire", "stars": 4, "awakened": "Hong Hua", "family": "Kung Fu Girl"},
            "Xiao Lin": {"element": "water", "stars": 4, "awakened": "Xiao Lin", "family": "Kung Fu Girl"},
            "Randy": {"element": "wind", "stars": 3, "awakened": "Randy", "family": "Bounty Hunter"},
        }
    },
    "Balegyr": {
        "element": "fire",
        "awakened": "Balegyr",
        "materials": {
            "Shaffron": {"element": "light", "stars": 4, "awakened": "Shaffron", "family": "Imp Champion"},
            "Mara": {"element": "dark", "stars": 4, "awakened": "Mara", "family": "Amazon"},
            "Covenant": {"element": "dark", "stars": 4, "awakened": "Covenant", "family": "Magical Archer"},
            "Kroa": {"element": "dark", "stars": 3, "awakened": "Kroa", "family": "Harg"},
        }
    },
    "Riley": {
        "element": "wind",
        "awakened": "Riley",
        "materials": {
            "Moria": {"element": "wind", "stars": 4, "awakened": "Moria", "family": "Dryad"},
            "Herne": {"element": "water", "stars": 4, "awakened": "Herne", "family": "Dryad"},
            "Nisha": {"element": "dark", "stars": 4, "awakened": "Nisha", "family": "Dryad"},
            "Gina": {"element": "wind", "stars": 3, "awakened": "Gina", "family": "Mystic Witch"},
        }
    },
}

# Карта семейство -> базовые составляющие (для раскрытия 4★)
FAMILY_BASE_MATERIALS = {
    "Succubus": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
    "Undine": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
    "Vampire": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
    "Ninja": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
    "Joker": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
    "Nine-tailed Fox": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
    "Sylph": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
    "Sylphid": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
    "Kung Fu Girl": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
    "Imp Champion": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
    "Amazon": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
    "Magical Archer": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
    "Dryad": {"stars": 4, "materials": {
        "Fire": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Water": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Wind": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Light": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
        "Dark": ["Magical Archer", "Pixie", "Inugami", "Salamander"],
    }},
}

# Карта 3★ -> базовые 2★ и 3★
AWAKENED_3STAR_MATERIALS = {
    "Lulu": {"family": "Howl", "element": "water", "stars": 3, "materials": {
        "water": ["Imp", "Mushroom", "Harpu", "Forest Keeper"],
    }},
    "Taru": {"family": "Imp", "element": "light", "stars": 3, "materials": {
        "light": ["Imp", "Mushroom", "Harpu", "Forest Keeper"],
    }},
    "Raoq": {"family": "Inugami", "element": "fire", "stars": 3, "materials": {
        "fire": ["Harpy", "Elemental", "Fairy", "Golem"],
    }},
    "Eintau": {"family": "Minotauros", "element": "wind", "stars": 3, "materials": {
        "wind": ["Harpy", "Elemental", "Fairy", "Golem"],
    }},
    "Randy": {"family": "Bounty Hunter", "element": "wind", "stars": 3, "materials": {
        "wind": ["Harpy", "Elemental", "Fairy", "Golem"],
    }},
    "Kroa": {"family": "Harg", "element": "dark", "stars": 3, "materials": {
        "dark": ["Harpy", "Elemental", "Fairy", "Golem"],
    }},
    "Gina": {"family": "Mystic Witch", "element": "wind", "stars": 3, "materials": {
        "wind": ["Harpy", "Elemental", "Fairy", "Golem"],
    }},
    "Kumae": {"family": "Yeti", "element": "dark", "stars": 3, "materials": {
        "dark": ["Harpy", "Elemental", "Fairy", "Golem"],
    }},
}


class HexMonsterImage(QLabel):
    """
    Кликабельная картинка монстра с циклическим переключением:
    0 - обычная картинка
    1 - маркер (монстр получен)
    2 - скрыта (серая/пустая)
    Состояние сохраняется в БД.
    """

    def __init__(self, name, element, recipe_name, image_dir=HL_DIR, size=50):
        super().__init__()
        self.name = name
        self.element = element
        self.recipe_name = recipe_name  # <-- нужно для сохранения в БД
        self.image_dir = image_dir
        self.size = size

        # Загружаем состояние из БД
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
        """Загрузить все варианты картинки"""
        filename = f"{self.name}_{self.element}.png"
        path = os.path.join(self.image_dir, filename)

        pix = QPixmap(path)
        if not pix.isNull():
            pix = pix.scaled(self.size, self.size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            pix = QPixmap(self.size, self.size)
            pix.fill(QColor("#444"))

        self._pixmap_original = pix

        # Маркированная версия (с зеленой галочкой)
        self._pixmap_marked = QPixmap(pix)
        painter = QPainter(self._pixmap_marked)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#1abc9c"))
        painter.setPen(QPen(QColor("#fff"), 1))
        painter.drawEllipse(self.size - 14, 2, 12, 12)
        painter.setPen(QPen(QColor("#fff"), 2))
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        painter.drawText(self.size - 14, 2, 12, 12, Qt.AlignCenter, "✓")
        painter.end()

        # Скрытая версия (серая)
        self._pixmap_hidden = QPixmap(self.size, self.size)
        self._pixmap_hidden.fill(QColor("#333"))

    def mousePressEvent(self, event):
        """Циклическое переключение состояний с сохранением в БД"""
        if event.button() == Qt.LeftButton:
            self.state = (self.state + 1) % 3

            # Сохраняем в БД
            save_hex_state(self.recipe_name, self.name, self.element, self.state)

            self._update_display()

            # Уведомляем родительский виджет об изменении
            if hasattr(self, 'parent_recipe') and self.parent_recipe:
                self.parent_recipe.check_completion()
        super().mousePressEvent(event)

    def _update_display(self):
        """Обновить отображаемую картинку"""
        if self.state == 0:
            self.setPixmap(self._pixmap_original)
            self.setToolTip(f"{self.name} ({self.element})")
        elif self.state == 1:
            self.setPixmap(self._pixmap_marked)
            self.setToolTip(f"✅ {self.name} ({self.element}) - ПОЛУЧЕН")
        else:
            self.setPixmap(self._pixmap_hidden)
            self.setToolTip(f"❌ {self.name} ({self.element}) - СКРЫТ")

    def is_marked(self):
        """Получен ли монстр (state == 1)"""
        return self.state == 1

    def is_hidden(self):
        """Скрыт ли монстр (state == 2)"""
        return self.state == 2


class HexRecipeWidget(QFrame):
    """Виджет одного рецепта с деревом материалов"""

    def __init__(self, recipe_name, recipe_data):
        super().__init__()
        self.recipe_name = recipe_name
        self.recipe_data = recipe_data
        self.target_element = recipe_data["element"]
        self.target_awakened = recipe_data.get("awakened", recipe_name)
        self.materials = recipe_data["materials"]

        # Словарь всех HexMonsterImage для проверки
        self.all_images = {}
        # Изображение целевого монстра
        self.target_image = None

        self.setStyleSheet("""
            QFrame {
                background: #2a2a2a;
                border-radius: 10px;
                border: 2px solid #3d3d3d;
            }
            QFrame:hover {
                border: 2px solid #4a7aca;
            }
        """)

        self._build_ui()
        # Проверяем состояние после загрузки
        self.check_completion()

    def _build_ui(self):
        """Построить дерево рецепта"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(15, 10, 15, 10)

        # Заголовок
        title = QLabel(f"🔮 {self.recipe_name}")
        title.setStyleSheet("color:#f1c40f;font-size:16px;font-weight:bold;background:transparent;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Горизонтальная линия
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background:#555;max-height:2px;")
        main_layout.addWidget(line)

        # Целевой монстр (5★)
        target_layout = QHBoxLayout()
        target_layout.setAlignment(Qt.AlignCenter)
        target_label = QLabel(f"Цель ({self.target_element}):")
        target_label.setStyleSheet("color:#aaa;font-size:11px;background:transparent;")
        target_layout.addWidget(target_label)

        self.target_image = HexMonsterImage(
            self.target_awakened, self.target_element, self.recipe_name, HL_DIR, 64
        )
        self.target_image.parent_recipe = self
        self.all_images["target"] = self.target_image
        target_layout.addWidget(self.target_image)
        main_layout.addLayout(target_layout)

        # Стрелка вниз
        arrow = QLabel("▼")
        arrow.setStyleSheet("color:#888;font-size:14px;background:transparent;")
        arrow.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(arrow)

        # Материалы (4★ и 3★)
        materials_layout = QHBoxLayout()
        materials_layout.setSpacing(10)
        materials_layout.setAlignment(Qt.AlignCenter)

        for mat_name, mat_data in self.materials.items():
            mat_widget = self._create_material_widget(mat_name, mat_data)
            materials_layout.addWidget(mat_widget)

        main_layout.addLayout(materials_layout)
        main_layout.addStretch()

    def _create_material_widget(self, name, data):
        """Создать виджет для одного материала с его под-материалами"""
        widget = QFrame()
        widget.setStyleSheet("background:#333;border-radius:6px;padding:5px;")
        layout = QVBoxLayout(widget)
        layout.setSpacing(4)
        layout.setContentsMargins(5, 5, 5, 5)

        # Имя материала
        stars = "⭐" * data["stars"]
        lbl = QLabel(f"{name}\n{stars}")
        lbl.setStyleSheet("color:#fff;font-size:9px;font-weight:bold;background:transparent;")
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)

        # Картинка материала
        img = HexMonsterImage(name, data["element"], self.recipe_name, HL_DIR, 50)
        img.parent_recipe = self
        self.all_images[name] = img

        img_layout = QHBoxLayout()
        img_layout.setAlignment(Qt.AlignCenter)
        img_layout.addWidget(img)
        layout.addLayout(img_layout)

        # Под-материалы (для 4★ и некоторых 3★)
        if data["stars"] >= 3:
            sub_materials = self._get_sub_materials(name, data)
            if sub_materials:
                sub_lbl = QLabel("▾")
                sub_lbl.setStyleSheet("color:#888;font-size:10px;background:transparent;")
                sub_lbl.setAlignment(Qt.AlignCenter)
                layout.addWidget(sub_lbl)

                sub_layout = QHBoxLayout()
                sub_layout.setSpacing(2)
                sub_layout.setAlignment(Qt.AlignCenter)

                for sub in sub_materials:
                    sub_img = HexMonsterImage(
                        sub["name"], sub["element"], self.recipe_name, HL_DIR, 35
                    )
                    sub_img.parent_recipe = self
                    self.all_images[f"{name}_{sub['name']}"] = sub_img
                    sub_layout.addWidget(sub_img)

                layout.addLayout(sub_layout)

        return widget

    def _get_sub_materials(self, name, data):
        """Получить под-материалы для данного материала"""
        family = data.get("family", "")

        # Если это 4★ с известным семейством
        if data["stars"] == 4 and family in FAMILY_BASE_MATERIALS:
            element = data["element"]
            base_mats = FAMILY_BASE_MATERIALS[family]["materials"].get(
                element.capitalize(), []
            )
            return [{"name": mat, "element": element} for mat in base_mats[:4]]

        # Если это 3★ с известным рецептом
        if name in AWAKENED_3STAR_MATERIALS:
            recipe = AWAKENED_3STAR_MATERIALS[name]
            element = recipe["element"]
            base_mats = recipe["materials"].get(element, [])
            return [{"name": mat, "element": element} for mat in base_mats[:4]]

        # Для обычных 3★: базовые 2★
        if data["stars"] == 3:
            element = data["element"]
            base_mats = BASE_2STAR.get(element.capitalize(), [])[:4]
            return [{"name": mat, "element": element} for mat in base_mats]

        return []

    def check_completion(self):
        """Проверить, все ли составляющие (кроме target) помечены как полученные"""
        # Проверяем все материалы (исключая target)
        all_obtained = True
        for key, img in self.all_images.items():
            if key == "target":
                continue
            if not img.is_marked():
                all_obtained = False
                break

        # Авто-обновление цели
        if all_obtained and self.target_image.state != 1:
            self.target_image.state = 1
            self.target_image._update_display()
            # Сохраняем в БД
            save_hex_state(
                self.recipe_name,
                self.target_awakened,
                self.target_element,
                1
            )
        elif not all_obtained and self.target_image.state == 1:
            self.target_image.state = 0
            self.target_image._update_display()
            save_hex_state(
                self.recipe_name,
                self.target_awakened,
                self.target_element,
                0
            )


class HexTab(BaseList):
    """Вкладка HEX - рецепты фьюжна"""

    def __init__(self):
        super().__init__()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.recipe_widgets = []

    def refresh(self):
        """Загрузить и отобразить все рецепты"""
        self.clear()
        self.recipe_widgets = []

        # Заголовок
        title = QLabel("🔮 HEX / FUSION RECIPES")
        title.setStyleSheet(
            "color:#f1c40f;font-size:18px;font-weight:bold;"
            "background:transparent;padding:10px;"
        )
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        # Описание
        desc = QLabel(
            "🖱️ Клик по картинке:\n"
            "  1-й раз = ✅ получен\n"
            "  2-й раз = ❌ скрыть\n"
            "  3-й раз = 🔄 сброс\n"
            "🌟 Когда все составляющие отмечены — цель отмечается автоматически!\n"
            "💾 Состояния сохраняются в БД между запусками"
        )
        desc.setStyleSheet("color:#888;font-size:11px;background:transparent;padding:5px;")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        self.layout.addWidget(desc)

        # Разделитель
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background:#555;max-height:2px;")
        self.layout.addWidget(sep)

        # Отображаем все рецепты
        for recipe_name, recipe_data in FUSION_RECIPES.items():
            recipe_widget = HexRecipeWidget(recipe_name, recipe_data)
            self.recipe_widgets.append(recipe_widget)
            self.layout.addWidget(recipe_widget)

        self.layout.addStretch()
