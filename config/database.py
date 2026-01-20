"""
Database Configuration and Connection Module
Enhanced version with better error handling and utilities
"""

import mysql.connector
from mysql.connector import Error, pooling
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseConfig:
    """Database configuration class"""

    HOST = os.getenv("DB_HOST", "localhost")
    USER = os.getenv("DB_USER", "root")
    PASSWORD = os.getenv("DB_PASSWORD", "")
    DATABASE = os.getenv("DB_NAME", "student_grade_db")
    PORT = int(os.getenv("DB_PORT", 3306))

    # Connection pool config
    POOL_NAME = "student_pool"
    POOL_SIZE = 5


class Database:
    """Database connection and operations handler"""

    _connection_pool = None

    def __init__(self):
        self.connection = None
        self.cursor = None
        self._initialize_pool()

    @classmethod
    def _initialize_pool(cls):
        """Initialize connection pool (singleton pattern)"""
        if cls._connection_pool is None:
            try:
                cls._connection_pool = pooling.MySQLConnectionPool(
                    pool_name=DatabaseConfig.POOL_NAME,
                    pool_size=DatabaseConfig.POOL_SIZE,
                    pool_reset_session=True,
                    host=DatabaseConfig.HOST,
                    user=DatabaseConfig.USER,
                    password=DatabaseConfig.PASSWORD,
                    database=DatabaseConfig.DATABASE,
                    port=DatabaseConfig.PORT,
                )
                print("✓ Connection pool created successfully")
            except Error as e:
                print(f"✗ Error creating connection pool: {e}")

    def connect(self):
        """Establish database connection from pool"""
        try:
            self.connection = self._connection_pool.get_connection()

            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                db_info = self.connection.get_server_info()
                print(f"✓ Connected to MySQL Server version {db_info}")

                self.cursor.execute("SELECT DATABASE();")
                record = self.cursor.fetchone()
                print(f"✓ Connected to database: {record['DATABASE()']}")

                return True

        except Error as e:
            print(f"✗ Error connecting to MySQL: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("✓ MySQL connection closed")

    def execute_query(self, query, params=None):
        """
        Execute a single query (INSERT, UPDATE, DELETE)
        Returns: True if successful, False otherwise
        """
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Error as e:
            print(f"✗ Error executing query: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            self.connection.rollback()
            return False

    def fetch_one(self, query, params=None):
        """
        Fetch single row
        Returns: Dictionary or None
        """
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Error as e:
            print(f"✗ Error fetching data: {e}")
            print(f"Query: {query}")
            return None

    def fetch_all(self, query, params=None):
        """
        Fetch all rows
        Returns: List of dictionaries or empty list
        """
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Error fetching data: {e}")
            print(f"Query: {query}")
            return []

    def get_last_insert_id(self):
        """Get last inserted ID"""
        return self.cursor.lastrowid

    def execute_many(self, query, data_list):
        """
        Execute query with multiple data sets
        Useful for bulk insert
        """
        try:
            self.cursor.executemany(query, data_list)
            self.connection.commit()
            return True
        except Error as e:
            print(f"✗ Error executing many: {e}")
            self.connection.rollback()
            return False

    def table_exists(self, table_name):
        """Check if table exists"""
        query = """
            SELECT COUNT(*)
            FROM information_schema.tables 
            WHERE table_schema = %s 
            AND table_name = %s
        """
        result = self.fetch_one(query, (DatabaseConfig.DATABASE, table_name))
        return result and result["COUNT(*)"] > 0


# Test connection function
def test_connection():
    """Test database connection"""
    print("\n" + "=" * 60)
    print("Testing Database Connection...")
    print("=" * 60 + "\n")

    db = Database()

    if db.connect():
        # Test table exists
        print("\nChecking tables...")
        tables = ["students", "courses", "grades"]
        for table in tables:
            exists = db.table_exists(table)
            status = "✓" if exists else "✗"
            print(f"{status} Table '{table}': {'exists' if exists else 'not found'}")

        # Test query
        print("\nTesting sample query...")
        students = db.fetch_all("SELECT * FROM students LIMIT 3")

        if students:
            print(f"\n✓ Found {len(students)} students:")
            for student in students:
                print(f"  - {student['nim']}: {student['name']} ({student['major']})")

        db.disconnect()
        return True
    else:
        print("\n✗ Connection failed!")
        return False


if __name__ == "__main__":
    test_connection()
