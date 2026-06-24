from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QCheckBox, QPushButton
from PySide6.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0b0f19;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(25)

        title = QLabel("Settings Configuration")
        title.setStyleSheet("font-size: 34px; font-weight: bold; letter-spacing: -0.8px; color: white;")
        layout.addWidget(title)

        panel = QFrame()
        panel.setStyleSheet("background-color: #111827; border-radius: 12px; border: 1px solid #1f2937; padding: 25px;")
        vbox = QVBoxLayout(panel)
        vbox.setSpacing(18)

        # Mock Checkboxes configurations
        cb1 = QCheckBox("Enable Background Real-time Telemetry Processing Engine")
        cb2 = QCheckBox("Execute Predictive AI Diagnostics Cycles on Startup Session")
        cb3 = QCheckBox("Automated Deep Cache Scrubbing on Critical Resource Flags")
        
        for cb in [cb1, cb2, cb3]:
            cb.setStyleSheet("QCheckBox { color: #d1d5db; font-size: 14px; spacing: 10px; } QCheckBox::indicator { width: 18px; height: 18px; }")
            vbox.addWidget(cb)
            
        vbox.addStretch()
        
        save_btn = QPushButton("Save Environment Constants")
        save_btn.setFixedWidth(240)
        save_btn.setStyleSheet("background-color: #2563eb; color: white; font-weight: bold; padding: 12px; border-radius: 8px; border: none;")
        vbox.addWidget(save_btn)

        layout.addWidget(panel)
        layout.addStretch()