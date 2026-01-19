-- ================================================
-- Student Grade Management System - Database Schema
-- ================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS student_grade_db;
USE student_grade_db;

-- Drop tables if exist (untuk development)
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;

-- ================================================
-- Table: students
-- ================================================

CREATE TABLE students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nim VARCHAR(20) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  major VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE,
  phone VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  INDEX idx_nim (nim),
  INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ================================================
-- Table: courses
-- ================================================

CREATE TABLE courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(20) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  credits INT NOT NULL CHECK (credits BETWEEN 1 AND 6),
  semester INT NOT NULL CHECK (semester BETWEEN 1 AND 8),
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  INDEX idx_code (code),
  INDEX idx_semester (semester)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ================================================
-- Table: grades
-- ================================================

CREATE TABLE grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    score DECIMAL(5,2) NOT NULL CHECK (score BETWEEN 0 AND 100),
    grade_letter CHAR(2) NOT NULL,
    semester INT NOT NULL CHECK (semester BETWEEN 1 AND 8),
    academic_year VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_student_course (student_id, course_id, semester, academic_year),
    INDEX idx_student (student_id),
    INDEX idx_course (course_id),
    INDEX idx_semester (semester)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ================================================
-- Insert Sample Data (untuk testing)
-- ================================================

-- Sample Students
INSERT INTO students (nim, name, major, email, phone) VALUES
('2021001', 'Ahmad Fauzi', 'Teknik Informatika', 'ahmad.fauzi@email.com', '081234567890'),
('2021002', 'Siti Nurhaliza', 'Sistem Informasi', 'siti.nur@email.com', '081234567891'),
('2021003', 'Budi Santoso', 'Teknik Informatika', 'budi.santoso@email.com', '081234567892'),
('2021004', 'Dewi Lestari', 'Sistem Informasi', 'dewi.lestari@email.com', '081234567893'),
('2021005', 'Eko Prasetyo', 'Teknik Informatika', 'eko.prasetyo@email.com', '081234567894');

-- Sample Courses (from your curriculum)
INSERT INTO courses (code, name, credits, semester, description) VALUES
('CAK1BAB3', 'Algoritma dan Pemrograman 1', 3, 1, 'Dasar-dasar algoritma dan pemrograman'),
('CAK1CAB3', 'Kalkulus', 3, 1, 'Matematika kalkulus dasar'),
('CAK1DAB3', 'Logika Matematika', 3, 1, 'Logika dan penalaran matematika'),
('CAK1EAB3', 'Matematika Diskrit', 3, 1, 'Struktur diskrit dalam matematika'),
('CAK1HDB2', 'Statistika', 2, 1, 'Statistika dasar dan probabilitas'),
('CAK1IAB4', 'Algoritma dan Pemrograman 2', 4, 2, 'Lanjutan algoritma dan pemrograman'),
('CAK1LAB3', 'Kalkulus Lanjut', 3, 2, 'Kalkulus tingkat lanjut'),
('CAK1MAB3', 'Matriks dan Ruang Vektor', 3, 2, 'Aljabar linear'),
('CAK2EAB4', 'Struktur Data', 4, 3, 'Struktur data dan algoritma'),
('CAK2DAB3', 'Sistem Operasi', 3, 3, 'Konsep sistem operasi');

-- Sample Grades
INSERT INTO grades (student_id, course_id, score, grade_letter, semester, academic_year) VALUES
-- Ahmad Fauzi - Semester 1
(1, 1, 85.5, 'A', 1, '2021/2022'),
(1, 2, 78.0, 'B', 1, '2021/2022'),
(1, 3, 88.5, 'A', 1, '2021/2022'),
(1, 4, 82.0, 'B', 1, '2021/2022'),
(1, 5, 90.0, 'A', 1, '2021/2022'),

-- Siti Nurhaliza - Semester 1
(2, 1, 92.0, 'A', 1, '2021/2022'),
(2, 2, 85.5, 'A', 1, '2021/2022'),
(2, 3, 88.0, 'A', 1, '2021/2022'),
(2, 4, 86.5, 'A', 1, '2021/2022'),
(2, 5, 89.0, 'A', 1, '2021/2022'),

-- Budi Santoso - Semester 1
(3, 1, 75.5, 'B', 1, '2021/2022'),
(3, 2, 70.0, 'B', 1, '2021/2022'),
(3, 3, 72.5, 'B', 1, '2021/2022'),
(3, 4, 78.0, 'B', 1, '2021/2022'),
(3, 5, 80.0, 'B', 1, '2021/2022');

-- ================================================
-- Verification Queries
-- ================================================

-- Check data
SELECT 'Students Count:' as Info, COUNT(*) as Count FROM students
UNION ALL
SELECT 'Courses Count:', COUNT(*) FROM courses
UNION ALL
SELECT 'Grades Count:', COUNT(*) FROM grades;

-- View student grades
SELECT 
    s.nim,
    s.name,
    c.code,
    c.name as course_name,
    g.score,
    g.grade_letter,
    g.semester
FROM grades g
JOIN students s ON g.student_id = s.id
JOIN courses c ON g.course_id = c.id
ORDER BY s.nim, g.semester;
