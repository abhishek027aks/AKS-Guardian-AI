import subprocess

def firewall_status():
    try:
        return subprocess.check_output(
            "netsh advfirewall show allprofiles",
            shell=True,
            text=True
        )
    except Exception as e:
        return str(e)

def defender_enabled():
    try:
        cmd = r'powershell "(Get-MpComputerStatus).RealTimeProtectionEnabled"'

        result = subprocess.check_output(
            cmd,
            shell=True,
            text=True
        ).strip()

        return "True" in result

    except:
        return False

def defender_status():
    try:
        cmd = r'powershell "Get-MpComputerStatus | Select AntivirusEnabled,RealTimeProtectionEnabled"'

        return subprocess.check_output(
            cmd,
            shell=True,
            text=True
        )

    except Exception as e:
        return str(e)

def security_score(ram_usage):
    score = 100

    if not defender_enabled():
        score -= 30

    if ram_usage > 90:
        score -= 15
    elif ram_usage > 80:
        score -= 5

    return max(score, 0)