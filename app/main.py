from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

from app.db.database import engine
from app.db.base import base
from app.routers import auth, user, course, assignment,submissions
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()


# alembic revision --autogenerate -m "create users table"
# alembic upgrade head

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(course.router)
app.include_router(assignment.router)
app.include_router(submissions.router)