from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel
from typing import Annotated, Any, Generic, Optional, TypeVar
T = TypeVar('T')

# generic class for response
class ResponseModel(BaseModel, Generic[T]):
    message: str | None = "Success"
    data: Optional[T] = None

    @classmethod
    def success(cls, data: T, message: str = "Request successful") -> "ResponseModel[T]":
        return cls(message=message, data=data)

    @classmethod
    def error(cls, message: str = "An error occurred") -> "ResponseModel[None]":
        return cls(message=message, data=None)



# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    gender: str | None = None
    school_id: int | None = None
    school_major_id: int | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(SQLModel, table=True):
    # custom table name
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    # hashed_password: str | None = None
    uid: str | None = None
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    gender: str | None = None
    school_id: int | None = None
    school_major_id: int | None = None

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            email=db_model.email,
            first_name=db_model.first_name,
            last_name=db_model.last_name
        )

class Token(BaseModel):
    access_token: str | None = None
    token_type: str = "bearer"
    user: User | None = None

class School(SQLModel, table=True):
    __tablename__ = "schools"
    id: int | None = Field(default=None, primary_key=True)
    npsn: str | None = Field(default=None)  # Ensure defaults are appropriate
    school_name: str | None = Field(default=None)
    school_province: str | None = Field(default=None)
    school_city: str | None = Field(default=None)

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            npsn=db_model.npsn,
            school_name=db_model.school_name
        )

class SchoolMajor(SQLModel, table=True):
    __tablename__ = "school_major"
    id: int | None = Field(default=None, primary_key=True)
    school_major_name: str | None = Field(default=None)

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            school_major_name=db_model.school_major_name
        )

class UserSchoolDetail(BaseModel):
    school: School
    school_major: SchoolMajor
    user: User


### RESPONSE MODELS ###
class UserSchoolDetailResponse(ResponseModel):
    data: UserSchoolDetail | None = None

class UserDetailResponse(ResponseModel):
    data: User | None = None

class TokenResponse(ResponseModel):
    data: Token | None = None

class SchoolListResponse(ResponseModel):
    data: list[School] | None = None

class SchoolMajorListResponse(ResponseModel):
    data: list[SchoolMajor] | None = None

# Generic message
class Message(SQLModel):
    message: str





# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str



class RequestToken(BaseModel):
    token: str