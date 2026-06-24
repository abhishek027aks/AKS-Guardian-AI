import os
import csv
import json
from datetime import datetime

def save_report(cpu_val, ram_val, disk_val, network_status="Secure"):
    """
    Generates a system metric diagnostic capture log across different formats.
    Saves inside the dedicated root './reports/' directory.
    """
    # Create target directory path dynamically if missing
    target_dir = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"Guardian_Audit_{timestamp}"
    
    report_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "platform": "Windows OS Engine",
        "metrics": {
            "cpu_utilization_percent": cpu_val,
            "ram_utilization_percent": ram_val,
            "disk_utilization_percent": disk_val
        },
        "network_security_audit": network_status
    }

    try:
        # Format 1: JSON Engine Export Mapping
        json_path = os.path.join(target_dir, f"{base_filename}.json")
        with open(json_path, 'w') as j_file:
            json.dump(report_data, j_file, indent=4)

        # Format 2: Tabular CSV Serialization
        csv_path = os.path.join(target_dir, f"{base_filename}.csv")
        with open(csv_path, 'w', newline='') as c_file:
            writer = csv.writer(c_file)
            writer.writerow(["Parameter", "Value"])
            writer.writerow(["Timestamp", report_data["timestamp"]])
            writer.writerow(["CPU Usage %", cpu_val])
            writer.writerow(["RAM Usage %", ram_val])
            writer.writerow(["Disk Usage %", disk_val])
            writer.writerow(["Security State", network_status])

        # Format 3: Raw Clean Text Layout Manifest
        txt_path = os.path.join(target_dir, f"{base_filename}.txt")
        with open(txt_path, 'w') as t_file:
            t_file.write("==================================================\n")
            t_file.write("           AKS GUARDIAN AI SYSTEM REPORT          \n")
            t_file.write("==================================================\n")
            t_file.write(f"Generated at : {report_data['timestamp']}\n\n")
            t_file.write(f"● CPU Core Usage   : {cpu_val}%\n")
            t_file.write(f"● RAM Allocation   : {ram_val}%\n")
            t_file.write(f"● Hard Disk State  : {disk_val}%\n")
            t_file.write(f"● Network Perimeter: {network_status}\n")
            t_file.write("==================================================\n")

        return f"Success: Logs written to '{target_dir}' directory."
    except Exception as e:
        return f"Generation Failed: Internal storage error: {e}"