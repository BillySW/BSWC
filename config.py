# config.py - ИСПРАВЛЕННАЯ ВЕРСИЯ ДЛЯ НОВОГО ФОРМАТА
import os

# Пути к папкам
TL_DIR = "TL"
FL_DIR = "FL"
HAVE_DIR = "have"
HL_DIR = "HL"

# Список рун для комбобоксов
RUNES = [
    "", "Energy", "Fatal", "Blade", "Swift", "Despair", "Focus", "Guard", "Endure",
    "Shield", "Revenge", "Will", "Nemesis", "Vampire", "Destroy", "Rage",
    "Violent", "Seal", "Accuracy", "Determination", "Enhance", "Fight", "Tolerance"
]

# Статы для комбобоксов
RUNE_STATS = [
    "", "HP flat", "HP%", "ATK flat", "ATK%", "DEF flat", "DEF%",
    "SPD", "CR%", "CD%", "ACC%", "RES%"
]

# Загрузка пробужденных имен из awakened.txt
def load_awakened_names():
    """
    Загрузить пробужденные имена из файла
    Формат: Семейство|Стихия|Пробужденное имя
    Возвращает словарь: {семейство: {стихия: имя}}
    """
    awakened = {}
    filepath = os.path.join(os.path.dirname(__file__), "awakened.txt")

    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) == 3:
                        family = parts[0].strip()
                        element = parts[1].strip()
                        name = parts[2].strip()

                        if family not in awakened:
                            awakened[family] = {}
                        awakened[family][element] = name
    else:
        print(f"Файл awakened.txt не найден по пути: {filepath}")

    return awakened

AWAKENED_NAMES = load_awakened_names()

def get_awakened_name(family, element):
    """
    Получить пробужденное имя для семейства и стихии
    """
    if family in AWAKENED_NAMES:
        if element in AWAKENED_NAMES[family]:
            return AWAKENED_NAMES[family][element]
    return family  # Если нет в словаре, возвращаем имя семейства

# Коллаборационные монстры и их доступные элементы
COLLAB_MONSTERS = {
    # === Одиночные коллаборации ===
    "Fairy Queen": [0, 0, 0, 1, 0],      # только свет
    "Vampire Lord": [0, 0, 0, 0, 1],     # только тьма
    "GingerBrave": [0, 0, 1, 0, 0],      # только ветер
    "Lollipop Warrior": [0, 0, 1, 0, 0], # только ветер
    "Heihachi Mishima": [0, 1, 0, 0, 0], # только огонь
    "Frodo": [1, 0, 0, 0, 0],            # только вода
    "Dual Blade": [0, 0, 0, 1, 0],       # только свет
    "Altaïr": [0, 0, 0, 1, 0],           # только свет
    "KEN": [0, 1, 0, 0, 0],              # только огонь
    "Shadow Claw": [0, 1, 0, 0, 0],      # только огонь
    "Ryomen Sukuna": [0, 0, 0, 0, 1],    # только тьма
    "Black Tortoise Champion": [0, 0, 1, 0, 0], # только ветер
    "Gyomei Himejima": [0, 0, 1, 0, 0],  # только ветер
    "Exorcist Association Arbiter": [0, 0, 0, 0, 1], # только тьма
    "Low Elemental": [1, 1, 1, 0, 0],    # только стихии
    "Magical Archer Light": [0, 0, 0, 1, 0], # только свет
    "Daimon": [0, 1, 0, 0, 0],           # только огонь

    # === Street Fighter V ===
    "RYU": [1, 1, 1, 1, 1],
    "CHUN LI": [1, 1, 1, 1, 1],
    "KEN": [0, 1, 0, 0, 0],
    "M.BISON": [1, 1, 1, 1, 1],
    "DHALSIM": [1, 1, 1, 1, 1],

    # === Cookie Run: Kingdom ===
    "GingerBrave": [0, 0, 1, 0, 0],
    "Pure Vanilla Cookie": [1, 1, 1, 1, 1],
    "Madeleine Cookie": [1, 1, 1, 1, 1],
    "Espresso Cookie": [1, 1, 1, 1, 1],
    "Hollyberry Cookie": [1, 1, 1, 1, 1],
    "Black Tea Bunny": [1, 1, 1, 1, 1],
    "Pudding Princess": [1, 1, 1, 1, 1],
    "Choco Knight": [1, 1, 1, 1, 1],
    "Lollipop Warrior": [0, 0, 1, 0, 0],
    "Macaron Guard": [1, 1, 1, 1, 1],

    # === Assassin's Creed ===
    "Altaïr": [0, 0, 0, 1, 0],
    "Ezio": [1, 1, 1, 1, 1],
    "Kassandra": [1, 1, 1, 1, 1],
    "Eivor": [1, 1, 1, 1, 1],
    "Bayek": [1, 1, 1, 1, 1],

    # === The Witcher ===
    "Geralt": [1, 1, 1, 1, 1],
    "Ciri": [1, 1, 1, 1, 1],
    "Yennefer": [1, 1, 1, 1, 1],
    "Triss": [1, 1, 1, 1, 1],

    # === Jujutsu Kaisen ===
    "Yuji Itadori": [1, 1, 1, 1, 1],
    "Megumi Fushiguro": [1, 1, 1, 1, 1],
    "Nobara Kugisaki": [1, 1, 1, 1, 1],
    "Satoru Gojo": [1, 1, 1, 1, 1],
    "Ryomen Sukuna": [0, 0, 0, 0, 1],  # Только тьма
    "Exorcist Association Arbiter": [0, 0, 0, 0, 1],  # Только тьма
    "Exorcist Association Conjurer": [1, 1, 1, 1, 1],
    "Exorcist Association Fighter": [1, 1, 1, 1, 1],
    "Exorcist Association Hunter": [1, 1, 1, 1, 1],
    "Exorcist Association Resolver": [1, 1, 1, 1, 1],

    # === Tekken ===
    "Jin Kazama": [1, 1, 1, 1, 1],
    "Paul Phoenix": [1, 1, 1, 1, 1],
    "Nina Williams": [1, 1, 1, 1, 1],
    "Hwoarang": [1, 1, 1, 1, 1],
    "Heihachi Mishima": [0, 1, 0, 0, 0],  # Только огонь

    # === Demon Slayer ===
    "Azure Dragon Swordsman": [1, 1, 1, 1, 1],
    "Vermilion Bird Dancer": [1, 1, 1, 1, 1],
    "White Tiger Blade Master": [1, 1, 1, 1, 1],
    "Slayer": [1, 1, 1, 1, 1],
    "Qilin Slasher": [1, 1, 1, 1, 1],
    "Black Tortoise Champion": [0, 0, 1, 0, 0],  # Только ветер
    "Tanjiro Kamado": [1, 1, 1, 1, 1],
    "Nezuko Kamado": [1, 1, 1, 1, 1],
    "Zenitsu Agatsuma": [1, 1, 1, 1, 1],
    "Inosuke Hashibira": [1, 1, 1, 1, 1],
    "Gyomei Himejima": [0, 0, 1, 0, 0],  # Только ветер

    # === Lord of the Rings ===
    "Frodo": [1, 0, 0, 0, 0],  # Только вода
    "Aragorn": [1, 1, 1, 1, 1],
    "Legolas": [1, 1, 1, 1, 1],
    "Gandalf": [1, 1, 1, 1, 1],
    "Gollum": [1, 1, 1, 1, 1],

    # === The King of Fighters ===
    "Taebeak": [1, 1, 1, 1, 1],
    "Dr. Plazma": [1, 1, 1, 1, 1],

    # === Frieren ===
    "Himmel": [1, 0, 0, 0, 0],
    "Frieren": [1, 1, 1, 1, 1],
    "Fern": [1, 1, 1, 1, 1],
    "Stark": [1, 1, 1, 1, 1],
    "Ubel": [1, 1, 1, 1, 1],
}

# Список коллабораций для быстрой проверки
COLLAB_NAMES = set(COLLAB_MONSTERS.keys())

# Элементы в правильном порядке
ELEMENTS = ['water', 'fire', 'wind', 'light', 'dark']

# Иконки элементов
ELEMENT_ICONS = {
    'water': '💧',
    'fire': '🔥',
    'wind': '🍃',
    'light': '✨',
    'dark': '🌑'
}

# Стили для вкладок
TAB_STYLE = "background:#2d2d2d;"

# Проверка загрузки при старте (для отладки)
if __name__ == "__main__":
    print("=== ПРОВЕРКА ЗАГРУЗКИ AWAKENED.TXT ===")
    print(f"Загружено семейств: {len(AWAKENED_NAMES)}")

    # Проверяем конкретные имена
    test_cases = [
        ("Garuda", "water"),
        ("Garuda", "fire"),
        ("Inugami", "fire"),
        ("Inugami", "light"),
        ("Griffon", "wind"),
    ]
    for family, element in test_cases:
        name = get_awakened_name(family, element)
        print(f"{family} ({element}) -> {name}")
