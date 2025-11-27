
from volunteer_event_coordination.application_base import ApplicationBase
from volunteer_event_coordination.service_layer.app_services import AppServices
from volunteer_event_coordination.utils.logger_util import Logger


class UserInterface(ApplicationBase):

    def __init__(self):
        super().__init__("UserInterface", "ui_log")
        self.logger = Logger("UserInterface", "ui_log")

        self.services = AppServices()

    def display_menu(self):
        print("==============================")
        print(" Volunteer Event Coordination ")
        print("==============================")
        print("1. View all records")
        print("2. Add a new record")
        print("3. Update a record")
        print("4. Delete a record")
        print("5. Exit")
        print("==============================")
        choice = input("Select an option: ")
        return choice

    def run(self):
        while True:
            choice = self.display_menu()

            if choice == "1":
                users = self.services.get_all_users()
                print(users)

            elif choice == "2":
                first = input("Enter first name: ")
                last = input("Enter last name: ")
                email = input("Enter email: ")

                self.services.create_user({
                    "first_name": first,
                    "last_name": last,
                    "email": email
                })

            elif choice == "3":
                user_id = input("Enter user ID: ")
                new_last = input("Enter new last name: ")
                self.services.update_user(user_id, {"last_name": new_last})

            elif choice == "4":
                user_id = input("Enter user ID: ")
                self.services.delete_user(user_id)

            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid option.")
