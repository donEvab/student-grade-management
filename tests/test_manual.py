"""
Manual testing script for Student model
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.student import Student


def main():
    print("\n" + "=" * 60)
    print("Student Model - Manual Testing")
    print("=" * 60 + "\n")

    student = Student()

    while True:
        print("\nOptions:")
        print("1. Create student")
        print("2. Find student by NIM")
        print("3. List all students")
        print("4. Update student")
        print("5. Delete student")
        print("6. Search by name")
        print("7. Exit")

        choice = input("\nEnter choice (1-7): ").strip()

        if choice == "1":
            nim = input("NIM: ")
            name = input("Name: ")
            major = input("Major: ")
            email = input("Email (optional): ")
            phone = input("Phone (optional): ")

            student.create(nim, name, major, email or None, phone or None)

        elif choice == "2":
            nim = input("Enter NIM: ")
            data = student.find_by_nim(nim)
            if data:
                print(f"\nID: {data['id']}")
                print(f"NIM: {data['nim']}")
                print(f"Name: {data['name']}")
                print(f"Major: {data['major']}")
                print(f"Email: {data['email']}")
                print(f"Phone: {data['phone']}")
            else:
                print("Student not found")

        elif choice == "3":
            students = student.find_all()
            print(f"\nTotal: {len(students)} students\n")
            for s in students:
                print(f"{s['nim']} - {s['name']} ({s['major']})")

        elif choice == "4":
            id = int(input("Student ID: "))
            name = input("New name (press Enter to skip): ")
            major = input("New major (press Enter to skip): ")
            email = input("New email (press Enter to skip): ")

            updates = {}
            if name:
                updates["name"] = name
            if major:
                updates["major"] = major
            if email:
                updates["email"] = email

            student.update(id, **updates)

        elif choice == "5":
            id = int(input("Student ID to delete: "))
            confirm = input("Are you sure? (yes/no): ")
            if confirm.lower() == "yes":
                student.delete(id)

        elif choice == "6":
            name = input("Enter name to search: ")
            results = student.search_by_name(name)
            print(f"\nFound {len(results)} result(s):")
            for s in results:
                print(f"{s['nim']} - {s['name']}")

        elif choice == "7":
            print("\nGoodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
