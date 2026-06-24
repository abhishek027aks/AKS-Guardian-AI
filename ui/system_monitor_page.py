from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar, QGridLayout
from PySide6.QtCore import Qt, QTimer
import psutil

class SystemMonitorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0b0f19;")
        self.setup_ui()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_hardware_stats)
        self.timer.start(2000)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(25)

        title = QLabel("System Monitor")
        title.setStyleSheet("font-size: 34px; font-weight: bold; color: white; letter-spacing: -0.5px;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(20)

        # CPU Monitor Card
        self.cpu_bar, self.cpu_lbl = self.create_monitor_card("💻 CPU Utilization", grid, 0, 0, "#3b82f6")
        
        # RAM Monitor Card
        self.ram_bar, self.ram_lbl = self.create_monitor_card("💾 Memory (RAM) Usage", grid, 0, 1, "#a855f7")
        
        # Disk Monitor Card
        self.disk_bar, self.disk_lbl = self.create_monitor_card("💽 Primary Disk (C:)", grid, 1, 0, "#10b981")

        layout.addLayout(grid)
        layout.addStretch()

    def create_monitor_card(self, title_text, grid_layout, row, col, color):
        card = QFrame()
        card.setStyleSheet("background-color: #121927; border-radius: 12px; border: 1px solid #1E2638;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel(title_text)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #f3f4f6; border: none;")
        
        value_lbl = QLabel("0%")
        value_lbl.setStyleSheet("font-size: 14px; color: #9ca3af; border: none;")
        
        bar = QProgressBar()
        bar.setTextVisible(False)
        bar.setFixedHeight(12)
        bar.setStyleSheet(f"""
            QProgressBar {{ background-color: #1f2937; border-radius: 6px; border: none; }}
            QProgressBar::chunk {{ background-color: {color}; border-radius: 6px; }}
        """)

        card_layout.addWidget(title)
        card_layout.addWidget(value_lbl)
        card_layout.addWidget(bar)
        
        grid_layout.addWidget(card, row, col)
        return bar, value_lbl

    def update_hardware_stats(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage("C:\\")

            self.cpu_bar.setValue(int(cpu))
            self.cpu_lbl.setText(f"Utilized: {cpu}%")

            self.ram_bar.setValue(int(ram.percent))
            self.ram_lbl.setText(f"Used: {round(ram.used/(1024**3), 1)} GB / {round(ram.total/(1024**3), 1)} GB ({ram.percent}%)")

            self.disk_bar.setValue(int(disk.percent))
            self.disk_lbl.setText(f"Used: {round(disk.used/(1024**3), 1)} GB / {round(disk.total/(1024**3), 1)} GB ({disk.percent}%)")
        except Exception:
            pass