from app.models.user import UserModel
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from fastapi import status,HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.services.hashing import get_hashed_password


def get(db:Session):
    users=db.query(UserModel).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no user available in database")
    return users;  

def create(request:UserCreate,db:Session):
    existing_user=db.query(UserModel).filter(UserModel.email==request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with this email is already exist")
    
    hashed_password=get_hashed_password(request.password)
    user=UserModel(name=request.name,email=request.email,password=hashed_password,role=request.role)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")
    
def update(id:int,request:UserCreate,db:Session):
     user=db.query(UserModel).filter(id==UserModel.id)

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