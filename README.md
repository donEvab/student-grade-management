# Student Grade Management System

A comprehensive Python-based application for managing student grades, courses, and generating academic statistics.

## 🎯 Features (Planned)

- Student CRUD operations
- Course management
- Grade recording and calculation
- Statistical analysis (GPA, grade distribution)
- Student transcript generation
- Grade reports per course

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Database:** MySQL (via XAMPP)
- **Libraries:**
  - mysql-connector-python (Database connectivity)
  - pandas (Data manipulation)
  - tabulate (Table display)
  - python-dotenv (Environment variables)

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- XAMPP (MySQL)
- Git

### Setup Steps

1. Clone repository

```bash
git clone <https://github.com/donEvab/student-grade-management.git>
cd student-grade-management
```

2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Setup database

- Start XAMPP (Apache & MySQL)
- Open phpMyAdmin: `http://localhost/phpmyadmin`
- Import `database/schema.sql`

5. Configure environment

- Copy `.env.example` to `.env`
- Update database credentials if needed

6. Test connection

```bash
python config/database.py
```

## 📊 Database Schema

### Students

- id, nim, name, major, email, phone

### Courses

- id, code, name, credits, semester, description

### Grades

- id, student_id, course_id, score, grade_letter, semester, academic_year

## 🚀 Usage

```bash
python main.py
```

## 📅 Development Progress

- [x] Day 1: Database setup and schema design
- [ ] Day 2: Models and database connection
- [ ] Day 3: Course and grade models
- [ ] Day 4: Statistics and validation
- [ ] Day 5: Controllers
- [ ] Day 6: CLI interface
- [ ] Day 7: Documentation and testing

## 👨‍💻 Author

**Your Name**

- GitHub: [@donEvab]
- Email: revanacc2@gmail.com

## 📝 License

This project is for educational purposes.

---

**Last Updated:** Day 1 - January 19, 2026
