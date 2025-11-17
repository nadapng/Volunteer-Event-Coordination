from volunteer_event_coordination.application_base import ApplicationBase
from volunteer_event_coordination.service_layer.app_services import AppServices

class UserInterface(ApplicationBase):

    def __init__(self, config_dict):
        super().__init__("UserInterface", "user_interface")
        self.services = AppServices(config_dict)

    def menu(self):
        print("\n==============================")
        print(" Volunteer Event Coordination")
        print("==============================")
        print("1. View all records")
        print("2. Add a new record")
        print("3. Update a record")
        print("4. Delete a record")
        print("5. Exit")
        print("==============================")

    def process_choice(self, choice):
        # ==========================
        # 1) VIEW RECORDS
        # ==========================
        if choice == "1":
            table = input("Enter table name: ").strip()
            records = self.services.get_all_records(table)

            if not records:
                print(f"⚠️ No records found in '{table}' table.")
                return

            for row in records:
                print(row)

        # ==========================
        # 2) ADD NEW RECORD
        # ==========================
        elif choice == "2":
            table = input("Enter table name: ").strip()

            columns = self.services.get_columns(table)
            if not columns:
                print("⚠️ Could not retrieve columns.")
                return

            data_dict = {}

            for col in columns:
                if col.lower() in ("id", "created_at"):
                    continue

                value = input(f"Enter value for '{col}': ")
                data_dict[col] = value

            success = self.services.insert_record(table, data_dict)

            if success:
                print("✅ Record added successfully!")
            else:
                print("❌ Failed to add record.")

        else:
            print("⚠️ Invalid option.")

    def start(self):
        while True:
            self.menu()
            choice = input("Select an option: ").strip()
            if choice == "5":
                break
            self.process_choice(choice)
