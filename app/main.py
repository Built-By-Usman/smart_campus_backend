from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.base import base
from app.routers import auth, user, course, assignment, submissions, complaint, chat
from dotenv import load_dotenv

app = FastAPI(title="Smart Campus API", root_path="/smart-campus")

load_dotenv()


# alembic revision --autogenerate -m "create users table"
# alembic upgrade head
# sudo systemctl restart fastapi

origins = ["*"]


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
app.include_router(complaint.router)
app.include_router(chat.router)
