# options.py - ОБНОВЛЕННАЯ ВЕРСИЯ
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from db import sync_txt

class Options(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)

        # Кнопка синхронизации
        btn = QPushButton("📥 Sync mobs.txt")
        btn.setStyleSheet("QPushButton{background:#4a7aca;color:#fff;padding:12px;border-radius:6px;font-size:14px;}QPushButton:hover{background:#5a8ada;}")
        btn.clicked.connect(self.sync)
        lay.addWidget(btn)

        # Кнопка экспорта
        export_btn = QPushButton("💾 Export Data")
        export_btn.setStyleSheet("QPushButton{background:#27ae60;color:#fff;padding:12px;border-radius:6px;font-size:14px;}QPushButton:hover{background:#2ecc71;}")
        export_btn.clicked.connect(self.export_data)
        lay.addWidget(export_btn)

        # Кнопка импорта
        import_btn = QPushButton("📂 Import Data")
        import_btn.setStyleSheet("QPushButton{background:#f39c12;color:#fff;padding:12px;border-radius:6px;font-size:14px;}QPushButton:hover{background:#f1c40f;}")
        import_btn.clicked.connect(self.import_data)
        lay.addWidget(import_btn)

        # Статус
        self.status = QLabel("")
        self.status.setStyleSheet("color:#aaa;")
        lay.addWidget(self.status)
        lay.addStretch()

    def sync(self):
        path = os.path.join(os.path.dirname(__file__), "mobs.txt")
        if os.path.exists(path):
            added = sync_txt(path)
            self.status.setText(f"✅ Added {added} monsters")
            # Обновляем все вкладки
            self.parent.tir.refresh()
            self.parent.food.refresh()
            self.parent.tab_water.refresh()
            self.parent.tab_fire.refresh()
            self.parent.tab_wind.refresh()
            self.parent.tab_light.refresh()
            self.parent.tab_dark.refresh()
            self.parent.hex_tab.refresh()
            self.parent.search_tab.reload_monsters()
        else:
            self.status.setText("❌ mobs.txt not found")

    def export_data(self):
        """Экспорт данных в JSON"""
        from db import export_db
        path = export_db()
        self.status.setText(f"✅ Data exported to {path}")

    def import_data(self):
        """Импорт данных из JSON"""
        from db import import_db
        if import_db():
            self.status.setText("✅ Data imported successfully")
            # Обновляем все вкладки
            self.parent.tir.refresh()
            self.parent.food.refresh()
            self.parent.tab_water.refresh()
            self.parent.tab_fire.refresh()
            self.parent.tab_wind.refresh()
            self.parent.tab_light.refresh()
            self.parent.tab_dark.refresh()
            self.parent.hex_tab.refresh()
            self.parent.search_tab.reload_monsters()
        else:
            self.status.setText("❌ Import failed")
