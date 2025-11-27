from volunteer_event_coordination.presentation_layer.user_interface import UserInterface
from volunteer_event_coordination.settings import SettingsService


def main():
    print("\n🚀 Starting Volunteer Event Coordination App...\n")

    # Load config (even if UI does not use it now)
    settings = SettingsService()
    config_dict = settings.get_settings()

    # Create UI (no args)
    ui = UserInterface()

    # Run the UI loop
    ui.run()


if __name__ == "__main__":
    main()
