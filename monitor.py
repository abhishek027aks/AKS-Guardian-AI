import psutil

def system_status():
    """
    Returns current CPU, RAM and Disk usage.
    """

    try:

        cpu = psutil.cpu_percent(
            interval=1
        )

        ram = psutil.virtual_memory().percent

        disk = psutil.disk_usage(
            "C:\\"
        ).percent

        return {
            "cpu": cpu,
            "ram": ram,
            "disk": disk
        }

    except Exception as e:

        return {
            "cpu": 0,
            "ram": 0,
            "disk": 0,
            "error": str(e)
        }


def cpu_usage():
    """
    Returns CPU usage percentage.
    """

    try:
        return psutil.cpu_percent(
            interval=1
        )

    except:
        return 0


def ram_usage():
    """
    Returns RAM usage percentage.
    """

    try:
        return psutil.virtual_memory().percent

    except:
        return 0


def disk_usage():
    """
    Returns Disk usage percentage.
    """

    try:
        return psutil.disk_usage(
            "C:\\"
        ).percent

    except:
        return 0