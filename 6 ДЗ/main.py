from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi_redis_cache import FastApiRedisCache, cache
from sqlalchemy.orm import Session
from typing import List
import csv
import time
from datetime import timedelta
from models import Base, Student
from database import engine, get_db
import os

app = FastAPI()


# Инициализация Redis
@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=os.environ.get("REDIS_URL", "redis://localhost:6379"),
        prefix="myapi-cache",
        response_header="X-MyAPI-Cache",
        ignore_arg_types=[Session]
    )


# Модель для удаления студентов
class DeleteRequest(BaseModel):
    student_ids: List[int]


# Фоновая задача для загрузки данных из CSV
def load_data_from_csv(file_path: str, db: Session):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                student = Student(
                    last_name=row['Фамилия'],
                    first_name=row['Имя'],
                    faculty=row['Факультет'],
                    course=row['Курс'],
                    grade=float(row['Оценка'])
                )
                db.add(student)
            db.commit()
    except Exception as e:
        db.rollback()
        raise e


# Фоновая задача для удаления студентов
def delete_students(student_ids: List[int], db: Session):
    try:
        db.query(Student).filter(Student.id.in_(student_ids)).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


# Эндпоинт для загрузки данных из CSV (фоновая задача)
@app.post("/students/load_csv")
async def load_csv(
        file_path: str,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    background_tasks.add_task(load_data_from_csv, file_path, db)
    return {"message": "Data loading started in background"}


# Эндпоинт для удаления студентов (фоновая задача)
@app.post("/students/delete")
async def delete_students_endpoint(
        delete_request: DeleteRequest,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    background_tasks.add_task(delete_students, delete_request.student_ids, db)
    return {"message": "Deletion process started in background"}


# Кешированные эндпоинты
@app.get("/students/", response_model=List[Student])
@cache(expire=timedelta(minutes=5))
async def read_all_students(db: Session = Depends(get_db)):
    time.sleep(2)  # Имитация долгого запроса
    return db.query(Student).all()


@app.get("/students/{student_id}", response_model=Student)
@cache(expire=timedelta(minutes=5))
async def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.get("/students/faculty/{faculty}", response_model=List[Student])
@cache(expire=timedelta(minutes=5))
async def get_students_by_faculty(faculty: str, db: Session = Depends(get_db)):
    return db.query(Student).filter(Student.faculty == faculty).all()