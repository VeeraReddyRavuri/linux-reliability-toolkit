import yaml
import logging
from toolkit.monitor import check_cpu

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler("logs/toolkit.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

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


if __name__ == "__main__":
    main()