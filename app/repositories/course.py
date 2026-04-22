from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.course import CourseCreate
from app.schemas.enrollment import EnrollmentCreate
from app.models.enrollment import EnrollmentModel
from app.models.user import UserModel
from app.models.course import CourseModel
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import UserModel
from app.models.chat import ChatRoomModel, ChatMemberModel


def all(db: Session):
    courses = db.query(CourseModel).all()
    if not courses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No course found in database"
        )
    return courses


def create(request: CourseCreate, db: Session):
    existing_course = (
        db.query(CourseModel)
        .filter(CourseModel.course_code == request.course_code)
        .first()
    )

    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course with {request.course_code} already exists",
        )

    teacher = db.query(UserModel).filter(UserModel.id == request.teacher_id).first()

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found"
        )

    if teacher.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected user is not a teacher",
        )

    try:
        # -----------------------
        # 1. CREATE COURSE
        # -----------------------
        new_course = CourseModel(
            name=request.name,
            teacher_id=request.teacher_id,
            course_code=request.course_code,
            teacher_name=teacher.name,
        )

        db.add(new_course)
        db.commit()
        db.refresh(new_course)

        # -----------------------
        # 2. CREATE CHAT ROOM
        # -----------------------
        chat_room = ChatRoomModel(
            name=f"{new_course.name} Group Chat",
            course_id=new_course.id,
            created_by=teacher.id,
        )

        db.add(chat_room)
        db.commit()
        db.refresh(chat_room)

        # -----------------------
        # 3. ADD TEACHER AS MEMBER
        # -----------------------
        db.add(ChatMemberModel(chat_room_id=chat_room.id, user_id=teacher.id))

        db.commit()

        return new_course

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


def enrollment(request: EnrollmentCreate, db: Session):

    try:
        enrollment = EnrollmentModel(
            student_id=request.student_id, course_id=request.course_id
        )

        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)

        # -----------------------
        # ADD STUDENT TO CHAT ROOM
        # -----------------------
        chat_room = (
            db.query(ChatRoomModel)
            .filter(ChatRoomModel.course_id == request.course_id)
            .first()
        )

        if chat_room:
            db.add(
                ChatMemberModel(chat_room_id=chat_room.id, user_id=request.student_id)
            )

            db.commit()

        return enrollment

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


def teacher_courses(teacher_id: int, db: Session):
    courses = db.query(CourseModel).filter(CourseModel.teacher_id == teacher_id).all()
    if not courses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No course assigned to this teacher",
        )
    return courses


def student_courses(student_id: int, db: Session):
    courses = (
        db.query(EnrollmentModel).filter(EnrollmentModel.student_id == student_id).all()
    )
    if not courses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This student have no enrollment in any course",
        )
    return courses
