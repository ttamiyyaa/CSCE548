# client.py
"""
Simple console client that calls the FastAPI service.
Run this in a separate terminal while uvicorn is running:
python client.py
"""

import requests
BASE = "http://127.0.0.1:8000"

def pause():
    input("\nPress Enter to continue...")

def list_courses():
    r = requests.get(f"{BASE}/courses")
    if r.status_code != 200:
        print("Error:", r.status_code, r.text); return
    rows = r.json()
    print("\nCourses:")
    for c in rows:
        print(f"{c['id']}: {c['code']} - {c['title']} ({c.get('term')})")

def list_assignments():
    cid = input("Enter course id: ").strip()
    try:
        cid = int(cid)
    except:
        print("Invalid id"); return
    r = requests.get(f"{BASE}/assignments/{cid}")
    if r.status_code != 200:
        print("Error:", r.status_code, r.text); return
    rows = r.json()
    print(f"\nAssignments for course {cid}:")
    for a in rows:
        print(f"{a['id']}: {a['title']} due:{a.get('due_date')} pts:{a.get('points')}")

def submit():
    try:
        uid = int(input("Your user id: ").strip())
        aid = int(input("Assignment id: ").strip())
    except:
        print("Invalid id"); return
    content = input("Optional content: ").strip()
    payload = {"user_id": uid, "assignment_id": aid, "content": content or None}
    r = requests.post(f"{BASE}/submissions", json=payload)
    if r.status_code == 200:
        print("Submission created:", r.json())
    else:
        print("Error:", r.status_code, r.text)

def main():
    while True:
        print("\n=== Service Client ===")
        print("1) List courses")
        print("2) List assignments for course")
        print("3) Submit assignment (via service)")
        print("4) Quit")
        choice = input("Choice: ").strip()
        if choice == '1':
            list_courses(); pause()
        elif choice == '2':
            list_assignments(); pause()
        elif choice == '3':
            submit(); pause()
        elif choice == '4':
            break
        else:
            print("Invalid")

if __name__ == "__main__":
    main()

