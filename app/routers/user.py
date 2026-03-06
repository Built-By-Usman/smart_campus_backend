from fastapi import APIRouter,Depends
from app.models.user import UserModel
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse,UserCreate,VerifyOtp,ResendOtp
from app.db.database import get_db
from typing import List
from app.repositories.user import all,create,update,delete,all_teachers,all_students,unauthenticated_students,unauthenticated_teachers,approve_user,count_students,verify,resend
from app.services.oauth2 import get_current_user
from pydantic import EmailStr


router=APIRouter(
    prefix='/user',
    tags=['User']
)

@router.get('/',response_model=List[UserResponse])
def get_all_user(db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return all(db)


@router.get('/count-teachers/')
def count_all_teachers(db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   teachers=db.query(UserModel).filter(UserModel.role=='teacher',UserModel.is_authenticated==True).count()

   return {
      "total_teachers":teachers
   }


@router.get('/count-students/')
def count_all_students(db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return count_students(db=db)


@router.get('/all-students/',response_model=List[UserResponse])
def get_all_students(db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return all_students(db=db)

@router.get('/all-teachers/',response_model=List[UserResponse])
def get_all_teachers(db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return all_teachers(db=db)
   

@router.get('/all-unauthenticated-teachers/',response_model=List[UserResponse])
def all_unauthenticated_teachers(db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return unauthenticated_teachers(db=db)


@router.get('/all-unauthenticated-students/',response_model=List[UserResponse])
def all_unauthenticated_students(db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return unauthenticated_students(db=db)


@router.put('/approve-unauthenticated-user/',response_model=UserResponse)
def approve_unauthenticated_user(id:int,db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return approve_user(id=id,db=db)



@router.post('/')
def create_user(request:UserCreate,db:Session=Depends(get_db)):
   return create(request=request,db=db)

@router.post('/verify-otp/',response_model=UserResponse)
def verify_otp(request:VerifyOtp,db:Session=Depends(get_db)):
   return verify(email=request.email,otp_code=request.otp,db=db)

@router.put('/{id}/')
def update_user(request:UserCreate,id:int,db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return update(id,request,db)

@router.delete('/{id}/')
def delete_user(id:int,db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return delete(id,db)

@router.post('/resend-otp/')
def resend_otp(request:ResendOtp,db:Session=Depends(get_db)):
   return resend(email=request.email,db=db)