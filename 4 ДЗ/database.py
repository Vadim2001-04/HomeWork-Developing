from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, Student
import csv


class Database:
    def __init__(self, db_url="sqlite:///students.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_student(self, last_name: str, first_name: str, faculty: str, course: str, grade: float) -> Student:
        session = self.Session()
        student = Student(
            last_name=last_name,
            first_name=first_name,
            faculty=faculty,
            course=course,
            grade=grade
        )
        session.add(student)
        session.commit()
        session.refresh(student)
        session.close()
        return student

    def get_student(self, student_id: int) -> Student:
        session = self.Session()
        student = session.query(Student).filter(Student.id == student_id).first()
        session.close()
        return student

    def get_all_students(self) -> list[Student]:
        session = self.Session()
        students = session.query(Student).all()
        session.close()
        return students

    def update_student(self, student_id: int, **kwargs) -> Student:
        session = self.Session()
        student = session.query(Student).filter(Student.id == student_id).first()
        if not student:
            session.close()
            return None

        for key, value in kwargs.items():
            if hasattr(student, key):
                setattr(student, key, value)

        session.commit()
        session.refresh(student)
        session.close()
        return student

    def delete_student(self, student_id: int) -> bool:
        session = self.Session()
        student = session.query(Student).filter(Student.id == student_id).first()
        if not student:
            session.close()
            return False

        session.delete(student)
        session.commit()
        session.close()
        return True

    def get_students_by_faculty(self, faculty: str) -> list[Student]:
        session = self.Session()
        students = session.query(Student).filter(Student.faculty == faculty).all()
        session.close()
        return students

    def get_unique_courses(self) -> list[str]:
        session = self.Session()
        courses = session.query(Student.course).distinct().all()
        session.close()
        return [course[0] for course in courses]

    def get_average_grade_by_faculty(self, faculty: str) -> float:
        session = self.Session()
        avg_grade = session.query(func.avg(Student.grade)).filter(Student.faculty == faculty).scalar()
        session.close()
        return avg_grade

    def load_from_csv(self, file_path: str) -> int:
        count = 0
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.create_student(
                    last_name=row['Фамилия'],
                    first_name=row['Имя'],
                    faculty=row['Факультет'],
                    course=row['Курс'],
                    grade=float(row['Оценка'])
                )
                count += 1
        return count