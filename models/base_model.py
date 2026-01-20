"""
Base Model Class
All models will inherit from this class
"""

from config.database import Database


class BaseModel:
    """Base class for all models"""

    table_name = None  # To be overridden in child classes

    def __init__(self):
        """Initialize database connection"""
        self.db = Database()
        self.db.connect()

    def __del__(self):
        """Cleanup: close database connection"""
        if hasattr(self, "db"):
            self.db.disconnect()

    def create(self, data):
        """
        Generic create method
        To be overridden in child classes
        """
        raise NotImplementedError("Create method must be implemented in child class")

    def find_by_id(self, id):
        """
        Find record by ID
        Returns: Dictionary or None
        """
        if not self.table_name:
            raise ValueError("table_name must be set in child class")

        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        return self.db.fetch_one(query, (id,))

    def find_all(self, limit=None):
        """
        Get all records
        Returns: List of dictionaries
        """
        if not self.table_name:
            raise ValueError("table_name must be set in child class")

        query = f"SELECT * FROM {self.table_name}"
        if limit:
            query += f" LIMIT {limit}"

        return self.db.fetch_all(query)

    def update(self, id, data):
        """
        Generic update method
        To be overridden in child classes
        """
        raise NotImplementedError("Update method must be implemented in child class")

    def delete(self, id):
        """
        Delete record by ID
        Returns: True if successful, False otherwise
        """
        if not self.table_name:
            raise ValueError("table_name must be set in child class")

        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        return self.db.execute_query(query, (id,))

    def count(self):
        """
        Count total records
        Returns: Integer
        """
        if not self.table_name:
            raise ValueError("table_name must be set in child class")

        query = f"SELECT COUNT(*) as total FROM {self.table_name}"
        result = self.db.fetch_one(query)
        return result["total"] if result else 0
