from volunteer_event_coordination.application_base import ApplicationBase
from volunteer_event_coordination.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper

class AppServices(ApplicationBase):

    def __init__(self, config_dict):
        super().__init__("AppServices", "app_services")
        self.db = MySQLPersistenceWrapper(config_dict)

    # Fetch all rows
    def get_all_records(self, table_name):
        return self.db.fetch_all(table_name)

    # Get table columns
    def get_columns(self, table_name):
        return self.db.get_columns(table_name)

    # Insert new record
    def insert_record(self, table_name, data_dict):
        return self.db.insert_record(table_name, data_dict)
