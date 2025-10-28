"""Defines the MySQLPersistenceWrapper class."""

from application_name.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import MySQLConnectionPool
import inspect
import json


class MySQLPersistenceWrapper(ApplicationBase):
    """Implements the MySQLPersistenceWrapper class."""

    def __init__(self, config: dict) -> None:
        """Initializes object."""
        self._config_dict = config
        self.META = config["meta"]
        self.DATABASE = config["database"]
        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"]
        )
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: It works!')

        # Database Configuration Constants
        self.DB_CONFIG = {
            'database': self.DATABASE["connection"]["config"]["database"],
            'user': self.DATABASE["connection"]["config"]["user"],
            'password': self.DATABASE["connection"]["config"]["password"],
            'host': self.DATABASE["connection"]["config"]["host"],
            'port': self.DATABASE["connection"]["config"]["port"]
        }

        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: DB Connection Config Dict: {self.DB_CONFIG}'
        )

        # Database Connection
        self._connection_pool = self._initialize_database_connection_pool(self.DB_CONFIG)

        # 🔹 اختبار الاتصال بقاعدة البيانات
        try:
            test_conn = connector.connect(**self.DB_CONFIG)
            if test_conn.is_connected():
                print("✅ Database connection successful!")
                test_conn.close()
        except connector.Error as err:
            print(f"❌ Database connection failed: {err}")

        # SQL String Constants
        self.SQL_SELECT_VOLUNTEERS = "SELECT * FROM volunteers"
        self.SQL_INSERT_VOLUNTEER = (
            "INSERT INTO volunteers (name, email, phone, role) VALUES (%s, %s, %s, %s)"
        )

    # MySQLPersistenceWrapper Methods
    def get_all_volunteers(self):
        """Fetch and print all volunteers from the database."""
        try:
            conn = self._connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(self.SQL_SELECT_VOLUNTEERS)
            results = cursor.fetchall()

            print("\n🧾 Volunteers List:")
            if not results:
                print("No volunteers found.")
            else:
                for row in results:
                    print(row)

            cursor.close()
            conn.close()

        except connector.Error as err:
            print(f"❌ Database error: {err}")

    def add_volunteer(self, name, email, phone, role):
        """Add a new volunteer to the database."""
        try:
            conn = self._connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(self.SQL_INSERT_VOLUNTEER, (name, email, phone, role))
            conn.commit()
            print(f"✅ Volunteer '{name}' added successfully!")
            cursor.close()
            conn.close()
        except connector.Error as err:
            print(f"❌ Failed to add volunteer: {err}")

    ##### Private Utility Methods #####
    def _initialize_database_connection_pool(self, config: dict) -> MySQLConnectionPool:
        """Initializes database connection pool."""
        try:
            self._logger.log_debug('Creating connection pool...')
            cnx_pool = MySQLConnectionPool(
                pool_name=self.DATABASE["pool"]["name"],
                pool_size=self.DATABASE["pool"]["size"],
                pool_reset_session=self.DATABASE["pool"]["reset_session"],
                **config
            )
            self._logger.log_debug('Connection pool successfully created!')
            return cnx_pool
        except connector.Error as err:
            self._logger.log_error(f'Problem creating connection pool: {err}')
            self._logger.log_error(f'Check DB config:\n{json.dumps(self.DATABASE)}')
        except Exception as e:
            self._logger.log_error(f'Problem creating connection pool: {e}')
            self._logger.log_error(f'Check DB conf:\n{json.dumps(self.DATABASE)}')
