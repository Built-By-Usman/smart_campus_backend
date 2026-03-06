from app.models.user import UserModel
from app.models.otp import OTPModel
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from fastapi import status,HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.services.hashing import get_hashed_password
from app.services.email_sender import send_email_otp
from app.services.otp_generation import generate_otp,otp_expiration
from pydantic import EmailStr
from datetime import datetime


def all(db:Session):
    users=db.query(UserModel).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no user available in database")
    return users;  


def all_students(db:Session):
    students= db.query(UserModel).filter(UserModel.role=="student").all()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No student available in database")
    return students
def all_teachers(db:Session):
    teachers= db.query(UserModel).filter(UserModel.role=="teacher").all()
    if not teachers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No teacher available in database")
    return teachers


def unauthenticated_teachers(db:Session):
    unauthenticated_teachers = db.query(UserModel).filter(UserModel.is_authenticated==False,UserModel.role=="teacher").all()
    if not unauthenticated_teachers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No unauthenticated teacher available")
    return unauthenticated_teachers

def unauthenticated_students(db:Session):
    unauthenticated_students = db.query(UserModel).filter(UserModel.is_authenticated==False,UserModel.role=="student").all()
    if not unauthenticated_students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No unauthenticated student available")
    return unauthenticated_students


def approve_user(id:int,db:Session):
    user = db.query(UserModel).filter(UserModel.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid user")
    user.is_authenticated=True
    db.commit()
    db.refresh(user)
    return user
    

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

    db.add(otp)
    db.commit()

    send_email_otp(
        to_email=request.email,
        otp=otp_code
    )

    db.add(otp)
    db.commit()
    send_email_otp(
        to_email=request.email,
        otp=otp_code
    )
    try:

        db.add(user)
        db.commit()
        db.refresh(user)
        return {'detail':'Account created An otp send please verify your email address'}
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
        email=otp_code,
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
    send_email_otp(
        to_email=email,
        otp=otp_code
    )

    return {'detail':f'OTP sent to {email}'}




    
def update(id:int,request:UserCreate,db:Session):
     existing_email=db.query(UserModel).filter(UserModel.email==request.email).first()
     if existing_email:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="This email is already registered")
     user=db.query(UserModel).filter(UserModel.id==id)

     if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} is not available")
     
     try:
        user.update(request.dict(),synchronize_session=False)
        db.commit()
        return {"detail":"The book details are updated successfully"}
     except SQLAlchemyError as e:
         db.rollback()
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")



def delete(id:int,db:Session):
    user=db.query(UserModel).filter(UserModel.id==id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} is not available")


    try:
        user.update({UserModel.is_active:False},synchronize_session=False)
        db.commit()
        return {"detail":"User deactivated successfully"}
    except SQLAlchemyError as e:
         db.rollback()
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")
    


def count_students(db:Session):
    students=db.query(UserModel).filter(UserModel.role=='student',UserModel.is_authenticated==True).count()

    return {
        "total_students":students
    }



