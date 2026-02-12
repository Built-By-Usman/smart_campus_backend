from pydantic import BaseModel

class ComplaintCreate(BaseModel):
    title:str
    description:str


class ComplaintResponse(BaseModel):
    id:int
    student_id:int
    title:str
    description:str
    status:str

    class Config:
        from_attributes=True