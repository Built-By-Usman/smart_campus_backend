from app.models.user import UserModel
from app.models.course import CourseModel
from app.models.complaint import ComplaintModel
from app.schemas.user import UserCreate,ApproveRejectUserSchema
from sqlalchemy.orm import Session
from fastapi import status,HTTPException
from sqlalchemy.exc import SQLAlchemyError


def all(db:Session):
    users=db.query(UserModel).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no user available in database")
    return users;  


def all_students(db:Session):
    students= db.query(UserModel).filter(UserModel.role=="student").all()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No student available in database")
    return students
def all_teachers(db:Session):
    teachers= db.query(UserModel).filter(UserModel.role=="teacher").all()
    if not teachers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No teacher available in database")
    return teachers


def unauthenticated_teachers(db:Session):
    unauthenticated_teachers = db.query(UserModel).filter(UserModel.is_authenticated==False,UserModel.role=="teacher",UserModel.is_active==True).all()
    if not unauthenticated_teachers:
        raise HTTPException(status_code=status.HTTP_200_OK,detail="No unauthenticated teacher available")
    return unauthenticated_teachers

def unauthenticated_students(db:Session):
    unauthenticated_students = db.query(UserModel).filter(UserModel.is_authenticated==False,UserModel.role=="student",UserModel.is_active==True).all()
    if not unauthenticated_students:
        raise HTTPException(status_code=status.HTTP_200_OK,detail="No unauthenticated student available")
    return unauthenticated_students


def approve_user(data:ApproveRejectUserSchema,db:Session):
    for user_id in data.id:
        user = db.query(UserModel).filter(UserModel.id==user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid user")
        user.is_authenticated=True

    
    db.commit()
    return {'detail':'Approved successfully'}


def decline_user(data:ApproveRejectUserSchema,db:Session):
    for user_id in data.id:
        user=db.query(UserModel).filter(UserModel.id==user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid user")
        user.is_active=False
    
    db.commit()
    return {'detail':'Declined Successfully'}


    



    
def update(id:int,request:UserCreate,db:Session):
     existing_email=db.query(UserModel).filter(UserModel.email==request.email).first()
     if existing_email:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="This email is already registered")
     user=db.query(UserModel).filter(UserModel.id==id)

     if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} is not available")
     
     try:
        user.update(request.dict(),synchronize_session=False)
        db.commit()
        return {"detail":"The book details are updated successfully"}
     except SQLAlchemyError as e:
         db.rollback()
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")



def delete(id:int,db:Session):
    user=db.query(UserModel).filter(UserModel.id==id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} is not available")


    try:
        user.update({UserModel.is_active:False},synchronize_session=False)
        db.commit()
        return {"detail":"User deactivated successfully"}
    except SQLAlchemyError as e:
         db.rollback()
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")
    


def load_dashboard(db:Session):
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





