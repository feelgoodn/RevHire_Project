from .routers import jobposting, jobapplication, user
from .database import Base, engine
from fastapi import  FastAPI
from typing import Annotated
from . import database
from fastapi import Depends, FastAPI, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt




Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/docs")
async def welcome():
    return {"message": "Welcome to the RevHire!"}

app.include_router(jobposting.router)
app.include_router(jobapplication.router)
app.include_router(user.router)

