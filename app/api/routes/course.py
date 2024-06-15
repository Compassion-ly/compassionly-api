from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from app.core.db import get_session
from app.models import Major,MajorListResponseModel, MajorResponseModel, MajorCourse, Course, MajorDetail, CourseDetail, CourseDetailResponseModel, MajorResponseModel, MajorListResponseModel

router = APIRouter()

# Endpoint to get a major by ID
@router.get("/{course_id}", response_model=CourseDetailResponseModel)
def get_course_by_id(course_id: int, session: Session = Depends(get_session)):
    # class MajorResponseModel(BaseModel):
    # message: str
    # data: MajorDetail

    # class MajorDetail(BaseModel):
    # major: Major | None = None
    # courses: List[Course] | None = None

    # major - major_course - course
    course = session.exec(select(Course).where(Course.id == course_id)).first()

    course_detail = CourseDetail(course=course)

    if not course:
        raise HTTPException(status_code=404, detail="Major not found")
    return CourseDetailResponseModel(message="success", data=course_detail)
