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
    College,
    Major,
    Course,
    Personality,
    FutureProspect,
    MajorPersonality,
    MajorProspect,
    MajorCourse,
    CollegeDetail,
    MajorListResponse
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

# API to list all majors
@router.get("/list-college-majors", response_model=MajorListResponse) 
def list_college_majors(session: SessionDep, current_user: CurrentUser) -> MajorListResponse:
    """
    List all college majors.
    """
    majors = session.exec(select(Major)).all()
    response = MajorListResponse(data=majors, message="Majors retrieved successfully")
    return response

# API to list all colleges that have specific major
@router.get("/list-colleges-by-major/{major_id}", response_model=MajorListResponse)
def list_colleges_by_major(major_id: int, session: SessionDep, current_user: CurrentUser) -> MajorListResponse:
    """
    List all colleges that have specific major.
    """
    # select all from college_detail, join with college, where major_id = major_id
    colleges = session.exec(
        select(College)
        .join(CollegeDetail, College.id == CollegeDetail.college_id)  # Explicit join condition
        .where(CollegeDetail.major_id == major_id)
    ).all()
    
    response = MajorListResponse(data=colleges, message="Colleges retrieved successfully")
    return response

