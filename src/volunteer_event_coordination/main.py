import json
import os
from volunteer_event_coordination.presentation_layer.user_interface import UserInterface

def load_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "app_config.json")

    if not os.path.exists(config_path):
        print(f"⚠️ Config file not found at: {config_path}")
        return {}

    with open(config_path, "r") as f:
        return json.load(f)

def main():
    print("\n🚀 Starting Volunteer Event Coordination App...\n")

    config_dict = load_config()
    ui = UserInterface(config_dict)
    ui.start()

if __name__ == "__main__":
    main()
