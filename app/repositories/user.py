from app.models.user import UserModel
from app.models.course import CourseModel
from app.models.complaint import ComplaintModel
from app.schemas.user import UserUpdate,ApproveRejectUserSchema
from sqlalchemy.orm import Session
from fastapi import status,HTTPException
from sqlalchemy.exc import SQLAlchemyError


def all(db:Session):
    try:
        return db.query(UserModel).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )  


def all_students(db:Session):
    try:
        return db.query(UserModel).filter(UserModel.role=="student").all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )  

def all_teachers(db:Session):
    try:
        return db.query(UserModel).filter(UserModel.role=="teacher").all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )  


def unauthenticated_teachers(db:Session):
    try:
        return db.query(UserModel).filter(UserModel.is_authenticated==False,UserModel.role=="teacher",UserModel.is_active==True,UserModel.is_verified_email==True).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )  


def unauthenticated_students(db:Session):
    try:
        return db.query(UserModel).filter(UserModel.is_authenticated==False,UserModel.role=="student",UserModel.is_active==True,UserModel.is_verified_email==True).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )  


def approve_user(data:ApproveRejectUserSchema,db:Session):
    try:
        for user_id in data.id:
            user = db.query(UserModel).filter(UserModel.id==user_id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid user")
            user.is_authenticated=True

    
        db.commit()
        return {'detail':'Approved successfully'}

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )  

def decline_user(data:ApproveRejectUserSchema,db:Session):
    try:
        for user_id in data.id:
            user=db.query(UserModel).filter(UserModel.id==user_id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid user")
            user.is_active=False
        
        db.commit()
        return {'detail':'Declined Successfully'}

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )  



def update(id: int, request: UserUpdate, db: Session):
    query = db.query(UserModel).filter(UserModel.id == id)
    if not query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} is not available"
        )
    if request.email:
        existing_user = db.query(UserModel).filter(UserModel.email == request.email, UserModel.id != id).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already registered"
            )

    try:
        query.update(request.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        return {"detail": "The user details updated successfully"}

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )
def delete(id:int,db:Session):
    user=db.query(UserModel).filter(UserModel.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} is not available")


    try:
        user.is_active=False
        db.commit()
        return {"detail":"User deactivated successfully"}
    except SQLAlchemyError as e:
         db.rollback()
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")
    


def load_dashboard(db:Session):
    try:
        students=db.query(UserModel).filter(UserModel.role=='student',UserModel.is_authenticated==True).count()
        teachers=db.query(UserModel).filter(UserModel.role=='teacher',UserModel.is_authenticated==True).count()
        courses = db.query(CourseModel).count()
        complaints = db.query(ComplaintModel).filter(ComplaintModel.status=='pending').count()

        recentUsers = db.query(UserModel).order_by(UserModel.created_at.desc()).limit(5).all()
        recentComplaints = db.query(ComplaintModel).order_by(ComplaintModel.id.desc()).limit(5).all()

        return {
            "total_students":students,
            "total_teachers":teachers,
            "active_courses":courses,
            "pending_complaints":complaints,
            "recent_users":recentUsers,
            "recent_complaints":recentComplaints,
        }
    except SQLAlchemyError as e:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")
    




