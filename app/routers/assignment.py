from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.assignment import AssignmentCreate,AssignmentResponse
from typing import List
from app.repositories.assignment import all,create,teacher_assignments,course_assignments


router=APIRouter(
    prefix='/assignments',
    tags=['Assignment']
)

@router.get('/',response_model=List[AssignmentResponse])
def get_all_assignments(db:Session=Depends(get_db)):
    return all(db=db)

@router.get('/teacher_assignments/{teacher_id}',response_model=List[AssignmentResponse])
def get_all_assignments(teacher_id:int,db:Session=Depends(get_db)):
    return teacher_assignments(teacher_id=teacher_id,db=db)


@router.get('/course_assignments/{teacher_id}',response_model=List[AssignmentResponse])
def get_all_assignments(course_id:int,db:Session=Depends(get_db)):
    return course_assignments(course_id=course_id,db=db)

@router.post('/',response_model=AssignmentResponse)
def create_assignment(request:AssignmentCreate,db:Session=Depends(get_db)):
    return create(request=request,db=db)