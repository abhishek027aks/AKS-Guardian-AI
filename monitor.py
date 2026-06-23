import psutil

def system_status():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('C:\\').percent

    return {
        "cpu": cpu,
        "ram": ram,
        "disk": disk
    }