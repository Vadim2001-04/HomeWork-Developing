from fastapi import FastAPI
from database import Database
from models import Student
from typing import List

app = FastAPI()
db = Database()

@app.post("/students/load_csv")
async def load_csv():
    db.load_from_csv("students.csv")
    return {"message": "Data loaded successfully from CSV"}

@app.get("/students/faculty/{faculty}", response_model=List[dict])
async def get_students_by_faculty(faculty: str):
    students = db.get_students_by_faculty(faculty)
    return [
        {
            "last_name": s.last_name,
            "first_name": s.first_name,
            "faculty": s.faculty,
            "course": s.course,
            "grade": s.grade
        }
        for s in students
    ]

@app.get("/courses/unique", response_model=List[str])
async def get_unique_courses():
    return db.get_unique_courses()

@app.get("/faculty/{faculty}/average", response_model=float)
async def get_average_grade(faculty: str):
    return db.get_average_grade_by_faculty(faculty)

@app.get("/courses/{course}/low_grades", response_model=List[dict])
async def get_students_with_low_grades(course: str):
    students = db.get_students_with_low_grades(course)
    return [
        {
            "last_name": s.last_name,
            "first_name": s.first_name,
            "faculty": s.faculty,
            "grade": s.grade
        }
        for s in students
    ]