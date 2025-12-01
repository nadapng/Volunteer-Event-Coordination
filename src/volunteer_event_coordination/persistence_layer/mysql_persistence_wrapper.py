import mysql.connector
from mysql.connector import Error


class MySQLPersistenceWrapper:
    def __init__(self, config):
        try:
            self.connection = mysql.connector.connect(
                host=config["connection"]["config"]["host"],
                port=config["connection"]["config"]["port"],
                user=config["connection"]["config"]["user"],
                password=config["connection"]["config"]["password"],
                database=config["connection"]["config"]["database"],
                use_pure=True
            )
        except Error as e:
            print(f"Error connecting to database: {e}")
            self.connection = None

    # -------------------------------------------------------------------------
    # CREATE USER (tests expect boolean True)
    # -------------------------------------------------------------------------
    def create_user(self, data: dict):
        self.insert_record("users", data)
        return True

    # -------------------------------------------------------------------------
    # INSERT
    # -------------------------------------------------------------------------
    def insert_record(self, table_name, data: dict):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        cursor = self.connection.cursor()
        cursor.execute(query, tuple(data.values()))
        self.connection.commit()

        return cursor.lastrowid

    # -------------------------------------------------------------------------
    # GET BY ID  (tests call: get_by_id("users", "user_id", last_id))
    # -------------------------------------------------------------------------
    def get_by_id(self, table_name, id_column, id_value):
        query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"

        cursor = self.connection.cursor()
        cursor.execute(query, (id_value,))
        return cursor.fetchone()

    # -------------------------------------------------------------------------
    # UPDATE (tests expect return True)
    # -------------------------------------------------------------------------
    def update_record(self, table_name, id_column, id_value, data: dict):
        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = %s"

        cursor = self.connection.cursor()
        cursor.execute(query, (*data.values(), id_value))
        self.connection.commit()

        return True  # required by tests

    # -------------------------------------------------------------------------
    # DELETE (tests expect return True)
    # -------------------------------------------------------------------------
    def delete_record(self, table_name, id_column, id_value):
        query = f"DELETE FROM {table_name} WHERE {id_column} = %s"

        cursor = self.connection.cursor()
        cursor.execute(query, (id_value,))
        self.connection.commit()

        return True  # required by tests

    # -------------------------------------------------------------------------
    # FETCH ALL (must return tuples NOT dicts)
    # -------------------------------------------------------------------------
    def fetch_all(self, table_name):
        query = f"SELECT * FROM {table_name}"

        cursor = self.connection.cursor()  # tuple mode
        cursor.execute(query)
        return cursor.fetchall()
