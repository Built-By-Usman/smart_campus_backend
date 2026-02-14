from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.course import CourseCreate,CourseResponse
from app.schemas.enrollment import EnrollmentCreate,EnrollmentResponse
from typing import List
from app.repositories.course import all,create,teacher_courses,student_courses,enrollment


router = APIRouter(
    prefix='/course',
    tags=['Courses']
)

@router.get('/',response_model=List[CourseResponse])
def get_all_courses(db:Session=Depends(get_db)):
    return all(db=db)


@router.get('/get_student_courses/{student_id}',response_model=List[EnrollmentResponse])
def get_student_courses(student_id:int,db:Session=Depends(get_db)):
    return student_courses(student_id=student_id,db=db)


@router.get('/get_teacher_courses/{teacher_id}',response_model=List[CourseResponse])
def get_teacher_courses(teacher_id:int,db:Session=Depends(get_db)):
    return teacher_courses(teacher_id=teacher_id,db=db)


@router.post('/',response_model=CourseResponse)
def create_course(request:CourseCreate,db:Session=Depends(get_db)):
    return create(request=request,db=db)

@router.post('/enroll')
def enroll_student(request:EnrollmentCreate,db:Session=Depends(get_db)):
    return enrollment(request=request,db=db)