from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from app.core.db import get_session
from app.models import Major,MajorListResponseModel, MajorResponseModel

router = APIRouter()

# Endpoint to get all majors
@router.get("/majors", response_model=MajorListResponseModel)
def get_majors(session: Session = Depends(get_session)):
    statement = select(Major)
    results = session.exec(statement).all()
    return MajorListResponseModel(message="success", data=results)

# Endpoint to get a major by ID
@router.get("/majors/{major_id}", response_model=MajorResponseModel)
def get_major_by_id(major_id: int, session: Session = Depends(get_session)):
    major = session.get(Major, major_id)
    if not major:
        raise HTTPException(status_code=404, detail="Major not found")
    return MajorResponseModel(message="success", data=major)
