from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime



class UserBase(BaseModel):
    name:str
    email:EmailStr

class UserCreate(UserBase):
    password:str
    role:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    role:str

class AdminResponce(BaseModel):
    email:EmailStr
    id:int

class UserResponse(UserBase):
    id:int
    role:str
    is_active:bool
    is_authenticated=True
    is_authenticated:bool
    created_at:datetime

    class Config:
        from_attributes=True


class Token(BaseModel):
    user:UserResponse

    access_token: str
    token_type: str


class TokenForAdmin(BaseModel):
    admin:AdminResponce
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None