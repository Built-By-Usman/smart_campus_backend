from fastapi import FastAPI

from app.db.database import engine
from app.db.base import base

from app.routers import auth,user

app = FastAPI()

base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)