import mysql.connector

class MySQLPersistenceWrapper:
    def __init__(self, config):
        # Extract database config correctly
        db_cfg = config["database"]["connection"]["config"]

        # Create DB connection
        self.connection = mysql.connector.connect(
            host=db_cfg["host"],
            user=db_cfg["user"],
            password=db_cfg["password"],
            database=db_cfg["database"],
            port=db_cfg["port"],
            use_pure=db_cfg["use_pure"]
        )

    def fetch_all(self, table):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        result = cursor.fetchall()
        cursor.close()
        return result

    def insert_record(self, table, data):
        cursor = self.connection.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(data.values()))
        self.connection.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

    def get_by_id(self, table, key_column, key_value):
        cursor = self.connection.cursor()
        sql = f"SELECT * FROM {table} WHERE {key_column} = %s"
        cursor.execute(sql, (key_value,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def update_record(self, table, key_column, key_value, data):
        cursor = self.connection.cursor()
        set_clause = ", ".join([f"{col} = %s" for col in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {key_column} = %s"
        cursor.execute(sql, tuple(data.values()) + (key_value,))
        self.connection.commit()
        cursor.close()
        return True

    def delete_record(self, table, key_column, key_value):
        cursor = self.connection.cursor()
        sql = f"DELETE FROM {table} WHERE {key_column} = %s"
        cursor.execute(sql, (key_value,))
        self.connection.commit()
        cursor.close()
        return True
