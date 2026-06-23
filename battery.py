import psutil

def battery_info():

    battery = psutil.sensors_battery()

    if battery:

        return {
            "percent": battery.percent,
            "plugged": battery.power_plugged
        }

    return None