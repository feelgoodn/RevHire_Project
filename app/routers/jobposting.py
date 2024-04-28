from typing import List
from fastapi import Depends, HTTPException, Header, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from ..models import Job
from ..schemas import JobPostCreate, User, UserRoleEnum, View_JobPost
from ..services import user_services


router = APIRouter(
    tags=['JobPosting'])


@router.post("/job_postings")
async def create_job_post(
    job_post_create: JobPostCreate,
    token: str = Header(...),
    current_user: User = Depends(user_services.get_current_active_user),
    db: Session = Depends(get_db),
):
    try:
        current_user = await user_services.get_current_active_user(current_user, UserRoleEnum.Employer)
        job_post = Job(**job_post_create.dict(), user_id=current_user.id)
        db.add(job_post)
        db.commit()
        db.refresh(job_post)
        return {"message": "Job post created successfully"}
    except Exception:
        error_message = "Failed to create job post due to an internal server error."
        raise HTTPException(status_code=500, detail=error_message)

@router.get("/view_jobposts", response_model=List[View_JobPost])
async def get_job_postings(
    token: str = Header(...),
    current_user: User = Depends(user_services.get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        current_user = await user_services.get_current_active_user(current_user, UserRoleEnum.Employer)
        job_posts = db.query(Job).filter(Job.user_id == current_user.id).all()
        return job_posts
    except Exception:
        error_message = "Failed to retrieve job posts due to an internal server error."
        raise HTTPException(status_code=500, detail=error_message)

@router.put("/update_post")
async def update_job_post(
    job_post_id: int,
    job_post_create: JobPostCreate,
    token: str = Header(...),
    current_user: User = Depends(user_services.get_current_active_user),
    db: Session = Depends(get_db),
):
    try:
        current_user = await user_services.get_current_active_user(current_user, UserRoleEnum.Employer)
        job_post = db.query(Job).filter(Job.id == job_post_id).first()
        if not job_post:
            raise HTTPException(status_code=404, detail="Job post not found")
        if job_post.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to update this job post")
        for field, value in job_post_create.dict().items():
            setattr(job_post, field, value)
        db.commit()
        db.refresh(job_post)
        return {"message": "Job post updated successfully"}
    except Exception:
        error_message = "Failed to update job post."
        raise HTTPException(status_code=500, detail=error_message)

@router.delete("/delete_post")
async def delete_job_post(
    job_post_id: int,
    token: str = Header(...),
    current_user: User = Depends(user_services.get_current_active_user),
    db: Session = Depends(get_db),
):
    try:
        current_user = await user_services.get_current_active_user(current_user, UserRoleEnum.Employer)
        job_post = db.query(Job).filter(Job.id == job_post_id).first()
        if not job_post:
            raise HTTPException(status_code=404, detail="Job post not found")
        if job_post.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to delete this job post")
        db.delete(job_post)
        db.commit()
        return {"message": "Job post deleted successfully"}
    except Exception:
        error_message = "Failed to delete job post."
        raise HTTPException(status_code=500, detail=error_message)


    

    







