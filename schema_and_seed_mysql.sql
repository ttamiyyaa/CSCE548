-- schema_and_seed_mysql.sql
-- Homework / Assignment Tracker (MySQL)

SET FOREIGN_KEY_CHECKS = 0;
DROP DATABASE IF EXISTS homework_tracker;
SET FOREIGN_KEY_CHECKS = 1;

CREATE DATABASE homework_tracker;
USE homework_tracker;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  full_name VARCHAR(100),
  email VARCHAR(200),
  role ENUM('student','instructor') DEFAULT 'student'
);

CREATE TABLE courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(20) NOT NULL,
  title VARCHAR(200) NOT NULL,
  term VARCHAR(50)
);

CREATE TABLE enrollments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  course_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE assignments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  course_id INT NOT NULL,
  title VARCHAR(200) NOT NULL,
  due_date DATETIME,
  points INT DEFAULT 100,
  FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE submissions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  assignment_id INT NOT NULL,
  user_id INT NOT NULL,
  submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  score INT,
  FOREIGN KEY (assignment_id) REFERENCES assignments(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Seed data
INSERT INTO users (username, full_name, role) VALUES
('alice','Alice Johnson','student'),
('bob','Bob Smith','student'),
('carla','Carla Gomez','student'),
('dan','Dan Lee','student'),
('prof_m','Prof Miller','instructor');

INSERT INTO courses (code, title, term) VALUES
('CSCE548','Software Engineering','Spring 2026'),
('CSCE520','Databases','Spring 2026'),
('MATH101','Calculus I','Fall 2025');

INSERT INTO enrollments (user_id, course_id) VALUES
(1,1),(2,1),(3,1),(4,1),
(1,2),(2,2),(3,2),
(1,3),(2,3);

INSERT INTO assignments (course_id, title, due_date, points) VALUES
(1,'Project 1','2026-02-20 23:59:00',100),
(1,'Homework 1','2026-02-05 23:59:00',10),
(1,'Homework 2','2026-02-12 23:59:00',10),
(1,'Midterm','2026-03-01 09:00:00',200),
(2,'DB HW1','2026-02-10 23:59:00',50),
(2,'DB Project','2026-03-25 23:59:00',150),
(3,'Calc HW1','2025-10-05 23:59:00',20),
(3,'Calc Midterm','2025-10-20 09:00:00',150);

INSERT INTO submissions (assignment_id, user_id, score) VALUES
(1,1,95),(1,2,88),(1,3,92),(1,4,70),
(2,1,10),(2,2,9),(2,3,10),
(3,1,10),(3,2,8),
(4,1,180),(4,2,160),
(5,1,48),(5,2,45),
(6,1,140),(6,3,130),
(7,1,18),(7,2,19),
(8,2,140),(8,3,135),
(1,1,90),(2,1,10),(3,1,9),(4,2,150);

