from sqlalchemy import Column, String, Text, Integer
from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel
from typing import Annotated, Any, Generic, Optional, TypeVar, List

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

### SQL MODEL ###
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

class College(SQLModel, table=True):
    __tablename__ = "college"
    id: int | None = Field(default=None, primary_key=True)
    college_name: str | None = Field(default=None)
    college_province: str | None = Field(default=None)
    college_city: str | None = Field(default=None)
    details: List['CollegeDetail'] = Relationship(back_populates="college")

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            college_name=db_model.college_name,
            college_province=db_model.college_province,
            college_city=db_model.college_city
        )

class CollegeDetail(SQLModel, table=True):
    __tablename__ = "college_detail"
    id: int | None = Field(default=None, primary_key=True)
    college_id: int | None = Field(default=None, foreign_key="college.id")
    major_id: int | None = Field(default=None)
    college: College = Relationship(back_populates="details")

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            college_id=db_model.college_id
        )

class Major(SQLModel, table=True):
    __tablename__ = "major"
    id: int | None = Field(default=None, primary_key=True)
    major_name: str | None = Field(default=None)
    major_definition: str | None = Field(default=None)
    major_image: str | None = Field(default=None)

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            major_name=db_model.major_name
        )

class Course(SQLModel, table=True):
    __tablename__ = "course"
    id: int | None = Field(default=None, primary_key=True)
    course_name: str | None = Field(default=None)
    course_image: str | None = Field(default=None)
    course_definition: str | None = Field(default=None)
    course_explain: str | None = Field(default=None)

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            course_name=db_model.course_name
        )

class Personality(SQLModel, table=True):
    __tablename__ = "personality"
    id: int | None = Field(default=None, primary_key=True)
    personality_name: str | None = Field(default=None)

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            personality_name=db_model.personality_name
        )

class FutureProspect(SQLModel, table=True):
    __tablename__ = "future_prospect"
    id: int | None = Field(default=None, primary_key=True)
    future_prospect_name: str | None = Field(default=None)
    description: str | None = Field(default=None)

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            future_prospect_name=db_model.future_prospect_name
        )

class MajorPersonality(SQLModel, table=True):
    __tablename__ = "major_personality"
    id: int | None = Field(default=None, primary_key=True)
    major_id: int | None = Field(default=None)
    personality_id: int | None = Field(default=None)

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            major_id=db_model.major_id
        )

class MajorProspect(SQLModel, table=True):
    __tablename__ = "major_prospect"
    id: int | None = Field(default=None, primary_key=True)
    major_id: int | None = Field(default=None)
    prospect_id: int | None = Field(default=None)

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            major_id=db_model.major_id
        )

class MajorCourse(SQLModel, table=True):
    __tablename__ = "major_course"
    id: int | None = Field(default=None, primary_key=True)
    major_id: int | None = Field(default=None)
    course_id: int | None = Field(default=None)

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            major_id=db_model.major_id
        )

# start user_topic_rating table
class UserTopicRating(SQLModel, table=True):
    __tablename__ = "user_topic_rating"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None) # = Field(foreign_key="users.id")
    rating: str | None = Field(default=None)
    topic_id: int | None = Field(default=None) # = Field(foreign_key="topics.id")

    # user: User = Relationship(back_populates="ratings")
    # topic: Topic = Relationship(back_populates="ratings")
    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            user_id=db_model.user_id,
            rating=db_model.rating,
            topic_id=db_model.topic_id
        )

class UserTopicRatingCreate(UserTopicRating):
    pass
class UserTopicRatingRead(UserTopicRating):
    id: int

# end user_topic_rating table

# start topics table
class Topic(SQLModel, table=True):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    topic_name = Column(String, nullable=True)  # Example: Limit to 512 characters
    topic_category_id = Column(Integer, nullable=True)
    short_introduction = Column(String(1000), nullable=True)  # Example: Limit to 1000 characters
    topic_image = Column(String(512), nullable=True)  # Example: Limit to 512 characters
    topic_image2 = Column(String, nullable=True)  # Example: Limit to 512 characters
    topic_explanation = Column(Text, nullable=True)

class TopicCreate(Topic):
    pass
class TopicRead(Topic):
    id: int
# end topics table

### DETAIL MODEL ###
class UserSchoolDetail(BaseModel):
    school: School | None = None
    school_major: SchoolMajor | None = None
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

class MajorListResponse(ResponseModel):
    data: list[Major] | None = None

class CollegeListResponse(ResponseModel):
    data: list[College] | None = None

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