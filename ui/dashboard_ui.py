import sys
import psutil
import platform
import pyqtgraph as pg
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, 
    QHBoxLayout, QFrame, QPushButton, QGridLayout, QScrollArea, QStackedWidget
)

# -------------------------------------------------------------
# BACKEND CORE INTERFACES
# -------------------------------------------------------------
try:
    from modules.network import local_ip, public_ip, active_connections
except ImportError:
    def local_ip(): return "127.0.0.1"
    def public_ip(): return "Fetching..."
    def active_connections(): return len(psutil.net_connections())

try:
    from modules.processes import top_processes
except ImportError:
    def top_processes(): 
        apps = []
        for proc in psutil.process_iter(['name', 'memory_percent', 'cpu_percent']):
            try: apps.append(proc.info)
            except: pass
        apps.sort(key=lambda x: x['memory_percent'] if x['memory_percent'] else 0, reverse=True)
        return apps[:5]

# ACTUAL PAGES IMPORTS
try:
    from ui.security_page import SecurityPage
    from ui.system_monitor_page import SystemMonitorPage
    from ui.network_page import NetworkPage
    from ui.process_page import ProcessPage
    from ui.startup_page import StartupPage
    from ui.settings_page import SettingsPage
except ImportError:
    pass

class SimplePage(QWidget):
    def __init__(self, title_text):
        super().__init__()
        self.setStyleSheet("background-color: #0b0f19;")
        lay = QVBoxLayout(self)
        lbl = QLabel(title_text)
        lbl.setStyleSheet("font-size: 34px; font-weight: bold; color: white;")
        lay.addWidget(lbl)
        lay.addStretch()

# ==========================================
# CUSTOM DONUT CHART ENGINE
# ==========================================
class DonutProgress(QWidget):
    def __init__(self, color_hex, size=130):
        super().__init__()
        self.setFixedSize(size, size)
        self.value = 0
        self.color = QColor(color_hex)
        self.bg_color = QColor("#1e293b")

    def set_value(self, val):
        self.value = val
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(12, 12, self.width() - 24, self.height() - 24)
        pen_width = 12
        
        bg_pen = QPen(self.bg_color, pen_width)
        bg_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(rect, 0, 360 * 16)
        
        fg_pen = QPen(self.color, pen_width)
        fg_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(fg_pen)
        span_angle = int(-self.value * 3.6 * 16)
        painter.drawArc(rect, 90 * 16, span_angle)
        
        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Segoe UI", 16, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, f"{int(self.value)}%\nUsed")
        painter.end()


# ==========================================
# MASTER CONSOLE WINDOW CONTROLLER
# ==========================================
class DashboardUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AKS Guardian AI v3.0.0")
        self.resize(1600, 900) 
        self.cpu_history = [0] * 60
        self.last_net_io = psutil.net_io_counters() # For real network speed calculation
        
        # EXACT PIXEL-PERFECT CSS (NO HTML RELIANCE)
        self.setStyleSheet("""
            QMainWindow { background-color: #0A0F1C; }
            QScrollArea { border: none; background-color: transparent; }
            QWidget#scroll_content { background-color: #0A0F1C; }
            QLabel { color: #ffffff; font-family: 'Segoe UI', system-ui, sans-serif; }
            
            QFrame#card { 
                background-color: #121927; 
                border-radius: 12px; 
                border: 1px solid #1E2638;
            }
            QFrame#card:hover { border: 1px solid #3b82f6; }
            
            QPushButton#navBtn { 
                text-align: left; background: transparent; border: none; 
                padding: 10px 16px; font-size: 13px; color: #9ca3af; font-weight: 500;
                border-radius: 8px; margin-bottom: 2px;
            } 
            QPushButton#navBtn:hover { background-color: #161F33; color: #ffffff; }
            QPushButton#navBtn:checked { 
                background-color: #162444; color: #3b82f6; font-weight: bold; 
                border-left: 4px solid #3b82f6; border-top-left-radius: 4px; border-bottom-left-radius: 4px;
            }
            
            QPushButton#actionBtn {
                background-color: #161D2B; color: #d1d5db; border: 1px solid #1E2638;
                padding: 12px; border-radius: 8px; font-weight: 500; font-size: 12px;
            }
            QPushButton#actionBtn:hover { background-color: #1E2638; border-color: #3b82f6; color: white; }
            
            QPushButton#miniTab {
                background-color: transparent; color: #9ca3af; border: none; font-weight: bold; font-size: 11px; padding: 4px 8px;
            }
            QPushButton#miniTab:checked { background-color: #2563eb; color: white; border-radius: 6px; }
        """)
        
        self.setup_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000)

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        base_layout = QHBoxLayout(main_widget)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.setSpacing(0)
        
        # 1. SIDEBAR
        sidebar = QFrame()
        sidebar.setStyleSheet("QFrame { background-color: #0B101E; border-right: 1px solid #1E2638; }")
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 25, 15, 20)
        
        brand_lbl = QLabel("🛡️ AKS Guardian AI")
        brand_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #f3f4f6; margin-bottom: 2px;")
        sub_brand = QLabel("Your AI System Guardian")
        sub_brand.setStyleSheet("color: #6b7280; font-size: 11px; margin-bottom: 15px;")
        
        status_frame = QFrame()
        status_frame.setStyleSheet("background-color: #064E3B; border-radius: 12px; padding: 6px;")
        status_lbl = QLabel("🟢 System Online")
        status_lbl.setStyleSheet("color: #34D399; font-size: 12px; font-weight: bold;")
        s_lay = QHBoxLayout(status_frame)
        s_lay.setContentsMargins(10,2,10,2)
        s_lay.addWidget(status_lbl)
        
        sidebar_layout.addWidget(brand_lbl)
        sidebar_layout.addWidget(sub_brand)
        sidebar_layout.addWidget(status_frame)
        sidebar_layout.addSpacing(15)
        
        nav_items = [
            "📊 Dashboard", "🛡️ Security Center", "⚙️ System Monitor", "🌐 Network Monitor", 
            "📂 Process Manager", "🚀 Startup Manager", "⚡ Self-Healing", 
            "💻 Hardware Info", "🔌 USB Monitor", "📄 Reports", "🤖 AI Assistant", "🛠 Settings"
        ]
        
        self.nav_buttons = []
        for idx, text in enumerate(nav_items):
            btn = QPushButton(text)
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            if idx == 0: btn.setChecked(True)
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        sidebar_layout.addStretch()
        base_layout.addWidget(sidebar)
        
        # 2. MAIN DASHBOARD AREA
        self.page_container = QStackedWidget()
        base_layout.addWidget(self.page_container)
        
        self.dashboard_view = QWidget()
        self.build_full_dashboard()
        self.page_container.addWidget(self.dashboard_view)

    def build_full_dashboard(self):
        dash_main_lay = QVBoxLayout(self.dashboard_view)
        dash_main_lay.setContentsMargins(0, 0, 0, 0)
        dash_main_lay.setSpacing(0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_content")
        
        split_layout = QHBoxLayout(scroll_content)
        split_layout.setContentsMargins(25, 20, 25, 20)
        split_layout.setSpacing(20)
        
        # Left Content Wrapper
        left_col = QVBoxLayout()
        left_col.setSpacing(15)
        
        # Right Sidebar Wrapper (Fixed Width)
        right_wrapper = QWidget()
        right_wrapper.setFixedWidth(320)
        right_col = QVBoxLayout(right_wrapper)
        right_col.setContentsMargins(0, 0, 0, 0)
        right_col.setSpacing(15)
        
        # ==============================================================
        # LEFT COLUMN: THE CORE DASHBOARD
        # ==============================================================
        
        # HEADER (No HTML span leaking)
        header_lay = QHBoxLayout()
        h_text_v = QVBoxLayout()
        h_title = QLabel("Dashboard")
        h_title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        h_sub = QLabel("Real-time overview of your system health and security")
        h_sub.setStyleSheet("font-size: 13px; color: #9ca3af;")
        h_text_v.addWidget(h_title)
        h_text_v.addWidget(h_sub)
        header_lay.addLayout(h_text_v)
        header_lay.addStretch()
        
        header_lay.addWidget(QLabel("Last Updated: Live 🔄"))
        scan_btn = QPushButton("🔄 Run AI Scan")
        scan_btn.setStyleSheet("background-color: #2563eb; color: white; padding: 8px 16px; border-radius: 6px; font-weight: bold; border:none;")
        header_lay.addWidget(scan_btn)
        left_col.addLayout(header_lay)
        
        # --- ROW 1: TOP 5 METRICS ---
        row1 = QHBoxLayout()
        self.cpu_card, self.cpu_val, self.cpu_sub = self.create_top_card("CPU Usage", "0.0%", "#3b82f6", platform.processor()[:15])
        self.ram_card, self.ram_val, self.ram_sub = self.create_top_card("RAM Usage", "0.0%", "#a855f7", "Calculating...")
        self.disk_card, self.disk_val, self.disk_sub = self.create_top_card("Disk Usage", "0.0%", "#10b981", "Calculating...")
        self.sec_card, self.sec_val, self.sec_sub = self.create_top_card("Security Score", "95/100", "#10b981", "🟢 LOW RISK")
        self.up_card, self.up_val, self.up_sub = self.create_top_card("System Uptime", "0d 4h 32m", "#10b981", "Running Smoothly")
        
        for card in [self.cpu_card, self.ram_card, self.disk_card, self.sec_card, self.up_card]:
            row1.addWidget(card)
        left_col.addLayout(row1)
        
        # --- ROW 2: GRAPH, DONUTS, SECURITY LIST ---
        row2 = QHBoxLayout()
        
        # Graph Frame
        g_frame = QFrame()
        g_frame.setObjectName("card")
        g_lay = QVBoxLayout(g_frame)
        g_lay.setContentsMargins(15,15,15,15)
        
        g_title = QLabel("Live System Monitor")
        g_title.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        g_lay.addWidget(g_title)
        
        tabs_lay = QHBoxLayout()
        for t in ["CPU", "RAM", "Disk", "Network"]:
            btn = QPushButton(t)
            btn.setObjectName("miniTab")
            btn.setCheckable(True)
            if t == "CPU": btn.setChecked(True)
            tabs_lay.addWidget(btn)
        tabs_lay.addStretch()
        g_lay.addLayout(tabs_lay)
        
        self.graph = pg.PlotWidget()
        self.graph.setBackground("#121927")
        self.graph.showGrid(x=True, y=True, alpha=0.1)
        self.graph.getAxis('left').setPen('#1E2638')
        self.graph.getAxis('bottom').setPen('#1E2638')
        self.curve = self.graph.plot(pen=pg.mkPen(color="#3b82f6", width=2))
        g_lay.addWidget(self.graph)
        row2.addWidget(g_frame, stretch=2)
        
        # RAM Donut
        r_frame = QFrame()
        r_frame.setObjectName("card")
        r_lay = QVBoxLayout(r_frame)
        r_title = QLabel("Memory Usage")
        r_title.setStyleSheet("font-size: 13px; font-weight: bold; color: white;")
        r_lay.addWidget(r_title, alignment=Qt.AlignTop)
        
        self.ram_donut = DonutProgress("#a855f7", 120)
        r_lay.addWidget(self.ram_donut, alignment=Qt.AlignCenter)
        self.ram_donut_sub = QLabel("Used: -- GB\nTotal: -- GB")
        self.ram_donut_sub.setStyleSheet("color: #9ca3af; font-size: 11px;")
        r_lay.addWidget(self.ram_donut_sub)
        row2.addWidget(r_frame, stretch=1)
        
        # Disk Donut
        d_frame = QFrame()
        d_frame.setObjectName("card")
        d_lay = QVBoxLayout(d_frame)
        d_title = QLabel("Disk Usage (C:)")
        d_title.setStyleSheet("font-size: 13px; font-weight: bold; color: white;")
        d_lay.addWidget(d_title, alignment=Qt.AlignTop)
        
        self.disk_donut = DonutProgress("#10b981", 120)
        d_lay.addWidget(self.disk_donut, alignment=Qt.AlignCenter)
        self.disk_donut_sub = QLabel("Used: -- GB\nTotal: -- GB")
        self.disk_donut_sub.setStyleSheet("color: #9ca3af; font-size: 11px;")
        d_lay.addWidget(self.disk_donut_sub)
        row2.addWidget(d_frame, stretch=1)
        
        left_col.addLayout(row2)
        
        # --- ROW 3: PROCESSES, NETWORK, ACTIONS ---
        row3 = QHBoxLayout()
        
        proc_f = QFrame()
        proc_f.setObjectName("card")
        self.p_lay = QVBoxLayout(proc_f)
        pt = QLabel("Top Processes (By CPU)")
        pt.setStyleSheet("font-size: 13px; font-weight: bold; color: white;")
        self.p_lay.addWidget(pt, alignment=Qt.AlignTop)
        row3.addWidget(proc_f, stretch=1)
        
        # Pure Qt Network Overview (No HTML)
        net_f = QFrame()
        net_f.setObjectName("card")
        n_lay = QVBoxLayout(net_f)
        nt = QLabel("Network Overview")
        nt.setStyleSheet("font-size: 13px; font-weight: bold; color: white;")
        n_lay.addWidget(nt, alignment=Qt.AlignTop)
        
        nn_h1 = QHBoxLayout()
        dn_v = QVBoxLayout()
        dn_v.addWidget(self.create_lbl("Download", "#9ca3af", 11))
        self.lbl_dl = self.create_lbl("0.0 Mbps", "white", 16, True)
        dn_v.addWidget(self.lbl_dl)
        
        up_v = QVBoxLayout()
        up_v.addWidget(self.create_lbl("Upload", "#9ca3af", 11))
        self.lbl_up = self.create_lbl("0.0 Mbps", "white", 16, True)
        up_v.addWidget(self.lbl_up)
        
        nn_h1.addLayout(dn_v)
        nn_h1.addLayout(up_v)
        n_lay.addLayout(nn_h1)
        
        nn_h2 = QHBoxLayout()
        c_v = QVBoxLayout()
        c_v.addWidget(self.create_lbl("Connections", "#9ca3af", 11))
        self.lbl_conn = self.create_lbl("0 Active", "white", 14, True)
        c_v.addWidget(self.lbl_conn)
        
        ip_v = QVBoxLayout()
        ip_v.addWidget(self.create_lbl("IP Address", "#9ca3af", 11))
        self.lbl_ip = self.create_lbl(local_ip(), "white", 14, True)
        ip_v.addWidget(self.lbl_ip)
        
        nn_h2.addLayout(c_v)
        nn_h2.addLayout(ip_v)
        n_lay.addLayout(nn_h2)
        row3.addWidget(net_f, stretch=1)
        
        # Self Healing (Actions)
        act_f = QFrame()
        act_f.setObjectName("card")
        a_lay = QVBoxLayout(act_f)
        at = QLabel("Self-Healing Quick Actions")
        at.setStyleSheet("font-size: 13px; font-weight: bold; color: white;")
        a_lay.addWidget(at, alignment=Qt.AlignTop)
        
        grid_btns = QGridLayout()
        btns_list = [("🧹 Clean Temp Files",1,1), ("🌐 Flush DNS",1,2), ("🗑 Empty Recycle Bin",1,3), 
                     ("🔄 Clear Browser Cache",2,1), ("🚀 Optimize Startup",2,2), ("⚙️ Repair Windows",2,3)]
        for text, r, c in btns_list:
            b = QPushButton(text)
            b.setObjectName("actionBtn")
            grid_btns.addWidget(b, r, c)
        a_lay.addLayout(grid_btns)
        row3.addWidget(act_f, stretch=1)
        
        left_col.addLayout(row3)
        
        # --- ROW 4: HARDWARE, BATTERY, STARTUP ---
        row4 = QHBoxLayout()
        
        hw_f = QFrame()
        hw_f.setObjectName("card")
        hw_lay = QVBoxLayout(hw_f)
        ht = QLabel("Hardware Information")
        ht.setStyleSheet("font-size: 13px; font-weight: bold; color: white;")
        hw_lay.addWidget(ht)
        
        hw_grid = QGridLayout()
        total_ram = f"{round(psutil.virtual_memory().total / (1024**3))} GB DDR4"
        hw_items = [("⚙️", "CPU", platform.processor()[:18]), ("💾", "RAM", total_ram), 
                    ("💻", "System", platform.system() + " " + platform.release())]
        
        for i, (ic, tit, sub) in enumerate(hw_items):
            v = QVBoxLayout()
            v.addWidget(self.create_lbl(f"{ic} {tit}", "#9ca3af", 11))
            v.addWidget(self.create_lbl(sub, "white", 12, True))
            hw_grid.addLayout(v, i, 0)
        hw_lay.addLayout(hw_grid)
        row4.addWidget(hw_f, stretch=1)
        
        # Battery Health (Pure Qt)
        bat_f = QFrame()
        bat_f.setObjectName("card")
        bat_lay = QVBoxLayout(bat_f)
        bt = QLabel("Battery Health")
        bt.setStyleSheet("font-size: 13px; font-weight: bold; color: white;")
        bat_lay.addWidget(bt)
        
        has_battery = psutil.sensors_battery()
        bat_percent = f"{has_battery.percent}%" if has_battery else "N/A"
        bat_status = "Charging" if has_battery and has_battery.power_plugged else "Discharging"
        
        bh_lay = QHBoxLayout()
        bh_lay.addWidget(self.create_lbl("🔋", "white", 24))
        b_val_v = QVBoxLayout()
        b_val_v.addWidget(self.create_lbl(bat_percent, "#10b981", 24, True))
        b_val_v.addWidget(self.create_lbl(bat_status, "#9ca3af", 11))
        bh_lay.addLayout(b_val_v)
        bat_lay.addLayout(bh_lay)
        row4.addWidget(bat_f, stretch=1)
        
        left_col.addLayout(row4)
        
        # ==============================================================
        # RIGHT COLUMN: ALERTS & AI RECS
        # ==============================================================
        
        # Live Alerts
        alert_f = QFrame()
        alert_f.setObjectName("card")
        alert_lay = QVBoxLayout(alert_f)
        alt = QLabel("Live Alerts")
        alt.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        alert_lay.addWidget(alt)
        
        alerts = [
            ("⚠️", "High RAM Usage", "Memory optimization needed", "#ef4444", "08:08 PM"),
            ("🔄", "Windows Update", "Updates available", "#3b82f6", "08:03 PM")
        ]
        for ic, tit, sub, col, t in alerts:
            al_h = QHBoxLayout()
            al_h.addWidget(self.create_lbl(ic, "white", 16))
            al_v = QVBoxLayout()
            al_v.addWidget(self.create_lbl(tit, col, 12, True))
            al_v.addWidget(self.create_lbl(sub, "#9ca3af", 10))
            al_h.addLayout(al_v)
            al_h.addStretch()
            al_h.addWidget(self.create_lbl(t, "#6b7280", 10))
            alert_lay.addLayout(al_h)
            
        right_col.addWidget(alert_f)
        
        # AI Recommendations
        ai_f = QFrame()
        ai_f.setObjectName("card")
        ai_lay = QVBoxLayout(ai_f)
        ait = QLabel("AI Recommendations")
        ait.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        ai_lay.addWidget(ait)
        
        recs = [
            ("🧠", "High memory usage detected", "Close unused applications"),
            ("🛑", "Disable startup apps", "3 apps can be disabled"),
            ("🗑️", "Clear temporary files", "3.2 GB can be cleaned")
        ]
        for ic, tit, sub in recs:
            ai_h = QHBoxLayout()
            ai_h.addWidget(self.create_lbl(ic, "white", 16))
            ai_v = QVBoxLayout()
            ai_v.addWidget(self.create_lbl(tit, "#d1d5db", 12))
            ai_v.addWidget(self.create_lbl(sub, "#9ca3af", 10))
            ai_h.addLayout(ai_v)
            ai_lay.addLayout(ai_h)
            
        ai_btn = QPushButton("✨ Run AI Optimization")
        ai_btn.setStyleSheet("background-color: #6d28d9; color: white; padding: 12px; border-radius: 8px; font-weight: bold; margin-top: 10px; border:none;")
        ai_lay.addWidget(ai_btn)
        right_col.addWidget(ai_f)
        
        right_col.addStretch()
        
        # ASSEMBLE
        split_layout.addLayout(left_col, stretch=4)
        split_layout.addWidget(right_wrapper, stretch=1)
        
        scroll_area.setWidget(scroll_content)
        dash_main_lay.addWidget(scroll_area)

    def create_lbl(self, text, color, size, bold=False):
        l = QLabel(text)
        b = "font-weight: bold;" if bold else ""
        l.setStyleSheet(f"color: {color}; font-size: {size}px; {b}")
        return l

    def create_top_card(self, title, value, color, subtext=""):
        frame = QFrame()
        frame.setObjectName("card")
        lay = QVBoxLayout(frame)
        lay.setContentsMargins(16, 16, 16, 16)
        
        t = self.create_lbl(title, "#9ca3af", 11, True)
        lay.addWidget(t)
        
        v = self.create_lbl(value, color, 28, True)
        lay.addWidget(v)
        
        s = self.create_lbl(subtext, "#6b7280", 11)
        lay.addWidget(s)
        return frame, v, s

    def switch_page(self, index):
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)
        self.page_container.setCurrentIndex(index)

    def update_stats(self):
        try:
            # CPU & RAM Fetch
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage("C:\\")
            
            # Top Cards
            self.cpu_val.setText(f"{cpu}%")
            self.ram_val.setText(f"{ram.percent}%")
            self.ram_sub.setText(f"{round(ram.used/(1024**3), 1)} / {round(ram.total/(1024**3), 1)} GB")
            self.disk_val.setText(f"{disk.percent}%")
            self.disk_sub.setText(f"{round(disk.used/(1024**3), 1)} / {round(disk.total/(1024**3), 1)} GB")
            
            # Graph
            self.cpu_history.append(cpu)
            if len(self.cpu_history) > 60: self.cpu_history.pop(0)
            self.curve.setData(self.cpu_history)
            
            # Donuts
            self.ram_donut.set_value(ram.percent)
            self.ram_donut_sub.setText(f"Used: {round(ram.used/(1024**3), 1)} GB\nTotal: {round(ram.total/(1024**3), 1)} GB")
            
            self.disk_donut.set_value(disk.percent)
            self.disk_donut_sub.setText(f"Used: {round(disk.used/(1024**3), 1)} GB\nTotal: {round(disk.total/(1024**3), 1)} GB")
            
            # REAL Network Speed Calculation
            new_net = psutil.net_io_counters()
            dl_mbps = (new_net.bytes_recv - self.last_net_io.bytes_recv) / 1024 / 1024 * 8 / 2 # 2 seconds interval
            ul_mbps = (new_net.bytes_sent - self.last_net_io.bytes_sent) / 1024 / 1024 * 8 / 2
            self.last_net_io = new_net
            
            self.lbl_dl.setText(f"{dl_mbps:.1f} Mbps")
            self.lbl_up.setText(f"{ul_mbps:.1f} Mbps")
            self.lbl_conn.setText(f"{len(psutil.net_connections())} Active")
            
            # Real Processes
            for i in reversed(range(1, self.p_lay.count())): 
                w = self.p_lay.itemAt(i).widget()
                if w: w.setParent(None)
            
            procs = top_processes()
            for p in procs[:4]:
                lbl = self.create_lbl(f"🛡 {p.get('name', 'Unknown')}    {p.get('cpu_percent', 0):.1f}% CPU    {p.get('memory_percent', 0):.1f}% RAM", "#d1d5db", 12)
                self.p_lay.addWidget(lbl)
            self.p_lay.addStretch()

        except Exception as e:
            print("Update Error:", e)