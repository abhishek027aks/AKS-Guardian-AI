import psutil


def top_processes():

    processes = []

    for proc in psutil.process_iter(
        ['pid', 'name', 'cpu_percent', 'memory_percent']
    ):
        try:
            processes.append(
                proc.info
            )
        except:
            pass

    return sorted(
        processes,
        key=lambda x: x['memory_percent'],
        reverse=True
    )