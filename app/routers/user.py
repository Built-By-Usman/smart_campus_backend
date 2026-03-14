from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse,UserCreate,ApproveRejectUserSchema
from app.db.database import get_db
from typing import List
from app.repositories.user import all,update,delete,all_teachers,all_students,unauthenticated_students,unauthenticated_teachers,approve_user,count_students,count_teachers,decline_user
from app.services.oauth2 import get_current_user


router=APIRouter(
    prefix='/user',
    tags=['User']
)

@router.get('/',response_model=List[UserResponse])
def get_all_user(db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return all(db)


@router.get('/count-teachers/')
def count_all_teachers(db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return count_teachers(db=db)


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


@router.put('/approve-unauthenticated-user/')
def approve_unauthenticated_user(data:ApproveRejectUserSchema,db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return approve_user(data=data,db=db)
@router.put('/decline-unauthenticated-user/')
def decline_unauthenticated_user(data:ApproveRejectUserSchema,db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return decline_user(data=data,db=db)




@router.put('/{id}/')
def update_user(request:UserCreate,id:int,db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return update(id,request,db)

@router.delete('/{id}/')
def delete_user(id:int,db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return delete(id,db)
