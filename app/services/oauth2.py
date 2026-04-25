from fastapi import HTTPException, status, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from app.services.JWTtoken import verify_token
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.models.admin import AdminModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # This returns the string (username/email) from the token
    email = verify_token(credentials_exception, token)

    # FETCH THE ACTUAL USER OBJECT
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if user is None:
        user = db.query(AdminModel).filter(AdminModel.email == email).first()
    if user is None:
        raise credentials_exception
    return user
