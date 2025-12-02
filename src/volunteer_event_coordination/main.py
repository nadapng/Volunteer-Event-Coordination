import json
import os

from volunteer_event_coordination.presentation_layer.user_interface import UserInterface
from volunteer_event_coordination.service_layer.app_services import AppServices
from volunteer_event_coordination.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper

def main():
    print("\n🚀 Starting Volunteer Event Coordination App...\n")

    # Absolute path to src
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Path to app_settings.json
    config_path = os.path.join(base_path, "app_settings.json")

    # Load config
    with open(config_path, "r") as f:
        config = json.load(f)

    # Create DB wrapper with config
    db = MySQLPersistenceWrapper(config)

    # Create service layer
    service = AppServices(db)

    # Create UI
    ui = UserInterface(service)

    # Run program
    ui.run()


if __name__ == "__main__":
    main()
