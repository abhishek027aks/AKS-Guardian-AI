import psutil

def top_processes():
    """
    Scans active operating system processes, filtering out restricted internal nodes
    and returns top 10 memory-consuming threads.
    """
    apps = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            # Fallback handling for background processes running under SYSTEM authority
            p_info = proc.info
            if p_info['memory_percent'] is None:
                p_info['memory_percent'] = 0.0
            if p_info['cpu_percent'] is None:
                p_info['cpu_percent'] = 0.0
                
            apps.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except Exception:
            pass

    # Sort structures via lambda sorting mapping
    apps.sort(key=lambda x: x['memory_percent'], reverse=True)
    return apps[:10]