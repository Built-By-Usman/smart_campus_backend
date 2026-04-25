from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.assignment import AssignmentCreate
from app.models.assignment import AssignmentModel
from app.models.course import CourseModel
from app.models.user import UserModel
from sqlalchemy.exc import SQLAlchemyError


def all(db: Session):
    try:
        assignments = db.query(AssignmentModel).all()
        if not assignments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No assignment found in database",
            )
        return assignments
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


def create(request: AssignmentCreate, teacher_id: int, db: Session):
    # FIX: Use teacher_id (from argument) instead of request.teacher_id
    teacher = db.query(UserModel).filter(UserModel.id == teacher_id).first()

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher with id:{teacher_id} not found",
        )

    # Check if user is actually a teacher
    if teacher.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The selected user is not a teacher in our records",
        )

    course = db.query(CourseModel).filter(CourseModel.id == request.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id:{request.course_id} is not found",
        )

    # FIX: Verify if the logged-in teacher owns this course
    if course.teacher_id != teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # Better status code for auth issues
            detail="You are not the teacher of this course",
        )

    try:
        assignment = AssignmentModel(
            title=request.title,
            description=request.description,
            due_date=request.due_date,
            course_id=request.course_id,
            teacher_id=teacher_id,  # Use the ID from the token here
        )
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


def teacher_assignments(teacher_id: int, db: Session):
    teacher = db.query(UserModel).filter(UserModel.id == teacher_id).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher with id:{teacher_id} not found",
        )
    is_teacher = True if teacher.role == "teacher" else False
    if not is_teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The selected user is not a techer in our records",
        )

    try:
        assignments = (
            db.query(AssignmentModel)
            .filter(AssignmentModel.teacher_id == teacher_id)
            .all()
        )
        return assignments
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


def course_assignments(course_id: int, db: Session):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id:{course_id} is not found",
        )

    try:
        assignments = (
            db.query(AssignmentModel)
            .filter(AssignmentModel.teacher_id == course_id)
            .all()
        )
        if not assignments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This course have no assignment",
            )
        return assignments
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )
