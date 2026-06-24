import socket
import psutil
import requests

def local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "Unavailable"

def public_ip():
    try:
        # 5-second timeout ensures UI doesn't hang if internet is offline
        return requests.get("https://api.ipify.org", timeout=5).text
    except Exception:
        return "Offline/Unavailable"

def active_connections():
    try:
        return len(psutil.net_connections())
    except Exception:
        return 0

def open_ports():
    ports = []
    try:
        for conn in psutil.net_connections():
            if conn.status == "LISTEN":
                ports.append(conn.laddr.port)
        return sorted(set(ports))
    except Exception:
        return []