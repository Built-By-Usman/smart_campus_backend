from sqlalchemy import Column,String,Integer,ForeignKey,Float
from app.db.database import base

class SubmissionModel(base):
    __tablename__="submissions"

    id=Column(Integer,primary_key=True,index=True)

    assignment_id=Column(Integer,ForeignKey("assignments.id"))
    student_id=Column(Integer,ForeignKey("users.id"))

    file_url=Column(String,nullable=False)
    grade=Column(Float,nullable=False)