from pydantic import BaseModel, EmailStr
from enum import Enum 
from .models import UserRoleEnum



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str 
    role: UserRoleEnum

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRoleEnum
    phone_number: int 
   

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: int 

class ShowUser(BaseModel):
    username: str
    email: str
    phone_number: int


class Job(BaseModel):
    company : str
    email : str
    title : str
    description : str
    location : str
    experience : str
    skills : str

class View_JobPost(BaseModel):
    title: str
    job_description: str
    user_id: int
    salary: int
    location: str
    experience: int

class JobPostCreate(BaseModel):
    title: str
    job_description: str
    salary: int
    location: str
    experience: int


class ApplicationCreate(BaseModel):
    job_title: str
    username: str
    email: EmailStr
    resume_link: str
    cover_letter: str

class Applicationshow(BaseModel):
    applicant_id: int
    job_title: str
    username: str
    email: str
    resume_link: str



    


   





