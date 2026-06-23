import subprocess

def firewall_status():

    try:

        result = subprocess.check_output(
            "netsh advfirewall show allprofiles",
            shell=True,
            text=True
        )

        return result

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


def security_score(
    ram_usage,
    defender=True,
    firewall=True
):

    score = 100

    if ram_usage > 90:
        score -= 20

    elif ram_usage > 80:
        score -= 10

    if not defender:
        score -= 30

    if not firewall:
        score -= 20

    return max(score, 0)