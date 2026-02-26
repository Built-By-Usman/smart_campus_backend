from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.submission import SubmissionModel
from app.schemas.submission import SubmissionCreate, SubmissionUpdate
from app.models.user import UserModel

def submit_assignment(request: SubmissionCreate, db: Session, current_user: UserModel):
    new_submission = SubmissionModel(
        assignment_id=request.assignment_id,
        file_url=str(request.file_url),  
        student_id=current_user.id       
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission

def get_all_submissions(assignment_id: int, db: Session):
    
    all_assignements=db.query(SubmissionModel).filter(SubmissionModel.assignment_id == assignment_id).all()
    return all_assignements

def update_submission(submission_id: int, request: SubmissionUpdate, db: Session, current_user: UserModel):
    submission = db.query(SubmissionModel).filter(SubmissionModel.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    
    if submission.student_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this submission")
    
    submission.file_url = str(request.file_url)
    db.commit()
    db.refresh(submission)
    return submission

def delete_submission(submission_id: int, db: Session, current_user: UserModel):
    submission = db.query(SubmissionModel).filter(SubmissionModel.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    
    if submission.student_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this submission")
    
    db.delete(submission)
    db.commit()
    return {
        "detail": "Assignment Deleted Successfully"
        }