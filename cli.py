# cli.py
"""
Simple console-based frontend for the Homework / Assignment Tracker.
Run with: python cli.py
"""

from dal import (
    list_users,
    create_user,
    list_courses,
    list_assignments_for_course,
    create_assignment,
    list_submissions_for_assignment,
    create_submission,
)

def pause():
    input("\nPress Enter to continue...")

def show_users():
    users = list_users()
    print("\nUsers:")
    for u in users:
        print(f"{u['id']}: {u['username']} ({u.get('full_name')}) role={u.get('role')}")

def show_courses():
    courses = list_courses()
    print("\nCourses:")
    for c in courses:
        print(f"{c['id']}: {c['code']} - {c['title']} ({c.get('term')})")

def show_assignments():
    course_id = input("Enter course id: ").strip()
    try:
        course_id = int(course_id)
    except ValueError:
        print("Invalid course id")
        return
    assignments = list_assignments_for_course(course_id)
    print("\nAssignments:")
    for a in assignments:
        print(f"{a['id']}: {a['title']} due={a.get('due_date')} pts={a.get('points')}")

def add_submission():
    show_users()
    user_id = input("Enter your user id: ").strip()
    show_assignments()
    assignment_id = input("Enter assignment id: ").strip()
    try:
        user_id = int(user_id)
        assignment_id = int(assignment_id)
    except ValueError:
        print("Invalid id")
        return
    submission_id = create_submission(assignment_id, user_id)
    print(f"Submission created with id {submission_id}")

def show_submissions():
    assignment_id = input("Enter assignment id: ").strip()
    try:
        assignment_id = int(assignment_id)
    except ValueError:
        print("Invalid assignment id")
        return
    submissions = list_submissions_for_assignment(assignment_id)
    print("\nSubmissions:")
    for s in submissions:
        print(
            f"{s['id']}: user={s['user_id']} "
            f"submitted_at={s.get('submitted_at')} "
            f"score={s.get('score')}"
        )

def main():
    while True:
        print("\n=== Homework Tracker CLI ===")
        print("1) List users")
        print("2) List courses")
        print("3) View assignments for a course")
        print("4) Submit an assignment")
        print("5) View submissions for an assignment")
        print("6) Quit")

        choice = input("Choice: ").strip()

        if choice == "1":
            show_users()
            pause()
        elif choice == "2":
            show_courses()
            pause()
        elif choice == "3":
            show_assignments()
            pause()
        elif choice == "4":
            add_submission()
            pause()
        elif choice == "5":
            show_submissions()
            pause()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()

