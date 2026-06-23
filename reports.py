import pandas as pd

def save_report(cpu, ram, disk):

    report = pd.DataFrame({
        "CPU": [cpu],
        "RAM": [ram],
        "Disk": [disk]
    })

    report.to_csv(
        "guardian_report.csv",
        index=False
    )

    return "guardian_report.csv"