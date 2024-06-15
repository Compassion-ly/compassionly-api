from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from app.core.db import get_session
from app.models import Major,MajorListResponseModel, MajorResponseModel, MajorDetailResponseModel, Course, MajorCourse, FutureProspect, MajorDetail, MajorProspect

router = APIRouter()

# Endpoint to get all majors
@router.get("/majors", response_model=MajorListResponseModel)
def get_majors(session: Session = Depends(get_session)):
    statement = select(Major)
    results = session.exec(statement).all()
    return MajorListResponseModel(message="success", data=results)

# Endpoint to get a major by ID
@router.get("/majors/{major_id}", response_model=MajorDetailResponseModel)
def get_major_by_id(major_id: int, session: Session = Depends(get_session)):

    # class MajorDetail(BaseModel):
    # major: Major | None = None
    # courses: List[Course] | None = None
    # prospects: List[FutureProspect] | None = None
    major = session.get(Major, major_id)
    # courses = session.exec(select(Course).where(Course.major_id == major_id)).all()
    courses = session.exec(select(Course).join(MajorCourse).join(Major).where(Major.id == major_id)).all()
    prospects = session.exec(select(FutureProspect).join(MajorProspect).where(MajorProspect.major_id == major_id)).all()
    major_detail = MajorDetail(major=major, courses=courses, prospects=prospects)

    if not major:
        raise HTTPException(status_code=404, detail="Major not found")
    return MajorDetailResponseModel(message="success", data=major_detail)
