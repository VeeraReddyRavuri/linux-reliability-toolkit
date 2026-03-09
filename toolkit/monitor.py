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
    
def check_memory(threshold):
    memory = psutil.virtual_memory()
    memory_usage =  memory.percent

    if memory_usage > threshold:
        return {
            "stauts": "Alert",
            "memory_usage": memory_usage
        }
    return {
            "stauts": "OK",
            "memory_usage": memory_usage
    }