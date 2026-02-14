from fastapi import FastAPI

from app.db.database import engine
from app.db.base import base

from app.routers import auth,user,course,assignment

app = FastAPI()

base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(course.router)
app.include_router(assignment.router)