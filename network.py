import socket
import psutil
import requests

def local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Unavailable"

def public_ip():
    try:
        return requests.get(
            "https://api.ipify.org",
            timeout=5
        ).text
    except:
        return "Unavailable"

def active_connections():
    try:
        return len(psutil.net_connections())
    except:
        return 0

def open_ports():
    ports = []

    try:
        for conn in psutil.net_connections():
            if conn.status == "LISTEN":
                ports.append(conn.laddr.port)

        return sorted(set(ports))

    except:
        return []