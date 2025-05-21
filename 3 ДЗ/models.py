from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    faculty = Column(String)
    course = Column(String)
    grade = Column(Float)

    def __repr__(self):
        return f"<Student(last_name='{self.last_name}', first_name='{self.first_name}', faculty='{self.faculty}', course='{self.course}', grade={self.grade})>"