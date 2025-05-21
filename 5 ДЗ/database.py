from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, User
from passlib.context import CryptContext
import csv

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Database:
    def __init__(self, db_url="sqlite:///students.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_user_by_username(self, username: str):
        session = self.Session()
        user = session.query(User).filter(User.username == username).first()
        session.close()
        return user

    def create_user(self, username: str, email: str, password: str, is_superuser: bool = False):
        session = self.Session()
        hashed_password = pwd_context.hash(password)
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_superuser=is_superuser
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return user

    # ... остальные методы из предыдущего задания ...