import yaml
import logging
from toolkit.monitor import check_cpu, check_memory, check_disk
from toolkit.service_manager import is_service_active, restart_service

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler("logs/toolkit.log")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    logger = setup_logger()
    config = load_config()

    logger.info("Configuration loaded successfully")

    cpu_result = check_cpu(config["cpu_threshold"])

    logger.info(f"CPU usage: {cpu_result["cpu_usage"]}%")

    if cpu_result["status"] == "Alert":
        logger.warning("CPU usage exceeded threshold")

    memory_result = check_memory(config["memory_threshold"])

    logger.info(f"Memory usage: {memory_result["memory_usage"]}%")

    if memory_result["stauts"] == "Alert":
        logger.warning("Memory usage exceeding threshold")

    disk_result = check_disk(config["disk_threshold"])

    logger.info(f"Disk usage: {disk_result["disk_usage"]}")

    if disk_result["stauts"] == "Alert":
        logger.warning("Disk usage exceeding threshold")
    
    services = config.get("services_to_monitor", [])

    for service in services:
        result = is_service_active(service)

        if result["status"] == "FAILED":
            logger.warning(f"Service {service} is not active. Attempting restart..")

            restart_result = restart_service(service)

            if restart_result["status"] == "RESTARTED":
                logger.info(f"Service {service} restarted succesfully")
            else:
                logger.error(f"Failed to restart service {service}: {restart_result["error"]}")
        else:
            logger.info(f"Service {service} is running")

if __name__ == "__main__":
    main()