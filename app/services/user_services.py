from ..models import User, UserRoleEnum
from ..database import SessionLocal
from passlib.context import CryptContext
from fastapi import Depends, HTTPException 
from ..auth import get_current_user
from typing import Annotated


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db, username: str, email: str, password: str, phone_number: int,  role: UserRoleEnum):
    hashed_password = get_password_hash(password)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        phone_number= phone_number,
        role=role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db, email: str):
    return db.query(User).filter(User.email == email).first()

def  get_user_by_id( db, user_id : int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_details(user_id: int, role: UserRoleEnum, db: SessionLocal):  # type: ignore
    if role == UserRoleEnum.Employer:
        return db.query(User).filter(User.id == user_id, User.role == UserRoleEnum.Employer).first()
    elif role == UserRoleEnum.Jobseeker:
        return db.query(User).filter(User.id == user_id, User.role == UserRoleEnum.Jobseeker).first()
    else:
        return None
    
def authenticate_user(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
    role: UserRoleEnum
):
    if current_user.role != role:
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user 