from volunteer_event_coordination.application_base import ApplicationBase
import mysql.connector
from mysql.connector import pooling

class MySQLPersistenceWrapper(ApplicationBase):

    def __init__(self, config_dict):
        super().__init__("MySQLPersistenceWrapper", "mysql_persistence_db")

        self.config = config_dict.get("connection", {}).get("config", {})
        self.pool_settings = config_dict.get("connection", {}).get("pool", {})
        self.connection_pool = None
        self.initialize_connection_pool()

    # ================================
    # Initialize Connection Pool
    # ================================
    def initialize_connection_pool(self):
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name=self.pool_settings.get("name", "volunteer_pool"),
                pool_size=self.pool_settings.get("size", 5),
                host=self.config.get("host", "localhost"),
                port=self.config.get("port", 3306),
                user=self.config.get("user", "root"),
                password=self.config.get("password", ""),
                database=self.config.get("database", "volunteer_event_db"),
                use_pure=self.config.get("use_pure", True)
            )
            self.logger.log_info("✅ Database connection pool initialized successfully.")

        except Exception as e:
            self.logger.log_error(f"❌ Failed to initialize database connection pool: {str(e)}")

    # ================================
    # Fetch ALL rows
    # ================================
    def fetch_all(self, table_name):
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM {table_name};")
            results = cursor.fetchall()

            cursor.close()
            connection.close()
            return results

        except Exception as e:
            self.logger.log_error(f"❌ fetch_all error: {str(e)}")
            return []

    # ================================
    # Get table columns
    # ================================
    def get_columns(self, table_name):
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()

            cursor.execute(f"DESCRIBE {table_name};")
            columns = cursor.fetchall()

            cursor.close()
            connection.close()

            column_names = [col[0] for col in columns]
            return column_names

        except Exception as e:
            self.logger.log_error(f"❌ get_columns error: {str(e)}")
            return []

    # ================================
    # Insert record
    # ================================
    def insert_record(self, table_name, data_dict):
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()

            columns = ", ".join(data_dict.keys())
            placeholders = ", ".join(["%s"] * len(data_dict))
            values = tuple(data_dict.values())

            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()
            return True

        except Exception as e:
            self.logger.log_error(f"❌ insert_record error: {str(e)}")
            return False
