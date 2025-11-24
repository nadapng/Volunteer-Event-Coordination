from volunteer_event_coordination.application_base import ApplicationBase
from volunteer_event_coordination.service_layer.app_services import AppServices


class UserInterface(ApplicationBase):

    def __init__(self, config_dict):
        super().__init__("UserInterface", "user_interface")
        self.services = AppServices(config_dict)

    # ===========================
    # MENU
    # ===========================
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

    # ===========================
    # PROCESS USER CHOICE
    # ===========================
    def process_choice(self, choice):

        # ===========================
        # 1) VIEW RECORDS
        # ===========================
        if choice == "1":
            table = input("Enter table name (users / events / registrations): ").strip()
            records = self.services.get_all_records(table)

            if not records:
                print(f"⚠️ No records found in '{table}'.")
                return

            print(f"\n📌 Records in {table}:")
            for row in records:
                print(row)

        # ===========================
        # 2) ADD RECORD
        # ===========================
        elif choice == "2":
            table = input("Enter table name: ").strip()
            columns = self.services.get_columns(table)

            if not columns:
                print("⚠️ Could not retrieve table columns.")
                return

            data_dict = {}

            for col in columns:
                if col.lower() in ("id", "created_at"):
                    continue

                val = input(f"Enter value for '{col}': ")
                data_dict[col] = val

            success = self.services.insert_record(table, data_dict)
            print("✅ Added successfully!" if success else "❌ Failed to add.")

        # ===========================
        # 3) UPDATE RECORD
        # ===========================
        elif choice == "3":
            table = input("Enter table name: ").strip()
            id_column = input("Enter ID column: ").strip()
            record_id = input("Enter record ID to update: ").strip()

            record = self.services.get_record(table, id_column, record_id)
            if not record:
                print("⚠️ Record not found.")
                return

            columns = self.services.get_columns(table)
            data_dict = {}

            print(f"\nCurrent record: {record}")
            print("Enter new values (leave blank to keep current):")

            for i, col in enumerate(columns):
                if col.lower() in ("id", "created_at"):
                    continue

                current = record[i]
                val = input(f"{col} (current: {current}): ")

                if val.strip() != "":
                    data_dict[col] = val

            if not data_dict:
                print("⚠️ No changes made.")
                return

            success = self.services.update_record(table, id_column, record_id, data_dict)
            print("✅ Updated!" if success else "❌ Update failed.")

        # ===========================
        # 4) DELETE RECORD
        # ===========================
        elif choice == "4":
            table = input("Enter table name: ").strip()
            id_column = input("Enter ID column: ").strip()
            record_id = input("Enter record ID to delete: ").strip()

            success = self.services.delete_record(table, id_column, record_id)
            print("🗑️ Deleted!" if success else "❌ Delete failed.")

        else:
            print("⚠️ Invalid choice.")

    # ===========================
    # START LOOP
    # ===========================
    def start(self):
        while True:
            self.menu()
            choice = input("Select an option: ").strip()
            if choice == "5":
                print("👋 Exiting program...")
                break
            self.process_choice(choice)
