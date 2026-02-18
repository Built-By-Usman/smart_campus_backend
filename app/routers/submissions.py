from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.submission import SubmissionCreate,SubmissionUpdate,SubmissionResponse,SubmissionCountResponse
from app.services.oauth2 import get_current_user
from app.repositories.assignment_submission import submit_assignment,get_all_submissions,update_submission,delete_submission
from app.models.user import UserModel


router=APIRouter(
    prefix='/submissions',
    tags=['Submissions']
    )

@router.post('/',response_model=SubmissionResponse,status_code=status.HTTP_201_CREATED)
def create_assignment(request:SubmissionCreate,db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    return submit_assignment(request=request,db=db,current_user=current_user) 


@router.get('/assignment{assignment_id}',response_model=List[SubmissionResponse])
def view_all_assignments(assignment_id:int,db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    return get_all_submissions(assignment_id=assignment_id,db=db)

@router.put('/submission_id',response_model=SubmissionResponse)
def assignment_updation(submission_id:int,request:SubmissionUpdate,db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    return update_submission(submission_id=submission_id,request=request,db=db,current_user=current_user)


@router.delete('/submission_id',status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(submission_id:int,db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    return delete_submission(submission_id=submission_id,db=db,current_user=current_user)



