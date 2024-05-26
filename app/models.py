from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel
from typing import Annotated, Any


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
# class UserBase(SQLModel):
    


# Properties to receive via API on creation
# class UserCreate(UserBase):
#     password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
# class UserUpdate(UserBase):
#     email: str | None = None  # type: ignore
#     password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    user_schools_id: int | None = None


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
    user_schools_id: int | None = None
    # items: list["Item"] = Relationship(back_populates="owner")

class School(SQLModel, table=True):
    __tablename__ = "schools"
    id: int | None = Field(default=None, primary_key=True)
    npsn: str = None
    school_name: str = None
    school_province: str = None
    school_city: str = None

class UserSchool(SQLModel, table=True):
    __tablename__ = "user_schools"
    id: int | None = Field(default=None, primary_key=True)
    school_id: int = None
    school_name: str = None
    school_major: str = None

# Properties to return via API, id is always required
# class UserPublic(UserBase):
#     id: int


# class UsersPublic(SQLModel):
#     data: list[UserPublic]
#     count: int


# # Shared properties
# class ItemBase(SQLModel):
#     title: str
#     description: str | None = None


# # Properties to receive on item creation
# class ItemCreate(ItemBase):
#     title: str


# # Properties to receive on item update
# class ItemUpdate(ItemBase):
#     title: str | None = None  # type: ignore


# # Database model, database table inferred from class name
# class Item(ItemBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     title: str
#     owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
#     owner: User | None = Relationship(back_populates="items")


# # Properties to return via API, id is always required
# class ItemPublic(ItemBase):
#     id: int
#     owner_id: int


# class ItemsPublic(SQLModel):
#     data: list[ItemPublic]
#     count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str

class ResponseToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User

class RequestToken(BaseModel):
    token: str