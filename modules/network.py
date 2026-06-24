import socket
import psutil


def get_local_ip():

    try:
        return socket.gethostbyname(
            socket.gethostname()
        )

    except:
        return "Unknown"


def active_connections():

    try:
        return len(
            psutil.net_connections()
        )

    except:
        return 0


def network_stats():

    try:

        net = psutil.net_io_counters()

        return {
            "sent": round(
                net.bytes_sent / (1024 * 1024),
                2
            ),
            "recv": round(
                net.bytes_recv / (1024 * 1024),
                2
            )
        }

    except:

        return {
            "sent": 0,
            "recv": 0
        }