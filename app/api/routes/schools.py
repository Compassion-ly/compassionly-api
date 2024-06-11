from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import (
    User,
    School,
    SchoolMajor,
    UserSchoolDetailResponse,
    UserSchoolDetail,
    SchoolListResponse,
    SchoolMajorListResponse
)
from app.utils import generate_new_account_email, send_email

router = APIRouter()


# @router.get(
#     "/",
#     dependencies=[Depends(get_current_active_superuser)],
#     response_model=UsersPublic,
# )
# def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
#     """
#     Retrieve users.
#     """

#     count_statement = select(func.count()).select_from(User)
#     count = session.exec(count_statement).one()

#     statement = select(User).offset(skip).limit(limit)
#     users = session.exec(statement).all()

#     return UsersPublic(data=users, count=count)

# get current logged in user school info
@router.get("/user-school-detail", response_model=UserSchoolDetailResponse)
def read_user_school_info(session: SessionDep, current_user: CurrentUser) -> UserSchoolDetailResponse:
    """
    Get current user school info.
    """
    user_id = current_user.id
    school_id = current_user.school_id
    
    current_user = session.exec(select(User).where(User.id == user_id)).first()

    school = session.exec(select(School).where(School.id == school_id)).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    school_major = session.exec(select(SchoolMajor).where(SchoolMajor.id == current_user.school_major_id)).first()

    # user_school_detail = UserSchoolDetail(school=school, school_major=school_major, user=current_user)

    # use from_db method to convert db model to pydantic model
    user_school_detail = UserSchoolDetail(school=School.from_db(school), school_major=SchoolMajor.from_db(school_major), user=User.from_db(current_user))

    response = UserSchoolDetailResponse(data=user_school_detail, message="User school info retrieved successfully")

    return response

# API to list all schools
@router.get("/list-schools", response_model=SchoolListResponse)
def list_schools(session: SessionDep) -> SchoolListResponse:
    """
    List all schools.
    """
    schools = session.exec(select(School)).all()
    response = SchoolListResponse(data=schools, message="Schools retrieved successfully")
    return response

# API to list school majors
@router.get("/list-school-majors", response_model=SchoolMajorListResponse)
def list_school_majors(session: SessionDep) -> SchoolMajorListResponse:
    """
    List all school majors.
    """
    school_majors = session.exec(select(SchoolMajor)).all()
    response = SchoolMajorListResponse(data=school_majors, message="School majors retrieved successfully")
    return response