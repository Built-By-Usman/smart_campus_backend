from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse,UserCreate
from app.models.user import UserModel
from app.db.database import get_db
from typing import List
from app.repositories.user import get,create,update,delete
from app.services.oauth2 import get_current_user


router=APIRouter(
    prefix='/user',
    tags=['user']
)

@router.get('/',response_model=List[UserResponse])
def get_all_user(db:Session=Depends(get_db)):
   return get(db)

@router.post('/',response_model=UserResponse)
def create_user(request:UserCreate,db:Session=Depends(get_db)):
   return create(request=request,db=db)

@router.put('/{id}')
def update_user(request:UserCreate,id:int,db:Session=Depends(get_db),current_user:UserResponse=Depends(get_current_user)):
   return update(id,request,db)

@router.delete('/{id}')
def delete_user(id:int,db:Session=Depends(get_db)):
   return delete(id,db)
