from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)


class USBPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            background:#0b0f19;
            color:white;
        """)

        layout = QVBoxLayout(self)

        title = QLabel(
            "USB Monitor"
        )

        title.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        info = QLabel(
            "USB monitoring module ready."
        )

        layout.addWidget(info)