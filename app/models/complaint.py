from sqlalchemy import Column,String,Integer,ForeignKey
from app.db.database import base

class ComplaintModel(base):
    __tablename__="complaints"

    id=Column(Integer,primary_key=True,index=True)
    student_id=Column(Integer,ForeignKey("users.id"))
    title=Column(String,nullable=False)
    description=Column(String,nullable=False)
    status=Column(String,default="pending")
    