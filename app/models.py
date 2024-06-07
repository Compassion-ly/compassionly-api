from sqlalchemy import Column, String, Text, Integer, JSON
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel, Json
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
    user_topic_weight: Optional[Json[List[float]]] = Field(default=None, sa_column=Column(JSON))
    school_id: int | None = None
    school_major_id: int | None = None

    # Define the relationship to UserTopicRating
    user_topic_ratings: List["UserTopicRating"] = Relationship(back_populates="user")

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

# start topic_category table
class TopicCategory(SQLModel, table=True):
    __tablename__ = "topic_category"
    id: int = Field(primary_key=True)
    category_name: Optional[str] = Field(nullable=True, max_length=100)

    # Define the relationship to Topic
    topics: List["Topic"] = Relationship(back_populates="category")

class TopicCategoryRead(SQLModel):
    id: int
    category_name: Optional[str]

# end topic_category table

# start topics table
class Topic(SQLModel, table=True):
    __tablename__ = "topics"
    id: int = Field(primary_key=True)
    topic_name: Optional[str] = Field(nullable=True, index=True, max_length=512)
    topic_category_id: Optional[int] = Field(foreign_key="topic_category.id")
    short_introduction: Optional[str] = Field(nullable=True, max_length=1000)
    topic_image: Optional[str] = Field(nullable=True, max_length=512)
    topic_image2: Optional[str] = Field(nullable=True, max_length=512)
    topic_weight: Optional[Json[List[float]]] = Field(default=None, sa_column=Column(JSON))  # Use JSON type for SQLAlchemy and Pydantic's Json type
    topic_explanation: Optional[str] = Field(nullable=True)

    # Define the relationship to TopicCategory
    category: Optional[TopicCategory] = Relationship(back_populates="topics")
    # Define the relationship to UserTopicRating
    ratings: List["UserTopicRating"] = Relationship(back_populates="topic")

class TopicCreate(SQLModel):
    topic_name: Optional[str]
    topic_category_id: Optional[int]
    short_introduction: Optional[str]
    topic_image: Optional[str]
    topic_image2: Optional[str]
    topic_explanation: Optional[str]

class TopicRead(SQLModel):
    id: int
    topic_name: Optional[str]
    topic_category_id: Optional[int]
    short_introduction: Optional[str]
    topic_image: Optional[str]
    topic_image2: Optional[str]
    topic_explanation: Optional[str]
    ratings: List["UserTopicRatingRead"] = []

# end topics table

# start user_topic_rating table
class UserTopicRating(SQLModel, table=True):
    __tablename__ = "user_topic_rating"
    id: int = Field(primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    rating: Optional[int] = Field(default=None)
    topic_id: Optional[int] = Field(foreign_key="topics.id")

    # Define the relationship to the Topic
    topic: Optional[Topic] = Relationship(back_populates="ratings")

    # Define the relationship to the User
    user: Optional["User"] = Relationship(back_populates="user_topic_ratings")

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            user_id=db_model.user_id,
            rating=db_model.rating,
            topic_id=db_model.topic_id
        )

class UserTopicRatingCreate(SQLModel):
    rating: int
    topic_id: int

class UserTopicRatingRead(SQLModel):
    id: int
    user_id: Optional[int]
    rating: Optional[int]
    topic_id: Optional[int]
# end user_topic_rating table

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