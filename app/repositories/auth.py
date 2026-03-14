from fastapi import status,HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import Token,UserLogin,TokenForAdmin,UserCreate
from app.models.user import UserModel
from app.models.otp import OTPModel
from app.services.hashing import verify_password,get_hashed_password
from app.services.JWTtoken import create_access_token
from sqlalchemy.exc import SQLAlchemyError
from app.models.admin import AdminModel
from app.services.hashing import get_hashed_password
from app.services.email_sender import send_email_otp
from app.services.otp_generation import generate_otp,otp_expiration
from pydantic import EmailStr
from datetime import datetime



def login_user(request:UserLogin ,db:Session):
    if request.role=="admin":
        admin=db.query(AdminModel).filter(AdminModel.email==request.email).first()
        if not admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="This email is not registered")
        if not request.password==admin.password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Password is incorrect")
        
        access_token = create_access_token(data={"sub": admin.email})
        return TokenForAdmin(
        admin=admin,
        access_token=access_token,
        token_type="bearer"
        )
    else:
        user=db.query(UserModel).filter(UserModel.email==request.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="This email is not registered")
        if not verify_password(request.password,user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Password is incorrect")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not allowed to access the system")
        if not user.is_authenticated:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please ask admin to approve your account")
        if not user.is_verified_email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please verify you email address")
        if user.role!=request.role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"You are not enroll as a {request.role}")

        


        access_token = create_access_token(data={"sub": user.email})
        return Token(
        user=user,
        access_token=access_token,
        token_type="bearer"
        )





def create(request:UserCreate,db:Session):
    existing_user=db.query(UserModel).filter(UserModel.email==request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with this email is already exist")
    
    hashed_password=get_hashed_password(request.password)
    user=UserModel(name=request.name.title(),email=request.email,password=hashed_password,role=request.role.lower())

    otp_code=generate_otp()
    expire_at=otp_expiration()

    otp=OTPModel(
        email=request.email,
        otp=otp_code,
        expire_at=expire_at,
        is_used=False
    )


    send_email_otp(
        to_email=request.email,
        otp=otp_code
    )

    db.add(otp)
    db.commit()
    
    try:

        db.add(user)
        db.commit()
        db.refresh(user)
        return {'detail':'Account created an otp send please verify your email address'}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")
    
def verify(email:EmailStr,otp_code:str,db:Session):
    otp=db.query(OTPModel).filter(
        OTPModel.email==email,
        OTPModel.otp==otp_code,
        OTPModel.expire_at>datetime.utcnow(),
        OTPModel.is_used==False
    ).first()
    if not otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid or expire otp")
    

    otp.is_used=True
    db.commit()

    user=db.query(UserModel).filter(UserModel.email==email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No user found with this email")
    

    user.is_verified_email=True
    db.commit()
    db.refresh(user)

    return user

def resend(email:EmailStr,db:Session):
    otp_code=generate_otp()
    expire_at=otp_expiration()

    otp=OTPModel(
        email=email,
        otp=otp_code,
        expire_at=expire_at,
        is_used=False
    )

    db.add(otp)
    db.commit()

    send_email_otp(
        to_email=email,
        otp=otp_code
    )

    db.add(otp)
    db.commit()

    return {'detail':f'OTP sent to {email}'}

