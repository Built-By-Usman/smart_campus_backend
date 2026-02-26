from pydantic import BaseModel
from datetime import date


class AttendanceCreate(BaseModel):
    course_id:int
    student_id:int
    date:date
    status:str


class AttendanceResponse(AttendanceCreate):
    id:int

    class Config:
        from_attributes=True

        
