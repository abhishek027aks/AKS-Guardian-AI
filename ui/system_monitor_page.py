from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame
)

from PySide6.QtCore import QTimer

import psutil


class SystemMonitorPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_stats
        )

        self.timer.start(1000)

    def setup_ui(self):

        self.setStyleSheet("""
            background:#0b0f19;
            color:white;
        """)

        layout = QVBoxLayout(self)

        title = QLabel(
            "System Monitor"
        )

        title.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.cpu = QLabel()
        self.ram = QLabel()
        self.disk = QLabel()

        layout.addWidget(self.cpu)
        layout.addWidget(self.ram)
        layout.addWidget(self.disk)

        self.update_stats()

    def update_stats(self):

        self.cpu.setText(
            f"CPU : {psutil.cpu_percent()}%"
        )

        self.ram.setText(
            f"RAM : {psutil.virtual_memory().percent}%"
        )

        self.disk.setText(
            f"Disk : {psutil.disk_usage('C:\\').percent}%"
        )