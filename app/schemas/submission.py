from pydantic import BaseModel,FileUrl
from typing import Optional


class SubmissionCreate(BaseModel):
    assignment_id:int
    file_url:FileUrl

class SubmissionResponse(BaseModel):
    id:int
    assignment_id:int
    student_id:int
    file_url:FileUrl
    grade:Optional[float]

    class Config:
        from_attributes=True