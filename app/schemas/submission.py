from pydantic import BaseModel
from typing import Optional


class SubmissionCreate(BaseModel):
    assignment_id:int
    file_url:str

class SubmissionResponse(BaseModel):
    id:int
    assignment_id:int
    student_id:int
    file_url:str
    grade:Optional[float]

    class Config:
        from_attributes=True