import sys
import psutil
import pyqtgraph as pg
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, 
    QHBoxLayout, QFrame, QPushButton, QGridLayout, QStackedWidget
)

# Backend modules integrations
from network import local_ip, public_ip, active_connections
from processes import top_processes

# Subpages UI structure layouts loading 
from ui.security_page import SecurityPage
from ui.network_page import NetworkPage
from ui.process_page import ProcessPage
from ui.settings_page import SettingsPage


class DashboardUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AKS Guardian AI v3.0.0")
        self.resize(1360, 780)
        
        # Datastream historical sequence pipeline tracking
        self.cpu_history = [0] * 60
        
        # Premium Deep Glassmorphic Custom Style Matrix Engine
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #0b0f19; 
            }
            QLabel { 
                color: #ffffff; 
                font-family: 'Segoe UI', -apple-system, sans-serif; 
            }
            QFrame#cardFrame { 
                background-color: #111827; 
                border-radius: 12px; 
                border: 1px solid #1f2937;
            }
            QFrame#cardFrame:hover {
                border: 1px solid #3b82f6;
            }
            QPushButton#navBtn { 
                text-align: left; 
                background: transparent; 
                border: none; 
                padding: 13px 18px; 
                font-size: 14px; 
                color: #9ca3af;
                font-weight: 500;
            } 
            QPushButton#navBtn:hover { 
                background-color: #111827; 
                color: #ffffff; 
                border-radius: 8px; 
            }
            QPushButton#navBtn:checked {
                background-color: #1e293b;
                color: #3b82f6;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton#actionBtn {
                background-color: #1f2937; 
                color: #f3f4f6; 
                border: 1px solid #374151;
                padding: 10px 20px; 
                border-radius: 8px; 
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton#actionBtn:hover {
                background-color: #2563eb; 
                border-color: #60a5fa; 
                color: white;
            }
        """)
        
        self.setup_ui()
        
        # Core async execution clock cycle tracking thread
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000)

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        base_layout = QHBoxLayout(main_widget)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.setSpacing(0)
        
        # -------------------------------------------------------------
        # SIDEBAR PANEL (Width adjusted to prevent title clipping)
        # -------------------------------------------------------------
        sidebar = QFrame()
        sidebar.setStyleSheet("QFrame { background-color: #070a13; border: none; border-right: 1px solid #111827; border-radius: 0px; }")
        sidebar.setFixedWidth(275) # Fixed: title text layout boundary truncation resolved
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(22, 25, 22, 25)
        
        brand_label = QLabel("🛡️ AKS Guardian AI")
        brand_label.setStyleSheet("font-size: 23px; font-weight: bold; color: #3b82f6; letter-spacing: 0.5px;")
        
        status_label = QLabel("● System Online")
        status_label.setStyleSheet("color: #22c55e; font-size: 13px; font-weight: bold; margin-bottom: 30px; margin-left: 2px;")
        
        sidebar_layout.addWidget(brand_label)
        sidebar_layout.addWidget(status_label)
        
        # Stack routing dynamic map lists configuration
        self.nav_buttons = []
        nav_items = [
            ("📊   Dashboard", 0),
            ("🛡️   Security Center", 1),
            ("⚙️   System Monitor", 2),
            ("🌐   Network Monitor", 3),
            ("🛠   Settings", 4)
        ]
        
        for item_text, index in nav_items:
            btn = QPushButton(item_text)
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            if index == 0:
                btn.setChecked(True)
                
            btn.clicked.connect(lambda checked=False, idx=index: self.switch_page(idx))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        sidebar_layout.addStretch()
        base_layout.addWidget(sidebar)
        
        # -------------------------------------------------------------
        # MULTI-PAGE VIEW MANAGER (QStackedWidget Framework Layer)
        # -------------------------------------------------------------
        self.page_container = QStackedWidget()
        base_layout.addWidget(self.page_container)
        
        # Construct dynamic dashboard homepage content workspace node
        self.dashboard_view = QWidget()
        self.setup_dashboard_view()
        
        # Inject individual external structural layouts into container stack index slots
        self.page_container.addWidget(self.dashboard_view)          # Index 0
        self.page_container.addWidget(SecurityPage())               # Index 1
        self.page_container.addWidget(ProcessPage())                # Index 2
        self.page_container.addWidget(NetworkPage())                 # Index 3
        self.page_container.addWidget(SettingsPage())                # Index 4

    def setup_dashboard_view(self):
        content_vbox = QVBoxLayout(self.dashboard_view)
        content_vbox.setContentsMargins(30, 25, 30, 25)
        content_vbox.setSpacing(20)
        
        # Header Row Layout Matrix
        header_layout = QHBoxLayout()
        header_title = QLabel("Dashboard")
        header_title.setStyleSheet("font-size: 32px; font-weight: bold; letter-spacing: -0.5px;")
        
        scan_btn = QPushButton("⚙️ Run AI Scan")
        scan_btn.setStyleSheet("""
            QPushButton { 
                background-color: #2563eb; 
                color: white; 
                border: none; 
                padding: 10px 22px; 
                font-size: 13px; 
                border-radius: 8px;
                font-weight: bold;
            } 
            QPushButton:hover { background-color: #1d4ed8; }
        """)
        
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        header_layout.addWidget(scan_btn)
        content_vbox.addLayout(header_layout)
        
        # Top Cards Data Metrics Grid Panels Row
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        self.cpu_card = self.create_card("CPU USAGE", "0.0%", "Intel Core i5", "#3b82f6")
        self.ram_card = self.create_card("RAM USAGE", "0.0%", "Available: --", "#a855f7")
        self.disk_card = self.create_card("DISK USAGE", "0.0%", "Drive C:\\", "#10b981")
        self.security_card = self.create_card("SECURITY SCORE", "95/100", "🟢 LOW RISK", "#ec4899")
        
        grid_layout.addWidget(self.cpu_card, 0, 0)
        grid_layout.addWidget(self.ram_card, 0, 1)
        grid_layout.addWidget(self.disk_card, 0, 2)
        grid_layout.addWidget(self.security_card, 0, 3)
        content_vbox.addLayout(grid_layout)
        
        # Telemetry Graph Tracking + Functional Macro Button Block Section
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(20)
        
        graph_frame = QFrame()
        graph_frame.setObjectName("cardFrame")
        graph_vbox = QVBoxLayout(graph_frame)
        graph_vbox.setContentsMargins(18, 18, 18, 18)
        
        g_title = QLabel("📈 Live System Monitor")
        g_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #f3f4f6; margin-bottom: 10px;")
        graph_vbox.addWidget(g_title)
        
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground("#111827")
        self.graph_widget.showGrid(x=True, y=True, alpha=0.15)
        self.graph_widget.getAxis('left').setPen('#374151')
        self.graph_widget.getAxis('bottom').setPen('#374151')
        
        self.graph_curve = self.graph_widget.plot(pen=pg.mkPen(color="#3b82f6", width=2.5))
        graph_vbox.addWidget(self.graph_widget)
        middle_layout.addWidget(graph_frame, stretch=2)
        
        actions_frame = QFrame()
        actions_frame.setObjectName("cardFrame")
        actions_vbox = QVBoxLayout(actions_frame)
        actions_vbox.setContentsMargins(18, 18, 18, 18)
        actions_vbox.setSpacing(12)
        
        a_title = QLabel("⚡ Self-Healing Quick Actions")
        a_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #f3f4f6; margin-bottom: 5px;")
        actions_vbox.addWidget(a_title)
        
        for btn_lbl in ["🧹   Clean Temp Files", "🌐   Flush DNS Cache", "📄   Export System Report"]:
            btn = QPushButton(btn_lbl)
            btn.setObjectName("actionBtn")
            actions_vbox.addWidget(btn)
        actions_vbox.addStretch()
        
        middle_layout.addWidget(actions_frame, stretch=1)
        content_vbox.addLayout(middle_layout)
        
        # Bottom Layout Information Feed Grids Block
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        
        proc_frame = QFrame()
        proc_frame.setObjectName("cardFrame")
        self.proc_vbox = QVBoxLayout(proc_frame)
        self.proc_vbox.setContentsMargins(18, 18, 18, 18)
        self.proc_vbox.setSpacing(10)
        
        p_title = QLabel("💾 Top Memory Processes")
        p_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #f3f4f6; margin-bottom: 5px;")
        self.proc_vbox.addWidget(p_title)
        bottom_layout.addWidget(proc_frame, stretch=1)
        
        net_frame = QFrame()
        net_frame.setObjectName("cardFrame")
        self.net_vbox = QVBoxLayout(net_frame)
        self.net_vbox.setContentsMargins(18, 18, 18, 18)
        self.net_vbox.setSpacing(12)
        
        n_title = QLabel("🌐 Network & Security Info")
        n_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #f3f4f6; margin-bottom: 5px;")
        self.net_vbox.addWidget(n_title)
        
        self.lbl_local_ip = QLabel("Local IP: Fetching...")
        self.lbl_public_ip = QLabel("Public IP: Fetching...")
        self.lbl_connections = QLabel("Active Connections: 0")
        
        for lbl in [self.lbl_local_ip, self.lbl_public_ip, self.lbl_connections]:
            lbl.setStyleSheet("color: #d1d5db; font-size: 13px; font-family: 'Consolas', monospace;")
            self.net_vbox.addWidget(lbl)
            
        self.net_vbox.addStretch()
        bottom_layout.addWidget(net_frame, stretch=1)
        content_vbox.addLayout(bottom_layout)

    def create_card(self, title, value, footer, highlight_color):
        card = QFrame()
        card.setObjectName("cardFrame")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("color: #9ca3af; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;")
        
        v_lbl = QLabel(value)
        v_lbl.setStyleSheet(f"color: {highlight_color}; font-size: 32px; font-weight: bold; margin: 4px 0px;")
        
        f_lbl = QLabel(footer)
        f_lbl.setStyleSheet("color: #6b7280; font-size: 12px;")
        
        layout.addWidget(t_lbl)
        layout.addWidget(v_lbl)
        layout.addWidget(f_lbl)
        
        card.value_label = v_lbl
        card.footer_label = f_lbl
        return card

    def switch_page(self, target_index):
        # Synchronize multi-button toggle states mapping
        for idx, btn in enumerate(self.nav_buttons):
            btn.setChecked(idx == target_index)
        self.page_container.setCurrentIndex(target_index)

    def update_stats(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage("C:\\")
            
            # Dynamic text updating via properties referencing
            self.cpu_card.value_label.setText(f"{cpu}%")
            self.ram_card.value_label.setText(f"{ram.percent}%")
            self.ram_card.footer_label.setText(f"{round(ram.used/(1024**3), 1)}GB / {round(ram.total/(1024**3), 1)}GB")
            self.disk_card.value_label.setText(f"{disk.percent}%")
            
            self.cpu_history.append(cpu)
            if len(self.cpu_history) > 60:
                self.cpu_history.pop(0)
            self.graph_curve.setData(self.cpu_history)
            
            self.lbl_local_ip.setText(f"Local IP:  {local_ip()}")
            self.lbl_public_ip.setText(f"Public IP: {public_ip()}")
            self.lbl_connections.setText(f"Active Connections: {active_connections()}")
            
            # Flush existing dynamic labels on current thread loop cleanly
            for i in reversed(range(1, self.proc_vbox.count())): 
                widget = self.proc_vbox.itemAt(i).widget()
                if widget: widget.setParent(None)
                
            procs = top_processes()[:4]
            for p in procs:
                lbl = QLabel(f"•  {p['name']} — {p['memory_percent']:.1f}% RAM")
                lbl.setStyleSheet("color: #d1d5db; font-size: 13px; font-family: 'Segoe UI';")
                self.proc_vbox.addWidget(lbl)
            self.proc_vbox.addStretch()
            
        except Exception as e:
            print(f"Error updating dynamic datastream loop: {e}")