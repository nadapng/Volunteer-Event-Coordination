class UserInterface:
    def __init__(self):
        from volunteer_event_coordination.service_layer.app_services import AppServices
        self.services = AppServices()

    def display_menu(self):
        print("\n" + "=" * 30)
        print(" Volunteer Event Coordination")
        print("=" * 30)
        print("1. View all records")
        print("2. Add a new record")
        print("3. Update a record")
        print("4. Delete a record")
        print("5. Exit")
        print("=" * 30)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Select an option: ")

            # ============================
            # VIEW ALL RECORDS
            # ============================
            if choice == "1":
                users = self.services.get_all_users()

                if not users:
                    print("\nNo users found.\n")
                else:
                    print("\n====== Users List ======\n")
                    for u in users:
                        print(f"ID: {u['user_id']}")
                        print(f"First Name: {u['first_name']}")
                        print(f"Last Name: {u['last_name']}")
                        print(f"Email: {u['email']}")
                        print(f"Created At: {u['created_at']}")
                        print("-----------------------------")

            # ============================
            # ADD NEW USER
            # ============================
            elif choice == "2":
                first = input("Enter first name: ")
                last = input("Enter last name: ")
                email = input("Enter email: ")

                self.services.create_user({
                    "first_name": first,
                    "last_name": last,
                    "email": email
                })

                print("\nUser added successfully!\n")

            # ============================
            # UPDATE USER
            # ============================
            elif choice == "3":
                user_id = input("Enter user ID to update: ")

                first = input("Enter new first name: ")
                last = input("Enter new last name: ")
                email = input("Enter new email: ")

                updated = self.services.update_user(user_id, {
                    "first_name": first,
                    "last_name": last,
                    "email": email
                })

                if updated:
                    print("\nUser updated successfully!\n")
                else:
                    print("\nUser not found.\n")

            # ============================
            # DELETE USER
            # ============================
            elif choice == "4":
                user_id = input("Enter user ID to delete: ")

                deleted = self.services.delete_user(user_id)

                if deleted:
                    print("\nUser deleted successfully!\n")
                else:
                    print("\nUser not found.\n")

            # ============================
            # EXIT
            # ============================
            elif choice == "5":
                print("Exiting program... Goodbye!")
                break

            else:
                print("Invalid option. Please try again.\n")
