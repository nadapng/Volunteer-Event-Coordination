class UserInterface:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        while True:
            print("\n====== Main Menu ======")
            print("1) View Users")
            print("2) Add User")
            print("3) Update User")
            print("4) Delete User")
            print("5) Exit")

            choice = input("\nSelect an option: ")

            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.add_user()
            elif choice == "3":
                self.update_user()
            elif choice == "4":
                self.delete_user()
            elif choice == "5":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    # -------------------------
    # VIEW USERS
    # -------------------------
    def view_users(self):
        print("\n====== Users List ======")
        users = self.controller.get_all_users()

        for u in users:
            user_dict = {
                "user_id": u[0],
                "first_name": u[1],
                "last_name": u[2],
                "email": u[3],
            }

            print(
                f"ID: {user_dict['user_id']}, "
                f"First Name: {user_dict['first_name']}, "
                f"Last Name: {user_dict['last_name']}, "
                f"Email: {user_dict['email']}"
            )

    # -------------------------
    # ADD USER
    # -------------------------
    def add_user(self):
        print("\n====== Add User ======")
        first = input("First name: ")
        last = input("Last name: ")
        email = input("Email: ")

        data = {"first_name": first, "last_name": last, "email": email}
        self.controller.create_user(data)
        print("User added successfully.")

    # -------------------------
    # UPDATE USER (UPDATE ALL FIELDS)
    # -------------------------
    def update_user(self):
        print("\n====== Update User ======")
        user_id = input("Enter user ID to update: ")

        print("Enter NEW values (leave blank to keep current):")
        new_first = input("New first name: ")
        new_last = input("New last name: ")
        new_email = input("New email: ")

        # Build data dict dynamically
        data = {}

        if new_first.strip():
            data["first_name"] = new_first
        if new_last.strip():
            data["last_name"] = new_last
        if new_email.strip():
            data["email"] = new_email

        if not data:
            print("No changes provided. Update canceled.")
            return

        self.controller.update_user("users", "user_id", user_id, data)
        print("User updated successfully.")

    # -------------------------
    # DELETE USER
    # -------------------------
    def delete_user(self):
        print("\n====== Delete User ======")
        user_id = input("Enter user ID to delete: ")

        self.controller.delete_user("users", "user_id", user_id)
        print("User deleted successfully.")
