# COPYRIGHT Tamiya Shepherd
# CSCE 548 – Project 1  
Homework / Assignment Tracker

## Overview
This project is a console-based Homework / Assignment Tracker designed to model a real-world software project structure. It includes a relational database, a Python data access layer (DAL) with CRUD operations, and a simple console frontend to retrieve and manipulate records.

The project is designed to be extended throughout the semester.

---

## Tech Stack
- **Database:** MySQL
- **Language:** Python 3
- **Libraries:** mysql-connector-python, python-dotenv
- **Environment:** Python virtual environment (venv)

---

## Database Schema
The database contains **5 tables**:

- `users` – students and instructors  
- `courses` – academic courses  
- `enrollments` – many-to-many relationship between users and courses  
- `assignments` – assignments belonging to courses  
- `submissions` – student submissions for assignments  

Foreign keys are used to enforce relationships between tables.

---

## Setup Instructions

### 1. Database Setup
Run the SQL script to create and seed the database:

```bash
/usr/local/mysql/bin/mysql -u root -p < schema_and_seed_mysql.sql

## Project 2 – Business and Service Layers

Project 2 extends the Homework Tracker by adding:

- A **Business Layer** (`business.py`) that enforces validation rules.
- A **Service Layer** (`service.py`) implemented using FastAPI.
- A **Console Client** (`client.py`) that calls the service endpoints.

### How to Run Project 2

1. Activate the virtual environment: source venv/bin/activate

2. Start the service: uvicorn service:app --reload --port 8000

3. In a second terminal, run the client: python client.py

The client demonstrates:
- Retrieving courses
- Retrieving assignments
- Submitting assignments
- Business rule validation


