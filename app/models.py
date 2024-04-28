from enum import Enum
from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship


class UserRoleEnum(str, Enum):
    Jobseeker = "Jobseeker"
    Employer = "Employer"

    def __str__(self):
        return str(self.value)




class User(Base):
    __tablename__ = "users"  
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone_number = Column(Integer)
    role = Column(SQLAlchemyEnum(UserRoleEnum))
    jobs = relationship("Job", back_populates="user")
    applications = relationship("Application", back_populates="applicant")


class Job(Base):
    __tablename__ = "jobposting"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    job_description = Column(String)
    location = Column(String)
    salary = Column(Integer)
    experience = Column(String)
    skills = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="jobs")



class Application(Base):
    __tablename__ = "application"
    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("users.id"))
    job_title = Column(String)
    username = Column(String)
    email= Column(String) 
    resume_link = Column(String)
    cover_letter = Column(String)
    applicant = relationship("User", back_populates="applications")
