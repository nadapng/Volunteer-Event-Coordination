import os
import json

class SettingsService:

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "config", "app_config.json")

        if not os.path.exists(config_path):
            print(f"⚠️ Settings file not found: {config_path}")
            self.config = {}
        else:
            with open(config_path, "r") as f:
                self.config = json.load(f)

    @property
    def log_directory(self):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")

    @property
    def log_prefix(self):
        return self.config.get("meta", {}).get("log_prefix", "app")
