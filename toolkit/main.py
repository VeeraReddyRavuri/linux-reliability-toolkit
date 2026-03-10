"""
Main orchestration module for the Linux Reliability Toolkit.

Responsibilities:
- Load configuration from YAML
- Initialize structured logging
- Execute system health checks (CPU, memory, disk)
- Detect failed systemd services and attempt restart
- Scan system logs for errors
- Send webhook alerts when issues are detected
"""

import yaml
import logging

# Monitoring utilities for system resources
from toolkit.monitor import check_cpu, check_memory, check_disk

# Service management utilities for systemd services
from toolkit.service_manager import is_service_active, restart_service

# Log scanning utility
from toolkit.log_parser import scan_logs

# Notification utility for external alerts
from toolkit.notifier import send_webhook_alert


def setup_logger():
    """
    Configure application logging.

    Logs are written to:
    - logs/toolkit.log (file logging)
    - console output (for interactive runs)
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Define common log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # File handler for persistent logs
    file_handler = logging.FileHandler("logs/toolkit.log")
    file_handler.setFormatter(formatter)

    # Console handler for terminal output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Attach handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def load_config():
    """
    Load configuration values from config.yaml.
    """
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def main():
    """
    Main execution flow for the reliability toolkit.
    """

    logger = setup_logger()
    config = load_config()

    logger.info("Configuration loaded successfully")

    # ---------------------------
    # CPU Monitoring
    # ---------------------------
    cpu_result = check_cpu(config["cpu_threshold"])

    logger.info(f"CPU usage: {cpu_result['cpu_usage']}%")

    if cpu_result["status"] == "ALERT":
        logger.warning("CPU usage exceeded threshold")

    # ---------------------------
    # Memory Monitoring
    # ---------------------------
    memory_result = check_memory(config["memory_threshold"])

    logger.info(f"Memory usage: {memory_result['memory_usage']}%")

    if memory_result["status"] == "ALERT":
        logger.warning("Memory usage exceeding threshold")

    # ---------------------------
    # Disk Monitoring
    # ---------------------------
    disk_result = check_disk(config["disk_threshold"])

    logger.info(f"Disk usage: {disk_result['disk_usage']}")

    if disk_result["status"] == "ALERT":
        logger.warning("Disk usage exceeding threshold")

    # ---------------------------
    # Service Health Checks
    # ---------------------------
    services = config.get("services_to_monitor", [])

    for service in services:
        result = is_service_active(service)

        if result["status"] == "FAILED":
            logger.warning(f"Service {service} is not active. Attempting restart..")

            restart_result = restart_service(service)

            if restart_result["status"] == "RESTARTED":
                logger.info(f"Service {service} restarted successfully")
            else:
                logger.error(
                    f"Failed to restart service {service}: {restart_result['error']}"
                )
        else:
            logger.info(f"Service {service} is running")

    # ---------------------------
    # System Log Inspection
    # ---------------------------
    log_result = scan_logs()

    if log_result["status"] == "ERROR_FOUND":
        logger.warning("Recent error logs detected")
        logger.warning(log_result["logs"])
    else:
        logger.info("No recent critical logs found")

    # ---------------------------
    # Webhook Alerting
    # ---------------------------
    webhook_config = config.get("webhook", {})

    if webhook_config.get("enabled"):
        alert_message = "Linux Reliability Toolkit detected an issue"

        alert_result = send_webhook_alert(
            webhook_config["url"],
            alert_message
        )

        if alert_result["status"] == "SENT":
            logger.info("Webhook alert sent successfully")
        else:
            logger.error(f"Webhook alert failed: {alert_result['error']}")


if __name__ == "__main__":
    main()