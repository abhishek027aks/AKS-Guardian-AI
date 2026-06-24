from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)

from modules.process_manager import (
    top_processes
)


class ProcessPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            background:#0b0f19;
            color:white;
        """)

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel(
            "Process Manager"
        )

        title.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        card = QFrame()

        card.setStyleSheet("""
            background:#111827;
            border-radius:12px;
            padding:20px;
        """)

        vbox = QVBoxLayout(card)

        processes = top_processes()[:10]

        for proc in processes:

            row = QHBoxLayout()

            name = QLabel(
                proc["name"]
            )

            ram = QLabel(
                f"{proc['memory_percent']:.2f}%"
            )

            row.addWidget(name)

            row.addStretch()

            row.addWidget(ram)

            vbox.addLayout(row)

        layout.addWidget(card)