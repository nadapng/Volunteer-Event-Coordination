import json
import os

class SettingsService:

    def __init__(self, config_path="config/app_config.json"):
        self.config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", config_path)
        )

    def get_settings(self):
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading settings: {e}")
            return {}

    def get_database_config(self):
        settings = self.get_settings()
        return settings.get("connection", {})
