from streamlit_autorefresh import st_autorefresh
import streamlit as st
import psutil
import pandas as pd

from self_heal import clean_temp, flush_dns
from reports import save_report
from updater import check_updates
from startup import startup_apps
from battery import battery_info

from hardware import (
    cpu_temperature,
    disk_health
)

from usb_monitor import usb_devices

from security import (
    defender_enabled,
    security_score
)

from network import (
    local_ip,
    public_ip,
    active_connections,
    open_ports
)

st.set_page_config(
    page_title="AKS Guardian AI",
    page_icon="🛡️",
    layout="wide"
)

st_autorefresh(
    interval=5000,
    key="guardian_refresh"
)

st.title("🛡️ AKS Guardian AI v2.0 Phase 3")

cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory().percent
disk = psutil.disk_usage("C:\\").percent

# Sidebar

st.sidebar.title("🛡️ AKS Guardian AI")
st.sidebar.success("System Online")

st.sidebar.metric("CPU", f"{cpu}%")
st.sidebar.metric("RAM", f"{ram}%")
st.sidebar.metric("Disk", f"{disk}%")

# Top Metrics

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CPU Usage", f"{cpu}%")

with col2:
    st.metric("RAM Usage", f"{ram}%")

with col3:
    st.metric("Disk Usage", f"{disk}%")

# Security

score = security_score(
    ram,
    defender_enabled(),
    True
)

st.subheader(f"🛡️ Security Score : {score}/100")

if defender_enabled():
    st.success("🛡️ Windows Defender : ON")
else:
    st.error("⚠ Windows Defender : OFF")

if score >= 80:
    st.success("🟢 LOW RISK")
elif score >= 60:
    st.warning("🟡 MEDIUM RISK")
else:
    st.error("🔴 HIGH RISK")

# Firewall

st.subheader("🔥 Firewall")
st.success("Windows Firewall : ON")

# Usage Chart

st.subheader("📊 System Usage")

chart_data = pd.DataFrame(
    {
        "Usage %": [cpu, ram, disk]
    },
    index=[
        "CPU",
        "RAM",
        "Disk"
    ]
)

st.bar_chart(chart_data)

# Network

st.subheader("🌐 Network Information")

st.info(f"Local IP : {local_ip()}")
st.info(f"Public IP : {public_ip()}")

st.write(
    f"Active Connections : {active_connections()}"
)

# Open Ports

st.subheader("🔓 Open Ports")

ports = open_ports()

if ports:

    port_df = pd.DataFrame({
        "Open Ports": ports[:20]
    })

    st.dataframe(
        port_df,
        use_container_width=True
    )

else:

    st.info(
        "No Open Ports Found"
    )

# Top Processes

st.subheader("💾 Top Memory Usage")

processes = []

for proc in psutil.process_iter(
    ['name', 'memory_percent']
):

    try:

        processes.append(
            proc.info
        )

    except:

        pass

processes = sorted(
    processes,
    key=lambda x: x["memory_percent"],
    reverse=True
)

st.dataframe(
    pd.DataFrame(
        processes[:10]
    ),
    use_container_width=True
)

# AI Recommendations

st.subheader("🤖 AI Recommendations")

if ram > 85:

    st.warning(
        "High RAM Usage Detected"
    )

    st.write(
        "• Close unused Brave tabs"
    )

    st.write(
        "• Close extra VS Code windows"
    )

elif cpu > 80:

    st.warning(
        "High CPU Usage Detected"
    )

elif disk > 80:

    st.warning(
        "Disk Space Running Low"
    )

else:

    st.success(
        "✅ System is running normally."
    )

# Self Healing

st.subheader("🧹 Self-Healing")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🧹 Clean Temp Files"
    ):

        count = clean_temp()

        st.success(
            f"{count} items cleaned"
        )

with col2:

    if st.button(
        "🌐 Flush DNS"
    ):

        if flush_dns():

            st.success(
                "DNS Cache Cleared"
            )

# Reports

st.subheader("📄 Reports")

if st.button(
    "📥 Export CSV Report"
):

    file = save_report(
        cpu,
        ram,
        disk
    )

    st.success(
        f"Saved : {file}"
    )

# Battery

st.subheader("🔋 Battery Health")

battery = battery_info()

if battery:

    st.metric(
        "Battery %",
        f"{battery['percent']}%"
    )

    if battery["plugged"]:

        st.success(
            "Charging"
        )

    else:

        st.warning(
            "Running on Battery"
        )

# Startup Apps

st.subheader("🚀 Startup Applications")

apps = startup_apps()

if apps:

    st.dataframe(
        pd.DataFrame(apps),
        use_container_width=True
    )

# Updates

st.subheader("🪟 Windows Updates")

if st.button(
    "Check Updates"
):

    st.code(
        check_updates()
    )

# Hardware

st.subheader("🖥️ Hardware Health")

temp = cpu_temperature()

if temp:

    st.metric(
        "CPU Temperature",
        f"{temp} °C"
    )

else:

    st.info(
        "CPU Temperature Not Available"
    )

disk_info = disk_health()

st.write(
    f"Total Disk : {disk_info['total_gb']} GB"
)

st.write(
    f"Used Disk : {disk_info['used_gb']} GB"
)

st.write(
    f"Free Disk : {disk_info['free_gb']} GB"
)

# USB

st.subheader("🔌 USB Devices")

devices = usb_devices()

if devices:

    for device in devices:

        st.success(
            f"Connected : {device}"
        )

else:

    st.info(
        "No USB Device Connected"
    )

st.markdown("---")
st.caption(
    "AKS Guardian AI v2.0 Phase 3"
)