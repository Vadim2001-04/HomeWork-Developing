from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from database import Database
from models import Student

app = FastAPI()
db = Database()

class StudentCreate(BaseModel):
    last_name: str
    first_name: str
    faculty: str
    course: str
    grade: float

class StudentUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    faculty: Optional[str] = None
    course: Optional[str] = None
    grade: Optional[float] = None

@app.post("/students/", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate):
    return db.create_student(
        last_name=student.last_name,
        first_name=student.first_name,
        faculty=student.faculty,
        course=student.course,
        grade=student.grade
    )

@app.get("/students/", response_model=List[Student])
async def read_all_students():
    return db.get_all_students()

@app.get("/students/{student_id}", response_model=Student)
async def read_student(student_id: int):
    student = db.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: int, student_update: StudentUpdate):
    student = db.update_student(student_id, **student_update.dict(exclude_unset=True))
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int):
    if not db.delete_student(student_id):
        raise HTTPException(status_code=404, detail="Student not found")

# Эндпоинты из предыдущего задания
@app.post("/students/load_csv", status_code=status.HTTP_201_CREATED)
async def load_csv():
    count = db.load_from_csv("students.csv")
    return {"message": f"Successfully loaded {count} students from CSV"}

@app.get("/students/faculty/{faculty}", response_model=List[Student])
async def get_students_by_faculty(faculty: str):
    return db.get_students_by_faculty(faculty)

@app.get("/courses/unique", response_model=List[str])
async def get_unique_courses():
    return db.get_unique_courses()

@app.get("/faculty/{faculty}/average", response_model=float)
async def get_average_grade(faculty: str):
    avg = db.get_average_grade_by_faculty(faculty)
    if avg is None:
        raise HTTPException(status_code=404, detail="Faculty not found or no students")
    return avg