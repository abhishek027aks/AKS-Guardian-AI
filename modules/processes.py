import psutil


def top_processes(limit=10):

    data = []

    for proc in psutil.process_iter(
        ['name', 'cpu_percent', 'memory_percent']
    ):

        try:

            data.append({
                "name": proc.info["name"],
                "cpu": round(proc.info["cpu_percent"], 1),
                "ram": round(proc.info["memory_percent"], 1)
            })

        except:
            pass

    data = sorted(
        data,
        key=lambda x: x["cpu"],
        reverse=True
    )

    return data[:limit]