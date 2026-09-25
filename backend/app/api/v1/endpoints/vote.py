from fastapi import status , HTTPException , Depends , APIRouter
from backend.app.api.db.database import Session, get_db
from backend.app.api.models import models
from backend.app.api.schemas.vote_schema import VoteInput, VoteType
from backend.app.api.v1.endpoints.oauth2 import get_current_user

router = APIRouter(
    prefix="/incidents/{incident_id}/vote" , tags=["Vote"]
)


@router.post("")
def vote(incident_id: int, vote: VoteInput, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Create, change, or clear the authenticated user's vote on an incident."""


    incident = db.query(models.Incident).filter(models.Incident.incident_id ==incident_id).first()

    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No incident found with id : {incident_id}")
    
    existing_vote = db.query(models.Vote).filter(models.Vote.incident_id == incident_id , models.Vote.user_id == current_user.user_id).first()

    if vote.vote_value == VoteType.NONE:
        if existing_vote:
            db.delete(existing_vote)
            db.commit()
            return {"msg": "Vote cleared."}

        return {"msg": "No vote to clear."}

    if existing_vote:
        if existing_vote.vote_value == vote.vote_value:
            db.delete(existing_vote)
            db.commit()
            return {"msg": "Vote cleared."}

        existing_vote.vote_value = vote.vote_value
        db.commit()
        return {"msg": "Vote changed."}

    new_vote = models.Vote(
        incident_id = incident_id,
        user_id = current_user.user_id,
        vote_value = vote.vote_value
    )

    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)

    return {"msg": "Vote created."}
