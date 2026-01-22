"""
Grade Model
Handles all grade-related database operations
Includes automatic grade letter calculation
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.base_model import BaseModel


class Grade(BaseModel):
    """Grade model class"""

    table_name = "grades"

    @staticmethod
    def calculate_grade_letter(score):
        """
        Convert numeric score to grade letter

        Grade Scale:
        A: 85-100
        B: 70-84
        C: 60-69
        D: 50-59
        E: 0-49

        Args:
            score (float): Numeric score (0-100)

        Returns:
            str: Grade letter (A, B, C, D, E)
        """
        if score >= 85:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "E"

    @staticmethod
    def grade_to_gpa(grade_letter):
        """
        Convert grade letter to GPA point

        Args:
            grade_letter (str): Grade letter

        Returns:
            float: GPA point
        """
        gpa_scale = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "E": 0.0}
        return gpa_scale.get(grade_letter, 0.0)

    def create(self, student_id, course_id, score, semester, academic_year):
        """
        Create new grade entry
        Grade letter is automatically calculated from score

        Args:
            student_id (int): Student ID
            course_id (int): Course ID
            score (float): Numeric score (0-100)
            semester (int): Semester number
            academic_year (str): Academic year (e.g., "2021/2022")

        Returns:
            int: ID of created grade, or None if failed
        """
        # Validate required fields
        if not student_id or not course_id or score is None:
            print("✗ Error: Student ID, course ID, and score are required")
            return None

        # Validate score range
        if score < 0 or score > 100:
            print("✗ Error: Score must be between 0 and 100")
            return None

        # Validate semester
        if semester < 1 or semester > 8:
            print("✗ Error: Semester must be between 1 and 8")
            return None

        # Check if grade already exists for this student-course combination
        existing = self.find_by_student_course(
            student_id, course_id, semester, academic_year
        )
        if existing:
            print(
                f"✗ Error: Grade already exists for this student-course in {academic_year}"
            )
            return None

        # Auto-calculate grade letter
        grade_letter = self.calculate_grade_letter(score)

        query = """
            INSERT INTO grades 
            (student_id, course_id, score, grade_letter, semester, academic_year)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (student_id, course_id, score, grade_letter, semester, academic_year)

        if self.db.execute_query(query, params):
            grade_id = self.db.get_last_insert_id()
            print(f"✓ Grade created: Score {score} = {grade_letter} (ID: {grade_id})")
            return grade_id

        return None

    def find_by_student_course(self, student_id, course_id, semester, academic_year):
        """
        Find grade for specific student-course combination

        Args:
            student_id (int): Student ID
            course_id (int): Course ID
            semester (int): Semester number
            academic_year (str): Academic year

        Returns:
            dict: Grade data or None
        """
        query = """
            SELECT * FROM grades 
            WHERE student_id = %s 
            AND course_id = %s 
            AND semester = %s
            AND academic_year = %s
        """
        return self.db.fetch_one(
            query, (student_id, course_id, semester, academic_year)
        )

    def get_student_grades(self, student_id):
        """
        Get all grades for a student

        Args:
            student_id (int): Student ID

        Returns:
            list: List of grades with course info
        """
        query = """
            SELECT 
                g.id, g.score, g.grade_letter, g.semester, g.academic_year,
                c.code, c.name as course_name, c.credits
            FROM grades g
            JOIN courses c ON g.course_id = c.id
            WHERE g.student_id = %s
            ORDER BY g.semester, c.code
        """
        return self.db.fetch_all(query, (student_id,))

    def get_course_grades(self, course_id):
        """
        Get all grades for a course

        Args:
            course_id (int): Course ID

        Returns:
            list: List of grades with student info
        """
        query = """
            SELECT 
                g.id, g.score, g.grade_letter, g.semester, g.academic_year,
                s.nim, s.name as student_name, s.major
            FROM grades g
            JOIN students s ON g.student_id = s.id
            WHERE g.course_id = %s
            ORDER BY s.nim
        """
        return self.db.fetch_all(query, (course_id,))

    def get_student_transcript(self, student_id):
        """
        Generate student transcript with all details

        Args:
            student_id (int): Student ID

        Returns:
            dict: Transcript data with grades and GPA
        """
        # Get student info
        from models.student import Student

        student_model = Student()
        student = student_model.find_by_id(student_id)

        if not student:
            print(f"✗ Error: Student with ID {student_id} not found")
            return None

        # Get all grades
        grades = self.get_student_grades(student_id)

        # Calculate GPA
        total_points = 0
        total_credits = 0

        for grade in grades:
            gpa_point = self.grade_to_gpa(grade["grade_letter"])
            credits = grade["credits"]
            total_points += gpa_point * credits
            total_credits += credits

        gpa = total_points / total_credits if total_credits > 0 else 0.0

        return {
            "student": student,
            "grades": grades,
            "total_credits": total_credits,
            "gpa": round(gpa, 2),
        }

    def update(self, id, score):
        """
        Update grade score
        Grade letter is automatically recalculated

        Args:
            id (int): Grade ID
            score (float): New score

        Returns:
            bool: True if successful, False otherwise
        """
        # Check if grade exists
        grade = self.find_by_id(id)
        if not grade:
            print(f"✗ Error: Grade with ID {id} not found")
            return False

        # Validate score
        if score < 0 or score > 100:
            print("✗ Error: Score must be between 0 and 100")
            return False

        # Auto-calculate new grade letter
        grade_letter = self.calculate_grade_letter(score)

        query = """
            UPDATE grades 
            SET score = %s, grade_letter = %s
            WHERE id = %s
        """

        if self.db.execute_query(query, (score, grade_letter, id)):
            print(f"✓ Grade updated: Score {score} = {grade_letter}")
            return True

        return False

    def delete(self, id):
        """
        Delete grade entry

        Args:
            id (int): Grade ID

        Returns:
            bool: True if successful, False otherwise
        """
        grade = self.find_by_id(id)
        if not grade:
            print(f"✗ Error: Grade with ID {id} not found")
            return False

        query = "DELETE FROM grades WHERE id = %s"

        if self.db.execute_query(query, (id,)):
            print(f"✓ Grade ID {id} deleted successfully")
            return True

        return False

    def get_grade_distribution(self, course_id=None):
        """
        Get grade distribution statistics

        Args:
            course_id (int, optional): Filter by course ID

        Returns:
            dict: Distribution of grades (A, B, C, D, E)
        """
        if course_id:
            query = """
                SELECT grade_letter, COUNT(*) as count
                FROM grades
                WHERE course_id = %s
                GROUP BY grade_letter
                ORDER BY grade_letter
            """
            results = self.db.fetch_all(query, (course_id,))
        else:
            query = """
                SELECT grade_letter, COUNT(*) as count
                FROM grades
                GROUP BY grade_letter
                ORDER BY grade_letter
            """
            results = self.db.fetch_all(query)

        distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
        for row in results:
            distribution[row["grade_letter"]] = row["count"]

        return distribution


# Manual testing function
def test_grade_model():
    """Test Grade model operations"""
    print("\n" + "=" * 60)
    print("Testing Grade Model Operations")
    print("=" * 60 + "\n")

    grade = Grade()

    # Test 1: Grade calculation
    print("1. Testing GRADE CALCULATION...")
    test_scores = [95, 80, 65, 55, 40]
    for score in test_scores:
        letter = grade.calculate_grade_letter(score)
        gpa = grade.grade_to_gpa(letter)
        print(f"   Score {score} = {letter} (GPA: {gpa})")
    print()

    # Test 2: Create grade
    print("2. Testing CREATE...")
    new_id = grade.create(
        student_id=1, course_id=1, score=88.5, semester=1, academic_year="2024/2025"
    )

    if new_id:
        print(f"   Grade created with ID: {new_id}\n")

    # Test 3: Get student grades
    print("3. Testing GET STUDENT GRADES...")
    grades = grade.get_student_grades(1)
    print(f"   Found {len(grades)} grade(s) for student ID 1")
    if grades:
        for g in grades[:3]:  # Show first 3
            print(f"   - {g['code']}: {g['score']} ({g['grade_letter']})")
    print()

    # Test 4: Get transcript
    print("4. Testing GET TRANSCRIPT...")
    transcript = grade.get_student_transcript(1)
    if transcript:
        print(f"   Student: {transcript['student']['name']}")
        print(f"   Total Credits: {transcript['total_credits']}")
        print(f"   GPA: {transcript['gpa']}\n")

    # Test 5: Update grade
    print("5. Testing UPDATE...")
    if new_id:
        grade.update(new_id, 92.0)
        updated = grade.find_by_id(new_id)
        if updated:
            print(f"   Updated: {updated['score']} ({updated['grade_letter']})\n")

    # Test 6: Grade distribution
    print("6. Testing GRADE DISTRIBUTION...")
    dist = grade.get_grade_distribution()
    print("   Distribution:")
    for letter, count in dist.items():
        print(f"   {letter}: {count}")
    print()

    # Test 7: Delete
    print("7. Testing DELETE...")
    if new_id:
        grade.delete(new_id)
        deleted = grade.find_by_id(new_id)
        if not deleted:
            print("   ✓ Grade deleted and verified\n")

    print("=" * 60)
    print("All tests completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    test_grade_model()
