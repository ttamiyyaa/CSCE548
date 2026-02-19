# business.py
"""
Business layer for Homework Tracker.
This layer sits between the service layer and the DAL.
It enforces validation and business rules.
"""

from datetime import datetime
from dal import get_user, get_assignment, create_submission, list_assignments_for_course

class BusinessError(Exception):
    pass

def ensure_user_exists(user_id):
    user = get_user(user_id)
    if not user:
        raise BusinessError(f"User {user_id} does not exist.")
    return user

def ensure_assignment_exists(assignment_id):
    assignment = get_assignment(assignment_id)
    if not assignment:
        raise BusinessError(f"Assignment {assignment_id} does not exist.")
    return assignment

def submit_assignment(user_id: int, assignment_id: int, content=None, score=None):
    """
    Business logic:
    - User must exist
    - Assignment must exist
    - Cannot submit after due date
    """
    user = ensure_user_exists(user_id)
    assignment = ensure_assignment_exists(assignment_id)

    due_date = assignment.get("due_date")

    # Optional rule: prevent late submissions
    if due_date:
        if isinstance(due_date, str):
            try:
                due_date = datetime.fromisoformat(due_date)
            except:
                due_date = None

        if due_date and datetime.now() > due_date:
            raise BusinessError("Cannot submit after due date.")

    submission_id = create_submission(
        assignment_id=assignment_id,
        user_id=user_id,
        content=content,
        score=score
    )

    return submission_id

def get_assignments_for_course(course_id: int):
    return list_assignments_for_course(course_id)

