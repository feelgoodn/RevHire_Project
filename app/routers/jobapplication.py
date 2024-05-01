from fastapi import Depends, HTTPException, Header, APIRouter
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from ..models import Application
from ..schemas import User, UserRoleEnum, Applicationshow , ApplicationCreate
from ..services import user_services


router = APIRouter(
    tags=['JobApplication']
    )


@router.get("/View_application", response_model=list[Applicationshow])
async def get_job_applications(
    token: str = Header(...),  
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user_services.get_current_active_user(current_user, UserRoleEnum.Jobseeker)
    try:
        job_applications = db.query().filter(Application.user_id == current_user.id).all()
        return job_applications
    except Exception :
        error_message = "Failed to retrieve job application."
        raise HTTPException(status_code=500, detail=error_message)
    

@router.post("/post_application")
async def create_job_application(
    job_application_create: ApplicationCreate,  
    token: str = Header(...),  
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        current_user = await user_services.get_current_active_user(current_user, UserRoleEnum.Jobseeker)
        job_application = Application(**job_application_create.dict(), applicant_id=current_user.id)

        db.add(job_application)
        db.commit()
        db.refresh(job_application)

        return {"message": "Job application posted successfully"}
    except Exception:
        error_message = "Failed to post job application."
        raise HTTPException(status_code=500, detail=error_message)
    

@router.put("/update_application")
async def update_job_application(   
    job_id: int,
    job_application_create: ApplicationCreate,
    token: str = Header(...),  
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user_services.get_current_active_user(current_user, UserRoleEnum.Jobseeker)
    try:
        job_application = db.query(Application).filter(Application.id == job_id).first()
        if not job_application:
            raise HTTPException(status_code=404, detail="Job application not found.")
        if job_application.applicant_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to update this job application.")
        for field, value in job_application_create.dict().items():
            setattr(job_application, field, value)
        db.commit()
        db.refresh(job_application)
        return {"message": "Job application updated successfully"}
    except Exception:
        error_message = "Failed to update job application."
        raise HTTPException(status_code=500, detail=error_message)


@router.delete("/delete_application")
async def delete_job_application(
    job_id: int,
    token: str = Header(...),  
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user_services.get_current_active_user(current_user, UserRoleEnum.Jobseeker)
    try:
        job_application = db.query(Application).filter(Application.id == job_id).first()
        if not job_application:
            raise HTTPException(status_code=404, detail="Job application not found.")
        if job_application.applicant_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to delete this job application.")
        db.delete(job_application)
        db.commit()
        return {"message": "Job application deleted successfully."}
    except Exception :
        error_message = "Failed to delete job application."
        raise HTTPException(status_code=500, detail=error_message)
    

   





