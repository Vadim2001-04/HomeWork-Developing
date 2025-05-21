from models import Base, Student
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv

class Database:
    def __init__(self, db_url="sqlite:///students.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def insert_student(self, last_name, first_name, faculty, course, grade):
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
        session.close()

    def get_students_by_faculty(self, faculty):
        session = self.Session()
        students = session.query(Student).filter(Student.faculty == faculty).all()
        session.close()
        return students

    def get_unique_courses(self):
        session = self.Session()
        courses = session.query(Student.course).distinct().all()
        session.close()
        return [course[0] for course in courses]

    def get_average_grade_by_faculty(self, faculty):
        session = self.Session()
        avg_grade = session.query(func.avg(Student.grade)).filter(Student.faculty == faculty).scalar()
        session.close()
        return avg_grade

    def get_students_with_low_grades(self, course, threshold=30):
        session = self.Session()
        students = session.query(Student).filter(
            Student.course == course,
            Student.grade < threshold
        ).all()
        session.close()
        return students

    def load_from_csv(self, file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.insert_student(
                    last_name=row['Фамилия'],
                    first_name=row['Имя'],
                    faculty=row['Факультет'],
                    course=row['Курс'],
                    grade=float(row['Оценка'])
                )