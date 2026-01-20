"""
Student Model
Handles all student-related database operations
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Baru import yang lain
from models.base_model import BaseModel
from datetime import datetime


class Student(BaseModel):
    """Student model class"""

    table_name = "students"

    def create(self, nim, name, major, email=None, phone=None):
        """
        Create new student

        Args:
            nim (str): Student ID number (unique)
            name (str): Student full name
            major (str): Student major/program
            email (str, optional): Student email
            phone (str, optional): Student phone number

        Returns:
            int: ID of created student, or None if failed
        """
        # Validate required fields
        if not nim or not name or not major:
            print("✗ Error: NIM, name, and major are required")
            return None

        # Check if NIM already exists
        if self.find_by_nim(nim):
            print(f"✗ Error: Student with NIM {nim} already exists")
            return None

        query = """
            INSERT INTO students (nim, name, major, email, phone)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (nim, name, major, email, phone)

        if self.db.execute_query(query, params):
            student_id = self.db.get_last_insert_id()
            print(f"✓ Student created successfully with ID: {student_id}")
            return student_id

        return None

    def find_by_nim(self, nim):
        """
        Find student by NIM

        Args:
            nim (str): Student ID number

        Returns:
            dict: Student data or None
        """
        query = "SELECT * FROM students WHERE nim = %s"
        return self.db.fetch_one(query, (nim,))

    def find_by_email(self, email):
        """
        Find student by email

        Args:
            email (str): Student email

        Returns:
            dict: Student data or None
        """
        query = "SELECT * FROM students WHERE email = %s"
        return self.db.fetch_one(query, (email,))

    def search_by_name(self, name):
        """
        Search students by name (partial match)

        Args:
            name (str): Name to search

        Returns:
            list: List of matching students
        """
        query = "SELECT * FROM students WHERE name LIKE %s"
        return self.db.fetch_all(query, (f"%{name}%",))

    def find_by_major(self, major):
        """
        Find all students in a major

        Args:
            major (str): Major name

        Returns:
            list: List of students
        """
        query = "SELECT * FROM students WHERE major = %s ORDER BY name"
        return self.db.fetch_all(query, (major,))

    def update(self, id, **kwargs):
        """
        Update student information

        Args:
            id (int): Student ID
            **kwargs: Fields to update (name, major, email, phone)

        Returns:
            bool: True if successful, False otherwise
        """
        # Check if student exists
        student = self.find_by_id(id)
        if not student:
            print(f"✗ Error: Student with ID {id} not found")
            return False

        # Build update query dynamically
        allowed_fields = ["name", "major", "email", "phone"]
        update_fields = []
        params = []

        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                update_fields.append(f"{field} = %s")
                params.append(value)

        if not update_fields:
            print("✗ Error: No valid fields to update")
            return False

        # Add ID to params
        params.append(id)

        query = f"""
            UPDATE students 
            SET {', '.join(update_fields)}
            WHERE id = %s
        """

        if self.db.execute_query(query, tuple(params)):
            print(f"✓ Student ID {id} updated successfully")
            return True

        return False

    def delete(self, id):
        """
        Delete student
        Note: This will also delete related grades (CASCADE)

        Args:
            id (int): Student ID

        Returns:
            bool: True if successful, False otherwise
        """
        # Check if student exists
        student = self.find_by_id(id)
        if not student:
            print(f"✗ Error: Student with ID {id} not found")
            return False

        query = "DELETE FROM students WHERE id = %s"

        if self.db.execute_query(query, (id,)):
            print(f"✓ Student ID {id} ({student['name']}) deleted successfully")
            return True

        return False

    def get_all_majors(self):
        """
        Get list of all unique majors

        Returns:
            list: List of major names
        """
        query = "SELECT DISTINCT major FROM students ORDER BY major"
        results = self.db.fetch_all(query)
        return [r["major"] for r in results]

    def count_by_major(self, major):
        """
        Count students in a major

        Args:
            major (str): Major name

        Returns:
            int: Number of students
        """
        query = "SELECT COUNT(*) as total FROM students WHERE major = %s"
        result = self.db.fetch_one(query, (major,))
        return result["total"] if result else 0


# Manual testing function
def test_student_model():
    """Test Student model CRUD operations"""
    print("\n" + "=" * 60)
    print("Testing Student Model CRUD Operations")
    print("=" * 60 + "\n")

    student = Student()

    # Test 1: Create student
    print("1. Testing CREATE...")
    new_id = student.create(
        nim="2021999",
        name="Test Student",
        major="Teknik Informatika",
        email="test@email.com",
        phone="08123456789",
    )

    if new_id:
        print(f"   Student created with ID: {new_id}\n")

    # Test 2: Read student by ID
    print("2. Testing READ by ID...")
    student_data = student.find_by_id(new_id)
    if student_data:
        print(f"   Found: {student_data['nim']} - {student_data['name']}\n")

    # Test 3: Read student by NIM
    print("3. Testing READ by NIM...")
    student_data = student.find_by_nim("2021999")
    if student_data:
        print(f"   Found: {student_data['name']} ({student_data['email']})\n")

    # Test 4: Search by name
    print("4. Testing SEARCH by name...")
    results = student.search_by_name("Test")
    print(f"   Found {len(results)} student(s)\n")

    # Test 5: Update student
    print("5. Testing UPDATE...")
    success = student.update(
        new_id, name="Test Student Updated", email="updated@email.com"
    )

    if success:
        updated = student.find_by_id(new_id)
        print(f"   Updated name: {updated['name']}")
        print(f"   Updated email: {updated['email']}\n")

    # Test 6: Count students
    print("6. Testing COUNT...")
    total = student.count()
    print(f"   Total students in database: {total}\n")

    # Test 7: Get all majors
    print("7. Testing GET ALL MAJORS...")
    majors = student.get_all_majors()
    print(f"   Available majors: {', '.join(majors)}\n")

    # Test 8: Delete student
    print("8. Testing DELETE...")
    student.delete(new_id)

    # Verify deletion
    deleted = student.find_by_id(new_id)
    if not deleted:
        print("   ✓ Student deleted and verified\n")

    print("=" * 60)
    print("All tests completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    test_student_model()
