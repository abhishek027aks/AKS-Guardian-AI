import winreg

def startup_apps():

    apps = []

    try:

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run"
        )

        count = winreg.QueryInfoKey(key)[1]

        for i in range(count):

            name, value, _ = winreg.EnumValue(
                key,
                i
            )

            apps.append({
                "name": name,
                "path": value
            })

    except:
        pass

    return apps