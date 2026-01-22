"""
Day 3 comprehensive tests
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.course import Course
from models.grade import Grade
from models.student import Student


def test_course_grade_integration():
    """Test integration between Course and Grade models"""
    print("\n" + "=" * 60)
    print("Testing Course-Grade Integration")
    print("=" * 60 + "\n")

    # Create instances
    student = Student()
    course = Course()
    grade = Grade()

    # Get existing student and course
    s = student.find_by_nim("2021001")
    c = course.find_by_code("CAK1BAB3")

    if s and c:
        print(f"✓ Found student: {s['name']}")
        print(f"✓ Found course: {c['name']}")

        # Create grade
        grade_id = grade.create(
            student_id=s["id"],
            course_id=c["id"],
            score=87.5,
            semester=1,
            academic_year="2024/2025",
        )

        if grade_id:
            # Get transcript
            transcript = grade.get_student_transcript(s["id"])
            print(f"\n✓ Transcript generated")
            print(f"  GPA: {transcript['gpa']}")
            print(f"  Total Credits: {transcript['total_credits']}")

            # Cleanup
            grade.delete(grade_id)
            print(f"\n✓ Test data cleaned up")

    print("\n" + "=" * 60)
    print("Integration test completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    test_course_grade_integration()
