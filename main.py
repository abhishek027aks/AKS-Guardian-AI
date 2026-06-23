from monitor import system_status
from ai_advisor import analyze
from processes import top_processes

from security import (
    firewall_status,
    defender_status
)

from network import (
    local_ip,
    public_ip,
    active_connections,
    open_ports
)

# =========================
# Firewall
# =========================
print("\n===== FIREWALL =====")
print(firewall_status())

# =========================
# System Status
# =========================
status = system_status()

print("\n===== AKS Guardian AI =====")

print(f"CPU  : {status['cpu']}%")
print(f"RAM  : {status['ram']}%")
print(f"Disk : {status['disk']}%")

# =========================
# Security
# =========================
print("\n===== SECURITY =====")

print(defender_status())

# =========================
# Network
# =========================
print("\n===== NETWORK =====")

print("Local IP      :", local_ip())
print("Public IP     :", public_ip())
print("Connections   :", active_connections())

print("\nOpen Ports:")
print(open_ports())

# =========================
# AI Analysis
# =========================
print("\n===== AI ANALYSIS =====")

for item in analyze(status):
    print("AI:", item)

# =========================
# Top Processes
# =========================
print("\n===== TOP MEMORY USERS =====")

for app in top_processes():
    print(
        f"{app['name']} | "
        f"RAM: {app['memory_percent']:.2f}%"
    )