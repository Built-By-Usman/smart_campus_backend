from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from app.models.user import UserModel


from app.db.database import get_db
from app.schemas.complaint import ComplaintResponse, ComplaintCreate
from app.models.complaint import ComplaintModel
from app.services.oauth2 import get_current_user

from app.schemas.complaint import ComplaintResponse, ComplaintCreate, ComplaintStatusUpdate
User = UserModel

from app.repositories.complaint import (
    create_complaint,
    get_student_complaints,
    get_all_complaints,
    get_complaint,
    update_complaint_status,
    delete_complaint,
)

router = APIRouter(prefix="/complaint", tags=["Complaints"])


# ----------------------------
# CREATE COMPLAINT (STUDENT)
# ----------------------------
@router.post("/", response_model=ComplaintResponse)
def create(
    request: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: ComplaintModel= Depends(get_current_user),
):
    return create_complaint(request=request, student_id=current_user.id, db=db)


# ----------------------------
# GET MY COMPLAINTS (STUDENT)
# ----------------------------
@router.get("/my", response_model=List[ComplaintResponse])
def my_complaints(
    db: Session = Depends(get_db),
    current_user: ComplaintModel= Depends(get_current_user),
):
    return get_student_complaints(student_id=current_user.id, db=db)


# ----------------------------
# GET ALL COMPLAINTS (ADMIN)
# ----------------------------
@router.get("/", response_model=List[ComplaintResponse])
def all_complaints(
    db: Session = Depends(get_db),
    current_user: ComplaintModel = Depends(get_current_user),
):
    return get_all_complaints(db=db)


# ----------------------------
# GET SINGLE COMPLAINT
# ----------------------------
@router.get("/{complaint_id}", response_model=ComplaintResponse)
def single_complaint(
    complaint_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: ComplaintModel = Depends(get_current_user),
):
    return get_complaint(complaint_id=complaint_id, db=db)


# ----------------------------
# UPDATE STATUS (ADMIN / TEACHER)
# ----------------------------
# ----------------------------
# UPDATE STATUS (ADMIN / TEACHER)
# ----------------------------
@router.patch("/{complaint_id}/status", response_model=ComplaintResponse)
def change_status(
    complaint_id: int,
    request: ComplaintStatusUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user), 
):
    
    user_role = getattr(current_user, 'role', None)

    if not user_role and current_user.__class__.__name__ == "AdminModel":
        user_role = "admin"

    if user_role not in ["teacher", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to change status"
        )
    
    return update_complaint_status(complaint_id=complaint_id, request=request, db=db)


# ----------------------------
# DELETE COMPLAINT (ADMIN)
# ----------------------------
@router.delete("/{complaint_id}")
def remove_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user: ComplaintModel = Depends(get_current_user),
):
    return delete_complaint(complaint_id=complaint_id, db=db)
