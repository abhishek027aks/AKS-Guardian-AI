import psutil

def top_processes():
    apps = []

    for proc in psutil.process_iter(
        ['pid', 'name', 'memory_percent', 'cpu_percent']
    ):
        try:
            apps.append(proc.info)
        except:
            pass

    apps.sort(
        key=lambda x: x['memory_percent'],
        reverse=True
    )

    return apps[:10]