from sqlalchemy import Column,String,Integer,ForeignKey,Date
from app.db.database import base
class AttendanceModel(base):
    __tablename__ = "attendence"

    id=Column(Integer,primary_key=True,index=True)

    course_id=Column(Integer,ForeignKey("courses.id"))
    student_id=Column(Integer,ForeignKey("users.id"))


    date=Column(Date,nullable=False)

    status=Column(String,nullable=False)
