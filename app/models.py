from sqlalchemy import Column, String, Text, Integer, JSON, text, MetaData
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel, Json
from typing import Annotated, Any, Generic, Optional, TypeVar, List, Union, Dict

T = TypeVar('T')
metadata = MetaData()
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
            last_name=db_model.last_name,
            uid=db_model.uid,
            is_active=db_model.is_active,
            phone_number=db_model.phone_number,
            gender=db_model.gender,
            user_topic_weight=db_model.user_topic_weight,
            school_id=db_model.school_id,
            school_major_id=db_model.school_major_id,
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
            school_name=db_model.school_name,
            school_province=db_model.school_province,
            school_city=db_model.school_city
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

class CollegeDetail(SQLModel, table=True):
    __tablename__ = "college_detail"
    id: int | None = Field(default=None, primary_key=True)
    college_id: int = Field(default=None, foreign_key="college.id")
    major_id: int = Field(default=None, foreign_key="major.id")
    capacity: int | None = Field(default=None)
    interest: int | None = Field(default=None)
    portofolio_type: str | None = Field(default=None)

    # Relationship with College
    college: Optional["College"] = Relationship(back_populates="college_detail")
    major: Optional["Major"] = Relationship(back_populates="college_details")

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            college_id=db_model.college_id,
            major_id=db_model.major_id,
            capacity=db_model.capacity,
            interest=db_model.interest,
            portofolio_type=db_model.portofolio_type
        )

class College(SQLModel, table=True):
    __tablename__ = "college"
    id: Optional[int] = Field(default=None, primary_key=True)
    college_name: Optional[str] = Field(default=None)

    # Relationship with CollegeDetail
    college_detail: List["CollegeDetail"] = Relationship(back_populates="college")

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            college_name=db_model.college_name,
        )


class Major(SQLModel, table=True):
    __tablename__ = "major"
    id: Optional[int] = Field(default=None, primary_key=True)
    major_name: Optional[str] = Field(default=None)
    major_definition: Optional[str] = Field(default=None)
    major_image: Optional[str] = Field(default=None)
    major_interest: Optional[int] = Field(default=None)
    major_level: Optional[str] = Field(default=None)
    for_who: Optional[str] = Field(default=None)

    # Relationship with CollegeDetail
    college_details: List["CollegeDetail"] = Relationship(back_populates="major")

    # Relationship with MajorCourse
    major_courses: List["MajorCourse"] = Relationship(back_populates="major")

    # Relationship with MajorProspect
    major_prospects: List["MajorProspect"] = Relationship(back_populates="major")

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            major_name=db_model.major_name,
            major_definition=db_model.major_definition,
            major_image=db_model.major_image,
            major_interest=db_model.major_interest,
            major_level=db_model.major_level,
            for_who=db_model.for_who
        )

class FutureProspect(SQLModel, table=True):
    __tablename__ = "future_prospect"
    id: Optional[int] = Field(default=None, primary_key=True)
    future_prospect_name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    # Ensure the relationship name in back_populates matches the one in MajorProspect
    major_prospects: List["MajorProspect"] = Relationship(back_populates="future_prospect")

# Corrected relationship in MajorProspect
class MajorProspect(SQLModel, table=True):
    __tablename__ = "major_prospect"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    major_id: Optional[int] = Field(default=None, foreign_key="major.id")
    future_prospect_id: Optional[int] = Field(default=None, foreign_key="future_prospect.id")

    major: Optional["Major"] = Relationship(back_populates="major_prospects")
    future_prospect: Optional["FutureProspect"] = Relationship(back_populates="major_prospects")


class Course(SQLModel, table=True):
    __tablename__ = "course"
    id: Optional[int] = Field(default=None, primary_key=True)
    course_name: Optional[str] = Field(default=None)
    course_image: Optional[str] = Field(default=None)
    course_definition: Optional[str] = Field(default=None)
    course_explain: Optional[str] = Field(default=None)

    # Relationship with MajorCourse
    major_courses: List["MajorCourse"] = Relationship(back_populates="course")

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            course_name=db_model.course_name,
            course_image=db_model.course_image,
            course_definition=db_model.course_definition,
            course_explain=db_model.course_explain
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


class MajorCourse(SQLModel, table=True):
    __tablename__ = "major_course"
    id: Optional[int] = Field(default=None, primary_key=True)
    major_id: Optional[int] = Field(default=None, foreign_key="major.id")
    course_id: Optional[int] = Field(default=None, foreign_key="course.id")

    # Relationships
    major: Optional["Major"] = Relationship(back_populates="major_courses")
    course: Optional["Course"] = Relationship(back_populates="major_courses")

    @classmethod
    def from_db(cls, db_model):
        return cls(
            id=db_model.id,
            major_id=db_model.major_id,
            course_id=db_model.course_id
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
    topic_weight: Optional[List[float]]
    #ratings: List["UserTopicRatingRead"] = []

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

class MajorDetail(BaseModel):
    major: Major | None = None
    courses: List[Course] | None = None
    prospects: List[FutureProspect] | None = None


class CourseDetail(BaseModel):
    course: Course | None = None


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

class CollegeResponse(BaseModel):
    message: str
    data: Dict[int, Dict[str, Union[College, List[CollegeDetail]]]]

    class Config:
        from_attributes = True

class MajorListResponseModel(BaseModel):
    message: str
    data: List[Major]

class MajorResponseModel(BaseModel):
    message: str
    data: Major

class CollegeResponseModel(BaseModel):
    message: str
    data: College

class CollegeDetailResponseModel(BaseModel):
    message: str
    data: CollegeDetail

class CourseDetailResponseModel(BaseModel):
    message: str
    data: CourseDetail

class MajorDetailResponseModel(BaseModel):
    message: str
    data: MajorDetail

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