from http.client import HTTPException
from typing import Optional, List, Union, Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlmodel import select, Session

from app.api.deps import (
    CurrentUser,
    SessionDep, get_current_user,
)
from app.core.db import get_session
from app.models import (
    College,
    Major,
    CollegeDetail,
    CollegeListResponse,
    MajorListResponse, CollegeResponse, CollegeResponseModel, CollegeDetailResponseModel
)

router = APIRouter()

# API to list all majors
# @router.get("/list-college", response_model=MajorListResponse)
# def list_college_majors(session: SessionDep, current_user: CurrentUser, search_query: Optional[str] = None) -> MajorListResponse:
#     """
#     List all college majors.
#     """
#     query = select(Major)
#     if search_query:
#         query = query.where(
#             or_(
#                 Major.major_name.ilike(f"%{search_query}%"),
#                 Major.major_definition.ilike(f"%{search_query}%")
#             )
#         )
#     majors = session.exec(query).all()
#     return MajorListResponse(data=majors, message="Majors retrieved successfully")
#
# @router.get("/list-colleges/{college_id}", response_model=CollegeListResponse)
# def list_colleges_by_major(major_id: int, session: SessionDep, current_user: CurrentUser) -> CollegeListResponse:
#
#     colleges = session.exec(
#         select(College)
#         .join(CollegeDetail, College.id == CollegeDetail.college_id)
#         .where(CollegeDetail.major_id == major_id)
#     ).all()
#
#     response = CollegeListResponse(data=colleges, message="Colleges retrieved successfully")
#     return response

@router.get("/colleges", response_model=Dict[str, Any])
def get_colleges(session: Session = Depends(get_session)):
    # Fetch all colleges
    colleges = session.exec(select(College)).all()

    # Return the response with message and data dictionary
    return {
        "message": "succes",
        "data": colleges
    }

@router.get("/colleges/{id}", response_model=CollegeResponseModel)
def get_major_by_id(college_id: int, session: Session = Depends(get_session)):
    college = session.get(College, college_id)
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    return CollegeResponseModel(message="success", data=college)

@router.get("/colleges-detail", response_model=Dict[str, Any])
def get_college_detail(session: Session = Depends(get_session)):
    # Fetch all colleges
    colleges_detail = session.exec(select(CollegeDetail)).all()

    # Return the response with message and data dictionary
    return {
        "message": "succes",
        "data": colleges_detail
    }

@router.get("/colleges-detail/{id}", response_model=CollegeDetailResponseModel)
def get_college_detail_by_id(
        *,
        session: Session = Depends(get_session),
        id: int, # Ensure the user is authenticated
) -> CollegeDetailResponseModel:
    # Check if the user is authenticated


    # Retrieve the college detail by ID
    college_detail = session.get(CollegeDetail, id)
    if not college_detail:
        raise HTTPException(status_code=404, detail="College detail not found")

    return CollegeDetailResponseModel(
        message="success",
        data=college_detail
    )



