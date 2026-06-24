import psutil
import time


def get_cpu():
    return round(psutil.cpu_percent(), 1)


def get_ram():
    return round(
        psutil.virtual_memory().percent,
        1
    )


def get_disk():
    return round(
        psutil.disk_usage("C:\\").percent,
        1
    )


def get_uptime():

    boot = psutil.boot_time()

    uptime = int(
        time.time() - boot
    )

    hours = uptime // 3600

    minutes = (
        uptime % 3600
    ) // 60

    return f"{hours}h {minutes}m"


def system_status():

    return {
        "cpu": get_cpu(),
        "ram": get_ram(),
        "disk": get_disk()
    }


def cpu_usage():
    return get_cpu()


def ram_usage():
    return get_ram()


def disk_usage():
    return get_disk()