import json
import inspect
import mysql.connector as connector
from mysql.connector import pooling
from application_name.application_base import ApplicationBase


class MySQLPersistenceWrapper(ApplicationBase):
    """Handles all database interactions"""

    def __init__(self, config):
        super().__init__(subclass_name=self.__class__.__name__,
                         logfile_prefix_name="mysql_persistence_wrapper")
        self.DATABASE = config["connection"]["config"]

        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: It works!")
        self._logger.log_debug(f"{inspect.currentframe().f_code.co_name}: DB Connection Config Dict: {self.DATABASE}")

        try:
            self._connection_pool = self._initialize_database_connection_pool(config)
            print("✅ Database connection successful!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")

    # -------------------------------------------------------------------------
    # Database pool initialization
    # -------------------------------------------------------------------------
    def _initialize_database_connection_pool(self, config):
        """Creates a reusable connection pool"""
        try:
            self._logger.log_debug("Creating connection pool...")
            pool = pooling.MySQLConnectionPool(
                pool_name=config["connection"]["pool"]["name"],
                pool_size=config["connection"]["pool"]["size"],
                pool_reset_session=config["connection"]["pool"]["reset_session"],
                **self.DATABASE
            )
            return pool
        except Exception as e:
            self._logger.log_error(f"Problem creating connection pool: {e}")
            self._logger.log_error(f"Check DB conf:\n{json.dumps(config['connection'], indent=4)}")
            raise e

    # -------------------------------------------------------------------------
    # Add volunteer (example)
    # -------------------------------------------------------------------------
    def add_volunteer(self, name, email, phone, role):
        """Adds a volunteer record"""
        try:
            conn = self._connection_pool.get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO volunteers (name, email, phone, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, phone, role))
            conn.commit()
            print(f"✅ Volunteer '{name}' added successfully!")
        except connector.Error as err:
            print(f"❌ Failed to add volunteer: {err}")
        finally:
            cursor.close()
            conn.close()

    # -------------------------------------------------------------------------
    # Show all tables
    # -------------------------------------------------------------------------
    def show_tables(self):
        """Displays all tables in the connected database"""
        try:
            conn = self._connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("\n📋 Tables in database:")
            if tables:
                for t in tables:
                    print(f"   - {t[0]}")
            else:
                print("   (No tables found yet)")
        except Exception as e:
            print(f"❌ Error showing tables: {e}")
        finally:
            cursor.close()
            conn.close()

    # -------------------------------------------------------------------------
    # Create volunteers table
    # -------------------------------------------------------------------------
    def create_volunteers_table(self):
        """Creates the volunteers table if it doesn't exist"""
        try:
            conn = self._connection_pool.get_connection()
            cursor = conn.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS volunteers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                role VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(query)
            conn.commit()
            print("✅ Table 'volunteers' created successfully!")
        except Exception as e:
            print(f"❌ Error creating volunteers table: {e}")
        finally:
            cursor.close()
            conn.close()

    # -------------------------------------------------------------------------
    # Create events table
    # -------------------------------------------------------------------------
    def create_events_table(self):
        """Creates the events table if it doesn't exist"""
        try:
            conn = self._connection_pool.get_connection()
            cursor = conn.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                event_date DATE NOT NULL,
                location VARCHAR(100),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(query)
            conn.commit()
            print("✅ Table 'events' created successfully!")
        except Exception as e:
            print(f"❌ Error creating events table: {e}")
        finally:
            cursor.close()
            conn.close()
        # -------------------------------------------------------------------------
    # Create volunteer_event_xref table
    # -------------------------------------------------------------------------
    def create_volunteer_event_xref_table(self):
        """Creates the volunteer_event_xref table to link volunteers and events"""
        try:
            conn = self._connection_pool.get_connection()
            cursor = conn.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS volunteer_event_xref (
                id INT AUTO_INCREMENT PRIMARY KEY,
                volunteer_id INT NOT NULL,
                event_id INT NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE,
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
            );
            """
            cursor.execute(query)
            conn.commit()
            print("✅ Table 'volunteer_event_xref' created successfully!")
        except Exception as e:
            print(f"❌ Error creating volunteer_event_xref table: {e}")
        finally:
            cursor.close()
            conn.close()
