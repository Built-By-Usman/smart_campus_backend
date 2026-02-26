from pydantic import BaseModel
from app.schemas.user import UserResponse
from app.schemas.course import CourseResponse



class EnrollmentCreate(BaseModel):
    course_id:int
    student_id:int

class EnrollmentResponse(BaseModel):
    id: int
    student: UserResponse
    course: CourseResponse

    class Config:
        from_attributes=True
