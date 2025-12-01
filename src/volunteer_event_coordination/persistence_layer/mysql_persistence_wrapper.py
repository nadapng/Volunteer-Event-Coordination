import mysql.connector.pooling

class MySQLPersistenceWrapper:

    def __init__(self, config_dict):
        self.config = config_dict.get("connection", {}).get("config", {})
        self.pool_settings = config_dict.get("connection", {}).get("pool", {})

        # Create connection pool
        self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="volunteer_pool",
            pool_size=self.pool_settings.get("size", 5),
            **self.config
        )

    # -----------------------------
    # Fetch ALL records
    # -----------------------------
    def fetch_all(self, table):
        conn = self.connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table}")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    # -----------------------------
    # Create User
    # -----------------------------
    def create_user(self, user_data):
        conn = self.connection_pool.get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO users (first_name, last_name, email)
            VALUES (%s, %s, %s)
        """
        values = (
            user_data["first_name"],
            user_data["last_name"],
            user_data["email"]
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()
        return True

    # -----------------------------
    # Update User
    # -----------------------------
    def update_user(self, user_id, updated_data):
        conn = self.connection_pool.get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE users
            SET first_name=%s, last_name=%s, email=%s
            WHERE user_id=%s
        """
        values = (
            updated_data["first_name"],
            updated_data["last_name"],
            updated_data["email"],
            user_id
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()
        return True

    # -----------------------------
    # Delete User
    # -----------------------------
    def delete_user(self, user_id):
        conn = self.connection_pool.get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM users WHERE user_id=%s"
        cursor.execute(sql, (user_id,))
        conn.commit()

        cursor.close()
        conn.close()
        return True
