from sqlalchemy import Column, String, Boolean, DateTime, Integer
from app.db.database import base


class OTPModel(base):
    __tablename__="otp_codes"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,nullable=False)
    otp=Column(String,nullable=False)
    expire_at=Column(DateTime,nullable=False)
    is_used=Column(Boolean,nullable=False,default=False)