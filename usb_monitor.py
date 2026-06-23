import psutil

def usb_devices():

    devices = []

    try:

        for part in psutil.disk_partitions():

            if "removable" in part.opts.lower():
                devices.append(
                    part.device
                )

    except:
        pass

    return devices