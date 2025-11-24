from mysql.connector import pooling
from volunteer_event_coordination.application_base import ApplicationBase


class MySQLPersistenceWrapper(ApplicationBase):

    def __init__(self, config_dict):
        super().__init__("MySQLPersistenceWrapper", "mysql_persistence_db")

        # Read connection settings
        self.config = config_dict.get("connection", {}).get("config", {})
        self.pool_settings = config_dict.get("connection", {}).get("pool", {})

        self.connection_pool = None
        self.initialize_connection_pool()

    # ================================
    # Initialize Connection Pool
    # ================================
    def initialize_connection_pool(self):
        print("🔍 DEBUG CONFIG:", self.config)
        print("🔍 DEBUG POOL:", self.pool_settings)

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
    # Get Connection
    # ================================
    def get_connection(self):
        try:
            return self.connection_pool.get_connection()
        except Exception as e:
            self.logger.log_error(f"❌ get_connection error: {str(e)}")
            return None

    @property
    def connection(self):
        return self.get_connection()

    # ================================
    # Fetch All Records
    # ================================
    def fetch_all(self, table_name):
        try:
            conn = self.get_connection()
            cur = conn.cursor()

            cur.execute(f"SELECT * FROM {table_name}")
            results = cur.fetchall()

            cur.close()
            conn.close()
            return results

        except Exception as e:
            self.logger.log_error(f"❌ fetch_all error: {str(e)}")
            return []

    # ================================
    # Insert Record
    # ================================
    def insert_record(self, table_name, data_dict):
        try:
            conn = self.get_connection()
            cur = conn.cursor()

            columns = ", ".join(data_dict.keys())
            placeholders = ", ".join(["%s"] * len(data_dict))
            values = tuple(data_dict.values())

            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cur.execute(query, values)
            conn.commit()

            cur.close()
            conn.close()
            return True

        except Exception as e:
            self.logger.log_error(f"❌ insert_record error: {str(e)}")
            return False

    # ================================
    # Get record by ID
    # ================================
    def get_by_id(self, table_name, id_column, record_id):
        try:
            conn = self.get_connection()
            cur = conn.cursor()

            query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"
            cur.execute(query, (record_id,))
            result = cur.fetchone()

            cur.close()
            conn.close()
            return result

        except Exception as e:
            self.logger.log_error(f"❌ get_by_id error: {str(e)}")
            return None

    # ================================
    # Update record
    # ================================
    def update_record(self, table_name, id_column, record_id, data_dict):
        try:
            conn = self.get_connection()
            cur = conn.cursor()

            set_clause = ", ".join([f"{col} = %s" for col in data_dict.keys()])
            values = list(data_dict.values())
            values.append(record_id)

            query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = %s"
            cur.execute(query, values)
            conn.commit()

            cur.close()
            conn.close()
            return True

        except Exception as e:
            self.logger.log_error(f"❌ update_record error: {str(e)}")
            return False

    # ================================
    # Delete record
    # ================================
    def delete_record(self, table_name, id_column, record_id):
        try:
            conn = self.get_connection()
            cur = conn.cursor()

            query = f"DELETE FROM {table_name} WHERE {id_column} = %s"
            cur.execute(query, (record_id,))
            conn.commit()

            cur.close()
            conn.close()
            return True

        except Exception as e:
            self.logger.log_error(f"❌ delete_record error: {str(e)}")
            return False

    # ================================
    # Create User Record (extra)
    # ================================
    def create_user(self, user_data):
        try:
            return self.insert_record("users", user_data)
        except Exception as e:
            self.logger.log_error(f"❌ create_user error: {str(e)}")
            return False
