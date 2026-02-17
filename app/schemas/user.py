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

class AdminResponse(BaseModel):
    email:EmailStr
    name:str
    id:int

    class Config:
        from_attributes=True

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
    admin:AdminResponse
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None