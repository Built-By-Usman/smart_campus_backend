from pydantic import BaseModel
from datetime import datetime

class AssignmentBase(BaseModel):
    title:str
    description:str
    due_date:datetime



class AssignmentCreate(AssignmentBase):
    course_id:int
    teacher_id:int

class AssignmentResponse(AssignmentBase):
    id:int
    course_id:int
    teacher_id:int

    class Config:
        from_attributes=True
    


