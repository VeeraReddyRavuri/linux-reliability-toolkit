import psutil

def check_cpu(threshold):
    cpu_usage = psutil.cpu_percent(interval=1)

    if cpu_usage > threshold:
        return {
            "status": "Alert",
            "cpu_usage": cpu_usage
        }
    return {
        "status": "OK",
        "cpu_usage": cpu_usage
    }
    