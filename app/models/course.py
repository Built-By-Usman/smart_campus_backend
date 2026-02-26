from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import base

class CourseModel(base):
    __tablename__="courses"
    id=Column(Integer,primary_key=True,index=True)
    course_code=Column(String,nullable=False,unique=True)
    teacher_name = Column(String,nullable=True)
    name=Column(String,nullable=False)
    teacher_id=Column(Integer,ForeignKey("users.id"))
    teacher=relationship("UserModel")