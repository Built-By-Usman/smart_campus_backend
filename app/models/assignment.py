from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from app.db.database import base

class AssignmentModel(base):
    __tablename__="assignments"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    description = Column(String,nullable=False)
    due_date = Column(DateTime,nullable=False)

    course_id=Column(Integer,ForeignKey("courses.id"))
    teacher_id=Column(Integer,ForeignKey("users.id"))
