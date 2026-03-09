import subprocess

def is_service_active(service_name):
    result = subprocess.run(
        ["systemctl", "is-active", service_name],
        capture_output = True,
        text = True,
    )

    status = result.stdout.strip()

    if status != "active":
        return{
            "status": "Failed",
            "service": service_name
        }
    return{
            "status": "OK  ",
            "service": service_name
        }

def restart_service(service_name):
    result = subprocess.run(
        ["systemctl", "is-active", service_name],
        capture_output = True,
        text = True,
    )

    if resutl.returncode == 0:
        return {
            "status": "RESTARTED",
            "service": service_name
        }  
    return {
        "status": "FAILED",
        "service": service_name,
        "error": result.stderr.strip()
    }