from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.schemas.user import Token,UserLogin,TokenForAdmin
from app.db.database import get_db
from app.repositories.auth import login_user
from typing import Union



router=APIRouter(
    prefix='/login',
    tags=['Authentication']
)

@router.post('/',response_model=Union[Token, TokenForAdmin])
def login(request:UserLogin = Depends(),db:Session=Depends(get_db)):
    return login_user(request=request,db=db)