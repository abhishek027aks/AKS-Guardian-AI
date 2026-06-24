import psutil
import pyqtgraph as pg
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame

# Assuming these are available in your directory structure
from modules.monitor import get_cpu, get_ram, get_disk, get_uptime


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()
        
        # Initialize history array
        self.cpu_history = [0] * 60
        
        # Set up UI elements first so graph_curve exists
        self.setup_ui()

        # Set up timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(1000)

    def update_dashboard(self):
        # Fallback to psutil if get_cpu() from monitor module doesn't match signatures
        try:
            cpu = get_cpu()
        except Exception:
            cpu = psutil.cpu_percent()

        self.cpu_history.append(cpu)

        if len(self.cpu_history) > 60:
            self.cpu_history.pop(0)

        self.graph_curve.setData(self.cpu_history)

    def card(self, title, value):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #1f2937;
                border-radius: 12px;
                color: white;
            }
        """)

        layout = QVBoxLayout(frame)

        lbl1 = QLabel(title)
        lbl1.setAlignment(Qt.AlignCenter)

        lbl2 = QLabel(value)
        lbl2.setAlignment(Qt.AlignCenter)
        lbl2.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #22c55e;
        """)

        layout.addWidget(lbl1)
        layout.addWidget(lbl2)

        return frame

    def setup_ui(self):
        self.setStyleSheet("""
            background: #111827;
            color: white;
        """)

        layout = QVBoxLayout(self)

        title = QLabel("Dashboard")
        title.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
        """)
        layout.addWidget(title)

        cards = QHBoxLayout()

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("C:\\").percent

        cards.addWidget(self.card("CPU Usage", f"{cpu}%"))
        cards.addWidget(self.card("RAM Usage", f"{ram}%"))
        cards.addWidget(self.card("Disk Usage", f"{disk}%"))
        cards.addWidget(self.card("Security Score", "90"))

        layout.addLayout(cards)

        graph_frame = QFrame()
        graph_frame.setMinimumHeight(400)
        graph_frame.setStyleSheet("""
            QFrame {
                background: #1f2937;
                border-radius: 12px;
            }
        """)

        g_layout = QVBoxLayout(graph_frame)

        txt = QLabel("Live Monitoring Graph (v3.3)")
        txt.setStyleSheet("color: white; font-weight: bold;")
        g_layout.addWidget(txt)

        # Pyqtgraph initialization
        self.graph = pg.PlotWidget()
        self.graph.setBackground("#1f2937")
        self.graph.showGrid(x=True, y=True)
        self.graph_curve = self.graph.plot(pen=pg.mkPen(color="#3b82f6", width=2))

        g_layout.addWidget(self.graph)
        layout.addWidget(graph_frame)