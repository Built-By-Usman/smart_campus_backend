from sqlalchemy import Column,Integer,ForeignKey
from app.db.database import base
from sqlalchemy.orm import relationship

class EnrollmentModel(base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    student = relationship("UserModel")
    course = relationship("CourseModel")
