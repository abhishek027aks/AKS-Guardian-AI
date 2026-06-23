from streamlit_autorefresh import st_autorefresh
import streamlit as st
import psutil
import pandas as pd

from self_heal import *
from reports import *

from updater import *
from startup import *
from battery import *

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

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="AKS Guardian AI",
    page_icon="🛡️",
    layout="wide"
)

# =========================
# Auto Refresh
# =========================
st_autorefresh(
    interval=5000,
    key="guardian_refresh"
)

# =========================
# Title
# =========================
st.title("🛡️ AKS Guardian AI v2.0")

# =========================
# System Stats
# =========================
cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory().percent
disk = psutil.disk_usage("C:\\").percent

# =========================
# Sidebar
# =========================
st.sidebar.title("🛡️ AKS Guardian AI")
st.sidebar.success("System Online")

st.sidebar.write(f"CPU : {cpu}%")
st.sidebar.write(f"RAM : {ram}%")
st.sidebar.write(f"Disk : {disk}%")

# =========================
# Metrics
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CPU Usage", f"{cpu}%")

with col2:
    st.metric("RAM Usage", f"{ram}%")

with col3:
    st.metric("Disk Usage", f"{disk}%")

# =========================
# Security Score
# =========================
score = security_score(ram)

st.subheader(f"🛡️ Security Score : {score}/100")

if defender_enabled():
    st.success("🛡️ Windows Defender : ON")
else:
    st.error("⚠️ Windows Defender : OFF")

if score >= 80:
    st.success("🟢 LOW RISK")
elif score >= 60:
    st.warning("🟡 MEDIUM RISK")
else:
    st.error("🔴 HIGH RISK")

# =========================
# Firewall
# =========================
st.subheader("🔥 Firewall")
st.success("Windows Firewall : ON")

# =========================
# System Usage Chart
# =========================
st.subheader("📊 System Usage")

chart_data = pd.DataFrame(
    {
        "Usage %": [cpu, ram, disk]
    },
    index=["CPU", "RAM", "Disk"]
)

st.bar_chart(chart_data)

# =========================
# Network Information
# =========================
st.subheader("🌐 Network Information")

st.info(f"Local IP : {local_ip()}")
st.info(f"Public IP : {public_ip()}")

st.write(
    f"Active Connections : {active_connections()}"
)

# =========================
# Open Ports
# =========================
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
    st.info("No Open Ports Found")

# =========================
# Top Memory Usage
# =========================
st.subheader("💾 Top Memory Usage")

processes = []

for proc in psutil.process_iter(
    ['name', 'memory_percent']
):
    try:
        processes.append(proc.info)
    except:
        pass

processes = sorted(
    processes,
    key=lambda x: x['memory_percent'],
    reverse=True
)

top_processes = pd.DataFrame(
    processes[:10]
)

st.dataframe(
    top_processes,
    use_container_width=True
)

# =========================
# AI Recommendations
# =========================
st.subheader("🤖 AI Recommendations")

if ram > 85:
    st.warning("⚠ High RAM Usage Detected")
    st.write("• Close unused Brave tabs")
    st.write("• Close extra VS Code windows")

if disk > 80:
    st.warning("⚠ Disk space is running low")
    st.write("• Clean unnecessary files")

if cpu > 80:
    st.warning("⚠ High CPU Usage Detected")
    st.write("• Check high CPU consuming processes")

if ram <= 85 and disk <= 80 and cpu <= 80:
    st.success("✅ System is running normally.")

# =========================
# Self Healing
# =========================
st.subheader("🧹 Self-Healing")

col1, col2 = st.columns(2)

with col1:

    if st.button("🧹 Clean Temp Files"):

        count = clean_temp()

        st.success(
            f"{count} temp items cleaned."
        )

with col2:

    if st.button("🌐 Flush DNS"):

        if flush_dns():
            st.success(
                "DNS Cache Cleared"
            )

# =========================
# Reports
# =========================
st.subheader("📄 Reports")

if st.button("📥 Export CSV Report"):

    file = save_report(
        cpu,
        ram,
        disk
    )

    st.success(
        f"Saved: {file}"
    )

# =========================
# Battery Health
# =========================
st.subheader("🔋 Battery Health")

battery = battery_info()

if battery:

    st.metric(
        "Battery %",
        f"{battery['percent']}%"
    )

    if battery["plugged"]:
        st.success("Charging")
    else:
        st.warning("Running on Battery")

else:
    st.info("Battery not detected")

# =========================
# Startup Applications
# =========================
st.subheader("🚀 Startup Applications")

apps = startup_apps()

if apps:

    startup_df = pd.DataFrame(apps)

    st.dataframe(
        startup_df,
        use_container_width=True
    )

else:
    st.info("No startup apps found")

# =========================
# Windows Updates
# =========================
st.subheader("🪟 Windows Updates")

if st.button("Check Updates"):

    updates = check_updates()

    st.code(updates)

# =========================
# Footer
# =========================
st.markdown("---")
st.caption("AKS Guardian AI v2.0 Phase 2")