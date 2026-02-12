from sqlalchemy import Column,String,Integer,ForeignKey
from app.db.database import base

class EnrollmentModel(base):
    __tablename__="enrollments"
    id=Column(Integer,primary_key=True,index=True)
    student_id=Column(Integer,ForeignKey("users.id"))
    course_id=Column(Integer,ForeignKey("courses.id"))
