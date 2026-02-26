from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from app.db.database import base
class AdminModel(base):
    __tablename__="admins"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True)
    password=Column(String)