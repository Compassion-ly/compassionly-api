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
    Message,
    UpdatePassword,
    User,
    UserRegister,
    UserUpdateMe,
    School,
    UserDetailResponse,
    UserSchoolDetail,
    UserSchoolDetailResponse,
    SchoolMajor,
)
from app.utils import generate_new_account_email, send_email

router = APIRouter()

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

    school = session.exec(select(School).where(School.id == school_id)).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    school_major = session.exec(select(SchoolMajor).where(SchoolMajor.id == current_user.school_major_id)).first()

    # user_school_detail = UserSchoolDetail(school=school, school_major=school_major, user=current_user)

    # use from_db method to convert db model to pydantic model
    user_school_detail = UserSchoolDetail(school=School.from_db(school), school_major=SchoolMajor.from_db(school_major), user=User.from_db(current_user))

    response = UserSchoolDetailResponse(data=user_school_detail, message="User school info retrieved successfully")

    return response


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

