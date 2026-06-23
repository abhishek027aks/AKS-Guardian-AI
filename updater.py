import subprocess

def check_updates():

    try:
        result = subprocess.check_output(
            'powershell "Get-HotFix | Select-Object -First 5"',
            shell=True,
            text=True
        )

        return result

    except Exception as e:
        return str(e)