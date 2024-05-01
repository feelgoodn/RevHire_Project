from datetime import timedelta
from typing import List
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException, status
from app.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from ..services import user_services
from ..schemas import  UserRoleEnum, UserCreate,Token, ShowUser, User
from ..database import get_db, SessionLocal


router = APIRouter(
    tags=['User']
)

@router.post("/login", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = user_services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user", response_model=ShowUser)
async def get_users(current_user: User = Depends(user_services.get_current_user)):
    return current_user

@router.post("/signup/{role}/", response_model=User)
async def register_user(
    role: UserRoleEnum,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    if user_services.get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if user_services.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_services.create_user(
        db, user_data.username, user_data.email, user_data.password, user_data.phone_number, role
    )

@router.put("/update", response_model=User)
async def update_user_me(
    user_data: UserCreate,
    current_user: User = Depends(user_services.get_current_user),
    db: Session = Depends(get_db)
):
    user = user_services.get_user_by_username(db, current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_data.username
    user.email = user_data.email
    user.hashed_password = user_services.get_password_hash(user_data.password)
    user.phone_number = user_data.phone_number
    db.commit()
    db.refresh(user)
    return user

          
    
