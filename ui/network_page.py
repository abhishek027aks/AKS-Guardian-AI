from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QGridLayout
from network import local_ip, public_ip, active_connections, open_ports

class NetworkPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0b0f19;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(25)

        title = QLabel("Network Monitor")
        title.setStyleSheet("font-size: 34px; font-weight: bold; letter-spacing: -0.8px; color: white;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(20)

        # Local Parameters block
        card1 = QFrame()
        card1.setStyleSheet("background-color: #111827; border-radius: 12px; border: 1px solid #1f2937; padding: 20px;")
        vbox1 = QVBoxLayout(card1)
        lbl1 = QLabel("NIC Local Address")
        lbl1.setStyleSheet("color: #9ca3af; font-size: 13px;")
        val1 = QLabel(local_ip())
        val1.setStyleSheet("color: #3b82f6; font-size: 22px; font-weight: bold; font-family: 'Consolas'; margin-top: 5px;")
        vbox1.addWidget(lbl1)
        vbox1.addWidget(val1)
        grid.addWidget(card1, 0, 0)

        # Public Gateways block
        card2 = QFrame()
        card2.setStyleSheet("background-color: #111827; border-radius: 12px; border: 1px solid #1f2937; padding: 20px;")
        vbox2 = QVBoxLayout(card2)
        lbl2 = QLabel("External Public IP WAN")
        lbl2.setStyleSheet("color: #9ca3af; font-size: 13px;")
        val2 = QLabel(public_ip())
        val2.setStyleSheet("color: #10b981; font-size: 22px; font-weight: bold; font-family: 'Consolas'; margin-top: 5px;")
        vbox2.addWidget(lbl2)
        vbox2.addWidget(val2)
        grid.addWidget(card2, 0, 1)

        layout.addLayout(grid)
        
        # Socket Tracker
        ports_card = QFrame()
        ports_card.setStyleSheet("background-color: #111827; border-radius: 12px; border: 1px solid #1f2937; padding: 22px;")
        ports_vbox = QVBoxLayout(ports_card)
        p_title = QLabel("🔓 Active Listening Socket Ports Topology")
        p_title.setStyleSheet("font-weight: bold; font-size: 15px; color: white; margin-bottom: 8px;")
        ports_vbox.addWidget(p_title)
        
        active_ports = open_ports()
        if active_ports:
            ports_lbl = QLabel(", ".join(map(str, active_ports[:25])))
        else:
            ports_lbl = QLabel("No unsecured open sockets ports detected.")
        ports_lbl.setStyleSheet("color: #d1d5db; font-family: 'Consolas'; font-size: 14px;")
        ports_vbox.addWidget(ports_lbl)
        
        layout.addWidget(ports_card)
        layout.addStretch()