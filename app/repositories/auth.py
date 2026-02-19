from fastapi import status,HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import Token,UserLogin,TokenForAdmin
from app.models.user import UserModel
from app.services.hashing import verify_password
from app.services.JWTtoken import create_access_token
from app.models.admin import AdminModel


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
        if not user.is_authenticated:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please ask admin to approve your account")
        if not user.is_verified_email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please verify you email address")
        


        access_token = create_access_token(data={"sub": user.email})
        return Token(
        user=user,
        access_token=access_token,
        token_type="bearer"
        )
