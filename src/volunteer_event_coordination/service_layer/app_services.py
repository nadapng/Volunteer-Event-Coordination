from volunteer_event_coordination.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
from volunteer_event_coordination.utils.logger_util import Logger
from volunteer_event_coordination.settings import SettingsService


class AppServices:

    def __init__(self):
        self.logger = Logger("AppServices", "app_services")

        self.settings = SettingsService()

        config_dict = self.settings.get_database_config()
        self.db = MySQLPersistenceWrapper(config_dict)

    # =======================
    # Example methods
    # =======================

    def get_all_users(self):
        return self.db.fetch_all("users")

    def create_user(self, user_data):
        return self.db.create_user(user_data)

    def get_user_by_id(self, user_id):
        return self.db.get_by_id("users", "id", user_id)

    def update_user(self, user_id, user_data):
        return self.db.update_record("users", "id", user_id, user_data)

    def delete_user(self, user_id):
        return self.db.delete_record("users", "id", user_id)
