import yaml
import logging

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    print("Configuration loaded:", config)

if __name__ == "__main__":
    main()