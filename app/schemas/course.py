from pydantic import BaseModel


class CourseBase(BaseModel):
    name:str

class CourseCreate(CourseBase):
    teacher_id:int

class CourseResponse(CourseBase):
    id:int
    teacher_id:int
    class Config:
        from_attributes=True