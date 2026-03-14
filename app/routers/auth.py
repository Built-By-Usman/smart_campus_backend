from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.schemas.user import Token,UserLogin,TokenForAdmin,UserCreate,UserResponse,VerifyOtp,ResendOtp
from app.db.database import get_db
from app.repositories.auth import login_user,create,resend,verify
from typing import Union



router=APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/login/',response_model=Union[Token, TokenForAdmin])
def login(request:UserLogin,db:Session=Depends(get_db)):
    return login_user(request=request,db=db)


@router.post('/create/')
def create_user(request:UserCreate,db:Session=Depends(get_db)):
   return create(request=request,db=db)

@router.post('/verify-otp/',response_model=UserResponse)
def verify_otp(request:VerifyOtp,db:Session=Depends(get_db)):
   return verify(email=request.email,otp_code=request.otp,db=db)




@router.post('/resend-otp/')
def resend_otp(request:ResendOtp,db:Session=Depends(get_db)):
   return resend(email=request.email,db=db)