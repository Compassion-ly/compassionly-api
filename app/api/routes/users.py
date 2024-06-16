from typing import List
import pandas as pd

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlmodel import select

from app.api.deps import (
    CurrentUser,
    SessionDep, get_current_user,
)
from app.core.db import get_session
from app.models import (
    User,
    UserUpdateMe,
    School,
    UserDetailResponse,
    UserSchoolDetail,
    UserSchoolDetailResponse,
    SchoolMajor,
)

router = APIRouter()

class TopTopicsData(BaseModel):
    top_topics: List[str]

class UserTopicResponse(BaseModel):
    message: str
    data: TopTopicsData

# Read the Excel file and create a mapping
df = pd.read_excel('assets/data_bidang.xlsx', engine='openpyxl')
bidang_mapping = df.set_index('id')['bidang'].to_dict()

# TODO: Implement initial user setup to edit personal data that is logged in (first name, last name, phone_number, user_schools_id)
@router.post("/save-user", response_model=UserDetailResponse)
def update_user_personal_data(
    *,
    session: SessionDep,
    user_in: UserUpdateMe,
    current_user: CurrentUser
) -> UserDetailResponse:
    """
    Update own user.
    """
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    response = UserDetailResponse(
        data=User.from_db(current_user), 
        message="Personal data updated successfully"
    )

    return response

# TODO: implement me
@router.get("/me", response_model=UserSchoolDetailResponse)
def read_user_me(session: SessionDep, current_user: CurrentUser) -> UserSchoolDetailResponse:
    """
    Profil lengkap user beserta asal sekolah.
    """
    user_id = current_user.id
    school_id = current_user.school_id
    
    current_user = session.exec(select(User).where(User.id == user_id)).first()
    # if have school_id, get school data

    school = session.exec(select(School).where(School.id == school_id)).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    school_major = session.exec(select(SchoolMajor).where(SchoolMajor.id == current_user.school_major_id)).first()

    # user_school_detail = UserSchoolDetail(school=school, school_major=school_major, user=current_user)

    # use from_db method to convert db model to pydantic model
    user_school_detail = UserSchoolDetail(school=School.from_db(school), school_major=SchoolMajor.from_db(school_major), user=User.from_db(current_user))

    response = UserSchoolDetailResponse(data=user_school_detail, message="User school info retrieved successfully")

    return response


@router.get("/field-recommendation", response_model=UserTopicResponse)
def get_user_top_topics(
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    user = current_user
    user_topic_weight = user.user_topic_weight
    if not user_topic_weight or len(user_topic_weight) != 17:
        raise HTTPException(status_code=400, detail="Invalid user_topic_weight data")

    # Find the indices of the top 3 elements
    top_indices = sorted(range(len(user_topic_weight)), key=lambda i: user_topic_weight[i], reverse=True)[:3]

    # Map the indices to the corresponding bidang text
    top_topics = [bidang_mapping.get(idx + 1, "Unknown") for idx in top_indices]  # +1 to match Excel index

    return UserTopicResponse(
        message="success",
        data=TopTopicsData(top_topics=top_topics)
    )

# @router.patch(
#     "/{user_id}",
#     dependencies=[Depends(get_current_active_superuser)],
#     response_model=UserPublic,
# )
# def update_user(
#     *,
#     session: SessionDep,
#     user_id: int,
#     user_in: UserUpdate,
# ) -> Any:
#     """
#     Update a user.
#     """

#     db_user = session.get(User, user_id)
#     if not db_user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this id does not exist in the system",
#         )
#     if user_in.email:
#         existing_user = crud.get_user_by_email(session=session, email=user_in.email)
#         if existing_user and existing_user.id != user_id:
#             raise HTTPException(
#                 status_code=409, detail="User with this email already exists"
#             )

#     db_user = crud.update_user(session=session, db_user=db_user, user_in=user_in)
#     return db_user

