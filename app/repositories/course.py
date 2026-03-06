from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.schemas.course import CourseCreate
from app.schemas.enrollment import EnrollmentCreate
from app.models.enrollment import EnrollmentModel
from app.models.user import UserModel
from app.models.course import CourseModel
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import UserModel


def all(db:Session):
    courses=db.query(CourseModel).all()
    if not courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No course found in database")
    return courses

def create(request:CourseCreate,db:Session):
    existing_course=db.query(CourseModel).filter(CourseModel.course_code==request.course_code).first()
    if existing_course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Course with {request.course_code} is already exist")
    
    
    teacher=db.query(UserModel).filter(UserModel.id==request.teacher_id).first()
    
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No teacher exist with this id")
    if not teacher.role=="teacher":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"The selected user is not a teacher")

        


    teacher_name=teacher.name
    
    new_course=CourseModel(name=request.name,teacher_id=request.teacher_id,course_code=request.course_code,teacher_name=teacher_name)

    try:
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")

def enrollment(request:EnrollmentCreate,db:Session):
    student=db.query(UserModel).filter(UserModel.id==request.student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Student with {id} is not found in database")
    is_student=True if student.role=="student" else False
    if not is_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Selected person is not a student in database")

    course = db.query(CourseModel).filter(CourseModel.id==request.course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No course found with this course id")
    existing_student=db.query(EnrollmentModel).filter(EnrollmentModel.student_id==request.student_id,EnrollmentModel.course_id==request.course_id).first()

    if existing_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="This student is already enrolled in this course")
    

    try:
        enrollment=EnrollmentModel(student_id=request.student_id,course_id=request.course_id)
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return {"detail":"Student enrolled in this course successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")

def teacher_courses(teacher_id:int,db:Session):
    courses=db.query(CourseModel).filter(CourseModel.teacher_id==teacher_id).all()
    if not courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No course assigned to this teacher")
    return courses

def student_courses(student_id:int,db:Session):
    courses=db.query(EnrollmentModel).filter(EnrollmentModel.student_id==student_id).all()
    if not courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This student have no enrollment in any course")
    return courses
