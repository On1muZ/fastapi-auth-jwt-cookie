from pydantic import BaseModel
from uuid import UUID


class UserCreate(BaseModel):
    username: str
    password: str


class UserPassword(BaseModel):
    password: str


class UserPasswordChange(BaseModel):
    password: str
    new_password: str


class BaseUser(BaseModel):
    user_id: UUID
    username: str


class Token(BaseModel):
    token: str