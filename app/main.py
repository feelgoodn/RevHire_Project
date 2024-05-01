from .routers import jobposting, jobapplication, user
from .database import Base, engine
from fastapi import  FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "Welcome to the RevHire!"}

app.include_router(jobposting.router)
app.include_router(jobapplication.router)
app.include_router(user.router)

