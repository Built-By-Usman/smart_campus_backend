from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.models.complaint import ComplaintModel
from app.schemas.complaint import ComplaintCreate
from app.schemas.complaint import ComplaintCreate, ComplaintStatusUpdate


# ----------------------------
# CREATE COMPLAINT
# ----------------------------
def create_complaint(request: ComplaintCreate, student_id: int, db: Session):
    try:
        complaint = ComplaintModel(
            student_id=student_id,
            title=request.title,
            description=request.description,
            status="pending",
        )

        db.add(complaint)
        db.commit()
        db.refresh(complaint)

        return complaint

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating complaint",
        )


# ----------------------------
# GET SINGLE COMPLAINT
# ----------------------------
def get_complaint(complaint_id: int, db: Session):
    complaint = (
        db.query(ComplaintModel).filter(ComplaintModel.id == complaint_id).first()
    )

    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found"
        )

    return complaint


# ----------------------------
# GET ALL COMPLAINTS (ADMIN)
# ----------------------------
def get_all_complaints(db: Session):
    return db.query(ComplaintModel).all()


# ----------------------------
# GET STUDENT COMPLAINTS
# ----------------------------
def get_student_complaints(student_id: int, db: Session):
    return (
        db.query(ComplaintModel).filter(ComplaintModel.student_id == student_id).all()
    )


# ----------------------------
# UPDATE COMPLAINT STATUS
# ----------------------------
def update_complaint_status(complaint_id: int, request: ComplaintStatusUpdate, db: Session):
    try:
        complaint = (
            db.query(ComplaintModel).filter(ComplaintModel.id == complaint_id).first()
        )

        if not complaint:
            raise HTTPException(
                status_code=404, detail="Complaint not found"
            )

        # Update status

        complaint.status = request.status
        
        # If status is declined, ensure a reason is provided

        if request.status.lower() == "declined" or request.status.lower() == "rejected":
            if not request.rejection_reason:
                raise HTTPException(status_code=400, detail="A reason is required when declining a complaint.")
            complaint.rejection_reason = request.rejection_reason
        else:
            # Optional: Clear reason if status is changed back to pending/approved
            
            complaint.rejection_reason = None

        db.commit()
        db.refresh(complaint)
        return complaint

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while updating complaint",
        )
# ----------------------------
# DELETE COMPLAINT (ADMIN)
# ----------------------------
def delete_complaint(complaint_id: int, db: Session):
    try:
        complaint = (
            db.query(ComplaintModel).filter(ComplaintModel.id == complaint_id).first()
        )

        if not complaint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found"
            )

        db.delete(complaint)
        db.commit()

        return {"message": "Complaint deleted successfully"}

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while deleting complaint",
        )
