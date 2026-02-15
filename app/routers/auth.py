from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from app.models.user import UserModel
from app.services.hashing import verify_password
from app.services.JWTtoken import create_access_token


router=APIRouter(
    prefix='/token',
    tags=['Authentication']
)

@router.post('/',response_model=Token)
def login(request:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user=db.query(UserModel).filter(UserModel.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="This email is not registered")
    if not verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Password is incorrect")
    
    access_token = create_access_token(data={"sub": user.email})
    return Token(
    user=user,
    access_token=access_token,
    token_type="bearer"
)


