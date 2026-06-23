from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout
)

import psutil
import sys

class GuardianWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "AKS Guardian AI"
        )

        self.resize(
            500,
            300
        )

        layout = QVBoxLayout()

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        disk = psutil.disk_usage(
            "C:\\"
        ).percent

        title = QLabel(
            "🛡️ AKS Guardian AI"
        )

        cpu_label = QLabel(
            f"CPU : {cpu}%"
        )

        ram_label = QLabel(
            f"RAM : {ram}%"
        )

        disk_label = QLabel(
            f"Disk : {disk}%"
        )

        layout.addWidget(title)
        layout.addWidget(cpu_label)
        layout.addWidget(ram_label)
        layout.addWidget(disk_label)

        self.setLayout(layout)


app = QApplication(sys.argv)

window = GuardianWindow()

window.show()

sys.exit(app.exec())