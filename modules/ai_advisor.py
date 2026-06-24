def analyze(data):
    advice = []

    if data["cpu"] > 80:
        advice.append("⚠ High CPU Usage detected.")
    elif data["cpu"] > 50:
        advice.append("ℹ CPU usage is moderate.")

    if data["ram"] > 85:
        advice.append("⚠ RAM usage critically high.")
    elif data["ram"] > 70:
        advice.append("ℹ RAM usage is high. Close unnecessary apps.")

    if data["disk"] > 90:
        advice.append("⚠ Disk space critically low.")
    elif data["disk"] > 80:
        advice.append("ℹ Disk space running low.")

    if not advice:
        advice.append("✅ System looks healthy.")

    return advice