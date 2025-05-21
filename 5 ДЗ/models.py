from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    faculty = Column(String)
    course = Column(String)
    grade = Column(Float)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)