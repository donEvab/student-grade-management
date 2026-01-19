"""
Database Configuration and Connection Module
"""

import mysql.connector
from mysql.connector import Error
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


class Database:
    """Database connection and operations handler"""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=DatabaseConfig.HOST,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                database=DatabaseConfig.DATABASE,
                port=DatabaseConfig.PORT,
            )

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
        """Execute a single query (INSERT, UPDATE, DELETE)"""
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Error as e:
            print(f"✗ Error executing query: {e}")
            self.connection.rollback()
            return False

    def fetch_one(self, query, params=None):
        """Fetch single row"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Error as e:
            print(f"✗ Error fetching data: {e}")
            return None

    def fetch_all(self, query, params=None):
        """Fetch all rows"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Error fetching data: {e}")
            return []

    def get_last_insert_id(self):
        """Get last inserted ID"""
        return self.cursor.lastrowid


# Test connection function
def test_connection():
    """Test database connection"""
    print("\n" + "=" * 50)
    print("Testing Database Connection...")
    print("=" * 50 + "\n")

    db = Database()

    if db.connect():
        # Test query
        print("\nTesting sample query...")
        students = db.fetch_all("SELECT * FROM students LIMIT 3")

        if students:
            print(f"\n✓ Found {len(students)} students:")
            for student in students:
                print(f"  - {student['nim']}: {student['name']}")

        db.disconnect()
        return True
    else:
        print("\n✗ Connection failed!")
        return False


if __name__ == "__main__":
    test_connection()
