from pydantic import BaseModel


class CourseBase(BaseModel):
    name:str

class CourseCreate(CourseBase):
    teacher_id:int
    course_code:str

class CourseResponse(CourseBase):
    id:int
    teacher_id:int
    course_code:str
    teacher_name:str
    class Config:
        from_attributes=True