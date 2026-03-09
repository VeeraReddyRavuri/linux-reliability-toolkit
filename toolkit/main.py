import yaml
import logging

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

if __name__ == "__main__":
    main()