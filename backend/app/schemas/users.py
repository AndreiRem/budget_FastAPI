from pydantic import BaseModel, Field
from typing import Annotated


class UserBase(BaseModel):
    username: Annotated[str, Field(
        max_length=20,
        description="Username"
    )]


class UserCreate(UserBase):
    password: str


class UserLogin(UserCreate):
    pass


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: str