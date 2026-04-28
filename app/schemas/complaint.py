from pydantic import BaseModel
from typing import Optional

class ComplaintCreate(BaseModel):
    title: str
    description: str

# --- NEW SCHEMA ---
class ComplaintStatusUpdate(BaseModel):
    status: str
    rejection_reason: Optional[str] = None

class ComplaintResponse(BaseModel):
    id: int
    student_id: int
    title: str
    description: str
    status: str
    rejection_reason: Optional[str] = None 

    class Config:
        from_attributes = True