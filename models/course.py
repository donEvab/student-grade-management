"""
Course Model
Handles all course-related database operations
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.base_model import BaseModel


class Course(BaseModel):
    """Course model class"""

    table_name = "courses"

    def create(self, code, name, credits, semester, description=None):
        """
        Create new course

        Args:
            code (str): Course code (unique, e.g., CAK1BAB3)
            name (str): Course name
            credits (int): Number of credits (1-6)
            semester (int): Semester number (1-8)
            description (str, optional): Course description

        Returns:
            int: ID of created course, or None if failed
        """
        # Validate required fields
        if not code or not name or not credits or not semester:
            print("✗ Error: Code, name, credits, and semester are required")
            return None

        # Validate credits range
        if credits < 1 or credits > 6:
            print("✗ Error: Credits must be between 1 and 6")
            return None

        # Validate semester range
        if semester < 1 or semester > 8:
            print("✗ Error: Semester must be between 1 and 8")
            return None

        # Check if code already exists
        if self.find_by_code(code):
            print(f"✗ Error: Course with code {code} already exists")
            return None

        query = """
            INSERT INTO courses (code, name, credits, semester, description)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (code, name, credits, semester, description)

        if self.db.execute_query(query, params):
            course_id = self.db.get_last_insert_id()
            print(f"✓ Course created successfully with ID: {course_id}")
            return course_id

        return None

    def find_by_code(self, code):
        """
        Find course by code

        Args:
            code (str): Course code

        Returns:
            dict: Course data or None
        """
        query = "SELECT * FROM courses WHERE code = %s"
        return self.db.fetch_one(query, (code,))

    def find_by_semester(self, semester):
        """
        Find all courses in a semester

        Args:
            semester (int): Semester number

        Returns:
            list: List of courses
        """
        query = """
            SELECT * FROM courses 
            WHERE semester = %s 
            ORDER BY code
        """
        return self.db.fetch_all(query, (semester,))

    def search_by_name(self, name):
        """
        Search courses by name (partial match)

        Args:
            name (str): Name to search

        Returns:
            list: List of matching courses
        """
        query = "SELECT * FROM courses WHERE name LIKE %s ORDER BY name"
        return self.db.fetch_all(query, (f"%{name}%",))

    def get_by_credits(self, credits):
        """
        Find courses by credit hours

        Args:
            credits (int): Number of credits

        Returns:
            list: List of courses
        """
        query = """
            SELECT * FROM courses 
            WHERE credits = %s 
            ORDER BY semester, code
        """
        return self.db.fetch_all(query, (credits,))

    def update(self, id, **kwargs):
        """
        Update course information

        Args:
            id (int): Course ID
            **kwargs: Fields to update (name, credits, semester, description)

        Returns:
            bool: True if successful, False otherwise
        """
        # Check if course exists
        course = self.find_by_id(id)
        if not course:
            print(f"✗ Error: Course with ID {id} not found")
            return False

        # Build update query dynamically
        allowed_fields = ["name", "credits", "semester", "description"]
        update_fields = []
        params = []

        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                # Validate credits and semester
                if field == "credits" and (value < 1 or value > 6):
                    print("✗ Error: Credits must be between 1 and 6")
                    return False
                if field == "semester" and (value < 1 or value > 8):
                    print("✗ Error: Semester must be between 1 and 8")
                    return False

                update_fields.append(f"{field} = %s")
                params.append(value)

        if not update_fields:
            print("✗ Error: No valid fields to update")
            return False

        params.append(id)

        query = f"""
            UPDATE courses 
            SET {', '.join(update_fields)}
            WHERE id = %s
        """

        if self.db.execute_query(query, tuple(params)):
            print(f"✓ Course ID {id} updated successfully")
            return True

        return False

    def delete(self, id):
        """
        Delete course
        Note: This will also delete related grades (CASCADE)

        Args:
            id (int): Course ID

        Returns:
            bool: True if successful, False otherwise
        """
        course = self.find_by_id(id)
        if not course:
            print(f"✗ Error: Course with ID {id} not found")
            return False

        query = "DELETE FROM courses WHERE id = %s"

        if self.db.execute_query(query, (id,)):
            print(f"✓ Course ID {id} ({course['code']}) deleted successfully")
            return True

        return False

    def get_total_credits_by_semester(self, semester):
        """
        Calculate total credits in a semester

        Args:
            semester (int): Semester number

        Returns:
            int: Total credits
        """
        query = """
            SELECT SUM(credits) as total_credits 
            FROM courses 
            WHERE semester = %s
        """
        result = self.db.fetch_one(query, (semester,))
        return result["total_credits"] if result and result["total_credits"] else 0

    def get_students_enrolled(self, course_id):
        """
        Get all students enrolled in a course

        Args:
            course_id (int): Course ID

        Returns:
            list: List of students with their grades
        """
        query = """
            SELECT 
                s.id, s.nim, s.name, s.major,
                g.score, g.grade_letter
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE g.course_id = %s
            ORDER BY s.nim
        """
        return self.db.fetch_all(query, (course_id,))


# Manual testing function
def test_course_model():
    """Test Course model CRUD operations"""
    print("\n" + "=" * 60)
    print("Testing Course Model CRUD Operations")
    print("=" * 60 + "\n")

    course = Course()

    # Test 1: Create course
    print("1. Testing CREATE...")
    new_id = course.create(
        code="TEST999",
        name="Test Course",
        credits=3,
        semester=1,
        description="Testing course model",
    )

    if new_id:
        print(f"   Course created with ID: {new_id}\n")

    # Test 2: Read by ID
    print("2. Testing READ by ID...")
    data = course.find_by_id(new_id)
    if data:
        print(f"   Found: {data['code']} - {data['name']}\n")

    # Test 3: Read by code
    print("3. Testing READ by code...")
    data = course.find_by_code("TEST999")
    if data:
        print(f"   Found: {data['name']} ({data['credits']} SKS)\n")

    # Test 4: Find by semester
    print("4. Testing FIND by semester...")
    courses = course.find_by_semester(1)
    print(f"   Found {len(courses)} course(s) in semester 1\n")

    # Test 5: Update
    print("5. Testing UPDATE...")
    success = course.update(new_id, name="Test Course Updated", credits=4)

    if success:
        updated = course.find_by_id(new_id)
        print(f"   Updated name: {updated['name']}")
        print(f"   Updated credits: {updated['credits']}\n")

    # Test 6: Get total credits
    print("6. Testing GET TOTAL CREDITS...")
    total = course.get_total_credits_by_semester(1)
    print(f"   Total credits in semester 1: {total} SKS\n")

    # Test 7: Delete
    print("7. Testing DELETE...")
    course.delete(new_id)

    # Verify deletion
    deleted = course.find_by_id(new_id)
    if not deleted:
        print("   ✓ Course deleted and verified\n")

    print("=" * 60)
    print("All tests completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    test_course_model()
