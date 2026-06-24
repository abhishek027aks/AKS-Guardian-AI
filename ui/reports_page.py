from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)


class ReportsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            background:#0b0f19;
            color:white;
        """)

        layout = QVBoxLayout(self)

        title = QLabel(
            "Reports"
        )

        title.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        info = QLabel(
            "Report generation module coming soon..."
        )

        layout.addWidget(info)