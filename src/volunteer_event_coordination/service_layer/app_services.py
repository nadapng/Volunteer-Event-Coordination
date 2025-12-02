class AppServices:
    def __init__(self, db):
        self.db = db

    # -------------------------
    # USERS CRUD
    # -------------------------

    def get_all_users(self):
        return self.db.fetch_all("users")

    def create_user(self, data):
        return self.db.insert_record("users", data)

    def update_user(self, table, id_column, record_id, data):
        return self.db.update_record(table, id_column, record_id, data)

    def delete_user(self, table, id_column, record_id):
        return self.db.delete_record(table, id_column, record_id)
