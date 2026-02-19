# service.py
"""
FastAPI service that exposes a minimal API for Homework Tracker.
Run: uvicorn service:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import business

app = FastAPI(title="Homework Tracker Service")

class SubmissionIn(BaseModel):
    user_id: int
    assignment_id: int
    content: Optional[str] = None
    score: Optional[float] = None

class CourseOut(BaseModel):
    id: int
    code: str
    title: str
    term: Optional[str] = None

class AssignmentOut(BaseModel):
    id: int
    course_id: int
    title: str
    due_date: Optional[str]
    points: Optional[int]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/courses", response_model=List[CourseOut])
def get_courses():
    # reuse DAL via import
    from dal import list_courses
    rows = list_courses()
    return rows

import datetime

@app.get("/assignments/{course_id}", response_model=List[AssignmentOut])
def get_assignments(course_id: int):
    try:
        rows = business.get_assignments_for_course(course_id)

        for r in rows:
            dd = r.get("due_date")
            if isinstance(dd, (datetime.datetime, datetime.date)):
                r["due_date"] = dd.isoformat()
            elif dd is None:
                r["due_date"] = None
            else:
                r["due_date"] = str(dd)

        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
       

@app.post("/submissions")
def post_submission(payload: SubmissionIn):
    try:
        sid = business.submit_assignment(
            user_id=payload.user_id,
            assignment_id=payload.assignment_id,
            content=payload.content,
            score=payload.score
        )
        return {"submission_id": sid}
    except business.BusinessError as be:
        raise HTTPException(status_code=400, detail=str(be))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

