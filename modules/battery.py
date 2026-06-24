import psutil

def battery_info():
    """
    Fetches real-time battery status, percentage, and power supply information.
    """
    try:
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "plugged": battery.power_plugged,
                "secsleft": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited/Full",
                "status_text": "⚡ Charging" if battery.power_plugged else "🔋 Running on Battery"
            }
        return None
    except Exception as e:
        print(f"Error in battery module: {e}")
        return None