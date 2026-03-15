from pydantic import BaseModel,EmailStr
from typing import List
from datetime import datetime
from app.schemas.complaint import ComplaintResponse



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
    is_authenticated:bool
    is_verified_email:bool
    created_at:datetime

    class Config:
        from_attributes=True


class ApproveRejectUserSchema(BaseModel):
    id:List[int]

class AdminDashboardResponse(BaseModel):
    total_students: int
    total_teachers: int
    active_courses: int
    pending_complaints: int
    recent_users:List[UserResponse]
    recent_complaints:List[ComplaintResponse]



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


class ResendOtp(BaseModel):
    email:EmailStr

class VerifyOtp(BaseModel):
    email:EmailStr
    otp:str