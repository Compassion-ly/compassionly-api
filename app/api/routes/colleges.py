from fastapi import HTTPException
from typing import Dict, Any

from fastapi import APIRouter, Depends
from sqlmodel import select, Session

from app.core.db import get_session
from app.models import (
    College,
    Major,
    CollegeDetail,
    CollegeResponseModel, CollegeDetailResponse, CollegeDetailResponseModel
)

router = APIRouter()


@router.get("/colleges", response_model=Dict[str, Any])
def get_colleges(session: Session = Depends(get_session)):
    # Fetch all colleges
    colleges = session.exec(select(College)).all()

    # Return the response with message and data dictionary
    return {
        "message": "succes",
        "data": colleges
    }

@router.get("/colleges/{college_id}", response_model=CollegeResponseModel)
def get_college_by_id(college_id: int, session: Session = Depends(get_session)):
    # Retrieve the college
    college = session.get(College, college_id)
    if not college:
        raise HTTPException(status_code=404, detail="College not found")

    # Retrieve the majors offered by the college
    major_ids = session.exec(select(CollegeDetail.major_id).where(CollegeDetail.college_id == college_id)).all()
    majors = session.exec(select(Major).where(Major.id.in_(major_ids))).all()

    # Create the response data structure
    response_data = {
        "college": college,
        "majors": majors
    }

    return CollegeResponseModel(message="success", data=response_data)


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




