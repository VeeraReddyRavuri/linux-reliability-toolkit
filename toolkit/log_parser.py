import subprocess

def scan_logs():
    result = subprocess.run(
        ["journalctl", "-p", "3", "-n", "20"],
        capture_output = True,
        text = True
    )

    logs = result.stdout.strip()

    if logs:
        return {
            "status": "ERROR_FOUND",
            "logs": logs
        }
    return {
        "status": "OK",
        "logs": None
    }