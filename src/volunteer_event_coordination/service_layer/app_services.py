from volunteer_event_coordination.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
from volunteer_event_coordination.settings import SettingsService

class AppServices:

    def __init__(self):
        settings = SettingsService().get_settings()
        self.db = MySQLPersistenceWrapper(settings)

    def get_all_users(self):
        return self.db.fetch_all("users")

    def create_user(self, data):
        return self.db.create_user(data)

    def update_user(self, user_id, data):
        return self.db.update_user(user_id, data)

    def delete_user(self, user_id):
        return self.db.delete_user(user_id)
