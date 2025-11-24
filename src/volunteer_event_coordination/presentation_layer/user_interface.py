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
                # نتجنب الأعمدة التلقائية
                if col.lower() in ("id", "created_at") or col.endswith("_id") and col == columns[0]:
                    # أول عمود غالبًا هو الـ PK (user_id / event_id / reg_id)
                    continue

                value = input(f"Enter value for '{col}': ")
                data_dict[col] = value

            success = self.services.insert_record(table, data_dict)

            if success:
                print("✅ Record added successfully!")
            else:
                print("❌ Failed to add record.")

        # ==========================
        # 3) UPDATE RECORD
        # ==========================
        elif choice == "3":
            table = input("Enter table name: ").strip()
            columns = self.services.get_columns(table)

            if not columns:
                print("⚠️ Could not retrieve columns.")
                return

            pk_column = columns[0]  # نفترض أول عمود هو الـ PK مثل user_id / event_id / reg_id
            pk_value = input(f"Enter {pk_column} of the record to update: ").strip()

            data_dict = {}
            for col in columns:
                if col == pk_column or col.lower() == "created_at":
                    continue

                new_val = input(f"New value for '{col}' (leave blank to keep current): ").strip()
                if new_val != "":
                    data_dict[col] = new_val

            if not data_dict:
                print("⚠️ No changes provided. Nothing to update.")
                return

            success = self.services.update_record(table, pk_column, pk_value, data_dict)

            if success:
                print("✅ Record updated successfully!")
            else:
                print("❌ Failed to update record.")

        # ==========================
        # 4) DELETE RECORD
        # ==========================
        elif choice == "4":
            table = input("Enter table name: ").strip()
            columns = self.services.get_columns(table)

            if not columns:
                print("⚠️ Could not retrieve columns.")
                return

            pk_column = columns[0]
            pk_value = input(f"Enter {pk_column} of the record to delete: ").strip()

            confirm = input("Are you sure you want to delete this record? (y/n): ").strip().lower()
            if confirm != "y":
                print("❎ Delete cancelled.")
                return

            success = self.services.delete_record(table, pk_column, pk_value)

            if success:
                print("✅ Record deleted successfully!")
            else:
                print("❌ Failed to delete record.")

        else:
            print("⚠️ Invalid option.")

    def start(self):
        while True:
            self.menu()
            choice = input("Select an option: ").strip()
            if choice == "5":
                print("Goodbye 👋")
                break
            self.process_choice(choice)
