# db.py - ПОЛНАЯ ВЕРСИЯ С ВСЕМИ ФУНКЦИЯМИ
import sqlite3
import os
import re
import json
from datetime import datetime

DB = os.path.join(os.path.dirname(__file__), "swtracker.db")

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS monsters(id INTEGER PRIMARY KEY AUTOINCREMENT, name_en TEXT UNIQUE, stars_base INTEGER DEFAULT 3, sort_order INTEGER DEFAULT 0, update_name TEXT DEFAULT '')")
    c.execute("CREATE TABLE IF NOT EXISTS monster_status(monster_id INTEGER PRIMARY KEY, water INTEGER DEFAULT 0, fire INTEGER DEFAULT 0, wind INTEGER DEFAULT 0, light INTEGER DEFAULT 0, dark INTEGER DEFAULT 0, water_locked INTEGER DEFAULT 0, fire_locked INTEGER DEFAULT 0, wind_locked INTEGER DEFAULT 0, light_locked INTEGER DEFAULT 0, dark_locked INTEGER DEFAULT 0)")
    c.execute("CREATE TABLE IF NOT EXISTS food_status(monster_id INTEGER PRIMARY KEY, water INTEGER DEFAULT 0, fire INTEGER DEFAULT 0, wind INTEGER DEFAULT 0, light INTEGER DEFAULT 0, dark INTEGER DEFAULT 0, water_locked INTEGER DEFAULT 0, fire_locked INTEGER DEFAULT 0, wind_locked INTEGER DEFAULT 0, light_locked INTEGER DEFAULT 0, dark_locked INTEGER DEFAULT 0)")
    c.execute("CREATE TABLE IF NOT EXISTS element_data(monster_id INTEGER, element TEXT, set1 TEXT DEFAULT '', set2 TEXT DEFAULT '', set3 TEXT DEFAULT '', slot2 TEXT DEFAULT '', slot4 TEXT DEFAULT '', slot6 TEXT DEFAULT '', slot2_rune TEXT DEFAULT '', slot4_rune TEXT DEFAULT '', slot6_rune TEXT DEFAULT '', rune1 TEXT DEFAULT '', rune2 TEXT DEFAULT '', rune3 TEXT DEFAULT '', stars TEXT DEFAULT '', awakening TEXT DEFAULT '', skills TEXT DEFAULT '', artifacts TEXT DEFAULT '', custom_name TEXT DEFAULT '', star5 INTEGER DEFAULT 0, star6 INTEGER DEFAULT 0, PRIMARY KEY(monster_id, element))")
    conn.commit()
    conn.close()

def get_monsters():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, name_en, stars_base, update_name FROM monsters ORDER BY stars_base DESC, name_en")
    r = c.fetchall()
    conn.close()
    return r

def get_status(mid):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT water, fire, wind, light, dark, water_locked, fire_locked, wind_locked, light_locked, dark_locked FROM monster_status WHERE monster_id=?", (mid,))
    r = c.fetchone()
    conn.close()
    if r: return list(r[:5]), list(r[5:])
    return [0,0,0,0,0], [0,0,0,0,0]

def save_status(mid, elem, val, locked=None):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO monster_status(monster_id) VALUES(?)", (mid,))
    c.execute(f"UPDATE monster_status SET {elem}=? WHERE monster_id=?", (val, mid))
    if locked is not None:
        c.execute(f"UPDATE monster_status SET {elem}_locked=? WHERE monster_id=?", (1 if locked else 0, mid))
    conn.commit()
    conn.close()

def get_monsters_food():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, name_en, stars_base, update_name FROM monsters ORDER BY sort_order, name_en")
    r = c.fetchall()
    conn.close()
    return r

def get_food(mid):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT water, fire, wind, light, dark, water_locked, fire_locked, wind_locked, light_locked, dark_locked FROM food_status WHERE monster_id=?", (mid,))
    r = c.fetchone()
    conn.close()
    if r: return list(r[:5]), list(r[5:])
    return [0,0,0,0,0], [0,0,0,0,0]

def save_food(mid, elem, val, locked=None):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO food_status(monster_id) VALUES(?)", (mid,))
    c.execute(f"UPDATE food_status SET {elem}=? WHERE monster_id=?", (val, mid))
    if locked is not None:
        c.execute(f"UPDATE food_status SET {elem}_locked=? WHERE monster_id=?", (1 if locked else 0, mid))
    conn.commit()
    conn.close()

def get_element_monsters(element):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(f"SELECT m.id, m.name_en FROM monsters m JOIN monster_status ms ON m.id=ms.monster_id WHERE ms.{element}=3 ORDER BY m.name_en")
    r = c.fetchall()
    conn.close()
    return [(row[0], row[1]) for row in r]

def get_element_status(mid, element):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT set1, set2, set3, slot2, slot4, slot6, slot2_rune, slot4_rune, slot6_rune, rune1, rune2, rune3, stars, awakening, skills, artifacts, custom_name, star5, star6 FROM element_data WHERE monster_id=? AND element=?", (mid, element))
    r = c.fetchone()
    conn.close()
    if r:
        return {
            "set1": r[0] or "", "set2": r[1] or "", "set3": r[2] or "",
            "slot2": r[3] or "", "slot4": r[4] or "", "slot6": r[5] or "",
            "slot2_rune": r[6] or "", "slot4_rune": r[7] or "", "slot6_rune": r[8] or "",
            "rune1": r[9] or "", "rune2": r[10] or "", "rune3": r[11] or "",
            "stars": r[12] or "", "awakening": r[13] or "", "skills": r[14] or "",
            "artifacts": r[15] or "", "custom_name": r[16] or "",
            "star5": bool(r[17]), "star6": bool(r[18])
        }
    return {}

def save_element_data(mid, element, data):
    """Сохранить данные карточки, не затирая поля, которые не переданы."""
    existing = get_element_status(mid, element)
    merged = {**existing, **data}

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        """INSERT OR REPLACE INTO element_data(
            monster_id, element, set1, set2, set3,
            slot2, slot4, slot6, slot2_rune, slot4_rune, slot6_rune,
            rune1, rune2, rune3, stars, awakening, skills, artifacts,
            custom_name, star5, star6
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            mid, element,
            merged.get("set1", ""), merged.get("set2", ""), merged.get("set3", ""),
            merged.get("slot2", ""), merged.get("slot4", ""), merged.get("slot6", ""),
            merged.get("slot2_rune", ""), merged.get("slot4_rune", ""), merged.get("slot6_rune", ""),
            merged.get("rune1", ""), merged.get("rune2", ""), merged.get("rune3", ""),
            merged.get("stars", ""), merged.get("awakening", ""), merged.get("skills", ""),
            merged.get("artifacts", ""), merged.get("custom_name", ""),
            1 if merged.get("star5") else 0, 1 if merged.get("star6") else 0,
        ),
    )
    conn.commit()
    conn.close()

def sync_txt(path):
    if not os.path.exists(DB): init_db()
    with open(path, 'r', encoding='utf-8') as f: lines = f.readlines()
    conn = sqlite3.connect(DB); c = conn.cursor()
    order = 0; cur_upd = "Base"; added = 0
    for line in lines:
        line = line.strip()
        if not line: continue
        if re.match(r'^\s*\d{4}', line): cur_upd = line.strip(); continue
        parts = line.rsplit(maxsplit=1)
        name = parts[0].strip()
        if not name: continue
        stars = int(parts[1]) if len(parts)>1 and parts[1].isdigit() else 3
        c.execute("INSERT OR IGNORE INTO monsters(name_en,stars_base,sort_order,update_name) VALUES(?,?,?,?)",(name,stars,order,cur_upd))
        if c.rowcount > 0:
            mid = c.lastrowid
            c.execute("INSERT OR IGNORE INTO monster_status(monster_id) VALUES(?)",(mid,))
            c.execute("INSERT OR IGNORE INTO food_status(monster_id) VALUES(?)",(mid,))
            added += 1
        order += 1
    conn.commit(); conn.close(); return added

def export_db():
    if not os.path.exists(DB): return None
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row; c = conn.cursor()
    data = {}
    for table in ['monsters','monster_status','food_status','element_data']:
        c.execute(f"SELECT * FROM {table}")
        data[table] = [dict(row) for row in c.fetchall()]
    conn.close()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bswc_export_{timestamp}.json"
    with open(os.path.join(os.path.dirname(__file__), filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename

def import_db():
    files = [f for f in os.listdir(os.path.dirname(__file__)) if f.startswith('bswc_export_') and f.endswith('.json')]
    if not files: return False
    with open(os.path.join(os.path.dirname(__file__), sorted(files)[-1]), 'r', encoding='utf-8') as f:
        data = json.load(f)
    conn = sqlite3.connect(DB); c = conn.cursor()
    try:
        c.execute("DELETE FROM element_data"); c.execute("DELETE FROM food_status")
        c.execute("DELETE FROM monster_status"); c.execute("DELETE FROM monsters")
        for table in ['monsters','monster_status','food_status','element_data']:
            if table in data and data[table]:
                for row in data[table]:
                    p = ','.join(['?' for _ in row])
                    c.execute(f"INSERT INTO {table} ({','.join(row.keys())}) VALUES ({p})", list(row.values()))
        conn.commit(); conn.close(); return True
    except Exception as e:
        conn.rollback(); conn.close(); print(f"Import error: {e}"); return False

def get_all_monsters():
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT id, name_en, stars_base FROM monsters ORDER BY name_en")
    r = c.fetchall(); conn.close(); return r

if not os.path.exists(DB):
    init_db()
