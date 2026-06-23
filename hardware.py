import psutil

def cpu_temperature():
    """
    Returns CPU temperature if available.
    Returns None if temperature sensors are not supported.
    """

    try:
        temps = psutil.sensors_temperatures()

        if not temps:
            return None

        for name, entries in temps.items():

            if entries:
                return entries[0].current

        return None

    except Exception:
        return None


def disk_health():
    """
    Returns disk information for C: drive.
    """

    try:

        usage = psutil.disk_usage("C:\\")

        return {
            "total_gb": round(
                usage.total / (1024 ** 3),
                2
            ),
            "used_gb": round(
                usage.used / (1024 ** 3),
                2
            ),
            "free_gb": round(
                usage.free / (1024 ** 3),
                2
            ),
            "percent": usage.percent
        }

    except Exception:

        return {
            "total_gb": 0,
            "used_gb": 0,
            "free_gb": 0,
            "percent": 0
        }


def ram_info():
    """
    Returns RAM information.
    """

    try:

        memory = psutil.virtual_memory()

        return {
            "total_gb": round(
                memory.total / (1024 ** 3),
                2
            ),
            "used_gb": round(
                memory.used / (1024 ** 3),
                2
            ),
            "available_gb": round(
                memory.available / (1024 ** 3),
                2
            ),
            "percent": memory.percent
        }

    except Exception:

        return {
            "total_gb": 0,
            "used_gb": 0,
            "available_gb": 0,
            "percent": 0
        }


def cpu_info():
    """
    Returns CPU information.
    """

    try:

        return {
            "physical_cores": psutil.cpu_count(
                logical=False
            ),
            "total_cores": psutil.cpu_count(),
            "cpu_usage": psutil.cpu_percent(
                interval=1
            )
        }

    except Exception:

        return {
            "physical_cores": 0,
            "total_cores": 0,
            "cpu_usage": 0
        }