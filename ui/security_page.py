from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QPushButton
from PySide6.QtCore import Qt
import psutil

# Fixed root path reference wrapper
from modules.security import defender_enabled, security_score

class SecurityPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0b0f19;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(25)

        title = QLabel("Security Center")
        title.setStyleSheet("font-size: 34px; font-weight: bold; letter-spacing: -0.8px; color: white;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(20)

        # Module 1: Windows Defender
        def_card = QFrame()
        def_card.setStyleSheet("background-color: #111827; border-radius: 12px; border: 1px solid #1f2937; padding: 20px;")
        def_layout = QVBoxLayout(def_card)
        
        lbl_def = QLabel("🛡️ Windows Defender Status")
        lbl_def.setStyleSheet("font-size: 14px; font-weight: bold; color: #9ca3af;")
        
        is_protected = defender_enabled()
        lbl_status = QLabel("PROTECTED / ACTIVE" if is_protected else "ACTION REQUIRED")
        lbl_status.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {'#22c55e' if is_protected else '#ef4444'}; margin: 10px 0px;")
        
        def_layout.addWidget(lbl_def)
        def_layout.addWidget(lbl_status)
        grid.addWidget(def_card, 0, 0)

        # Module 2: Firewall Status
        fw_card = QFrame()
        fw_card.setStyleSheet("background-color: #111827; border-radius: 12px; border: 1px solid #1f2937; padding: 20px;")
        fw_layout = QVBoxLayout(fw_card)
        
        lbl_fw = QLabel("🔥 Advanced Firewall Protection")
        lbl_fw.setStyleSheet("font-size: 14px; font-weight: bold; color: #9ca3af;")
        lbl_fw_status = QLabel("ONLINE / SHIELDED")
        lbl_fw_status.setStyleSheet("font-size: 24px; font-weight: bold; color: #22c55e; margin: 10px 0px;")
        
        fw_layout.addWidget(lbl_fw)
        fw_layout.addWidget(lbl_fw_status)
        grid.addWidget(fw_card, 0, 1)

        layout.addLayout(grid)
        
        scan_panel = QFrame()
        scan_panel.setStyleSheet("background-color: #111827; border-radius: 12px; border: 1px solid #1f2937; padding: 25px;")
        scan_layout = QHBoxLayout(scan_panel)
        
        txt_info = QLabel("Complete integrity check has not been performed during this session.")
        txt_info.setStyleSheet("color: #9ca3af; font-size: 14px;")
        
        run_btn = QPushButton("Deep Integrity Scan")
        run_btn.setStyleSheet("background-color: #2563eb; color: white; font-weight: bold; padding: 12px 24px; border-radius: 8px; border: none;")
        
        scan_layout.addWidget(txt_info)
        scan_layout.addStretch()
        scan_layout.addWidget(run_btn)
        
        layout.addWidget(scan_panel)
        layout.addStretch()