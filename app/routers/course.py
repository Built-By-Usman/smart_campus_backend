from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import UserModel
from app.services.oauth2 import get_current_user
from app.schemas.course import CourseCreate, CourseResponse
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from typing import List
from app.repositories.course import (
    all,
    create,
    teacher_courses,
    student_courses,
    enrollment,
    count_student_courses,
    count_teacher_courses,
)


router = APIRouter(prefix="/course", tags=["Courses"])


@router.get("/", response_model=List[CourseResponse])
def get_all_courses(
    db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)
):
    return all(db=db)


@router.get("/get-student-courses/", response_model=List[EnrollmentResponse])
def get_student_courses(
    db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)
):
    return student_courses(student_id=current_user.id, db=db)


@router.get("/get-teacher-courses/", response_model=List[CourseResponse])
def get_teacher_courses(
    db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)
):
    return teacher_courses(teacher_id=current_user.id, db=db)


@router.get("/count-teacher-courses/")
def get_student_courses(
    db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)
):
    return count_teacher_courses(teacher_id=current_user.id, db=db)


@router.get("/count-student-courses/")
def get_student_courses(
    db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)
):
    return count_student_courses(student_id=current_user.id, db=db)


@router.post("/", response_model=CourseResponse)
def create_course(
    request: CourseCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return create(request=request, db=db)


@router.post("/enroll/", response_model=EnrollmentResponse)
def enroll_student(
    request: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return enrollment(request=request, db=db)
