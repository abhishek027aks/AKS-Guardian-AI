from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt, QTimer
import psutil

class ProcessPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0b0f19;")
        self.setup_ui()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_processes)
        self.timer.start(3000) # Updates every 3 seconds to avoid UI lag

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(20)

        title = QLabel("Process Manager")
        title.setStyleSheet("font-size: 34px; font-weight: bold; color: white;")
        layout.addWidget(title)

        container = QFrame()
        container.setStyleSheet("background-color: #121927; border-radius: 12px; border: 1px solid #1E2638; padding: 10px;")
        vbox = QVBoxLayout(container)

        header = QLabel("Top 15 Resource Consumers")
        header.setStyleSheet("font-size: 16px; font-weight: bold; color: #f3f4f6; border: none; margin-bottom: 5px;")
        vbox.addWidget(header)

        # Professional Data Table
        self.table = QTableWidget(15, 3)
        self.table.setHorizontalHeaderLabels(["Process Name", "PID", "RAM Usage (%)"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        # Premium Table Styling
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: transparent; color: #d1d5db; border: none; gridline-color: #1f2937; font-size: 13px;
            }
            QHeaderView::section {
                background-color: #1E2638; color: #9ca3af; font-weight: bold; padding: 8px; border: none;
            }
            QTableWidget::item { padding: 5px; border-bottom: 1px solid #1f2937; }
        """)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        vbox.addWidget(self.table)
        layout.addWidget(container)

    def update_processes(self):
        try:
            apps = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    if proc.info['memory_percent'] is not None:
                        apps.append(proc.info)
                except: pass
                
            apps.sort(key=lambda x: x['memory_percent'], reverse=True)
            
            for row, p in enumerate(apps[:15]):
                name_item = QTableWidgetItem(f"⚙️ {p['name']}")
                pid_item = QTableWidgetItem(str(p['pid']))
                pid_item.setTextAlignment(Qt.AlignCenter)
                ram_item = QTableWidgetItem(f"{p['memory_percent']:.2f}%")
                ram_item.setTextAlignment(Qt.AlignCenter)
                
                self.table.setItem(row, 0, name_item)
                self.table.setItem(row, 1, pid_item)
                self.table.setItem(row, 2, ram_item)
        except Exception:
            pass