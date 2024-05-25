from schema.base import Base
from pydantic import BaseModel, EmailStr, Field


class Auth(Base):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class BaseUser(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1)


class UserCreate(BaseUser):
    password: str = Field(min_length=8, max_length=16)


class User(Base, BaseUser):
    class Config:
        from_attributes = True


class GroupBase(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=20)


class Group(Base, GroupBase):
    owner_id: int
    members: list[User] = []

    class Config:
        from_attributes = True
