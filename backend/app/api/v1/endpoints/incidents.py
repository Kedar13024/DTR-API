"""Endpoints for creating, reading, updating, and deleting incidents."""

from typing import List
from fastapi import Response , status , HTTPException , Depends , APIRouter
from sqlalchemy import func
from backend.app.api.db.database import Session, get_db
from backend.app.api.models import models
from backend.app.api.schemas.incident_schema import (
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
)
from backend.app.api.schemas.vote_schema import VoteType
from backend.app.api.v1.endpoints.oauth2 import get_current_user

router = APIRouter(
    prefix="/incidents" , tags=["Incident"]
)

def incident_response(db, incident, current_user_id):
    """Build an incident response with vote totals and the user's vote."""

    upvotes = db.query(func.count(models.Vote.vote_id)).filter(
        models.Vote.incident_id == incident.incident_id,
        models.Vote.vote_value == 1,
    ).scalar() or 0

    downvotes = db.query(func.count(models.Vote.vote_id)).filter(
        models.Vote.incident_id == incident.incident_id,
        models.Vote.vote_value == -1,
    ).scalar() or 0

    current_vote = db.query(models.Vote.vote_value).filter(
        models.Vote.incident_id == incident.incident_id,
        models.Vote.user_id == current_user_id,
    ).scalar()

    return {
        "incident_id": incident.incident_id,
        "incident_type": incident.incident_type,
        "description": incident.description,
        "severity": incident.severity,
        "published": incident.published,
        "reported_at": incident.reported_at,
        "reported_by": incident.reported_by,
        "reporter": incident.reporter,
        "upvote_count": upvotes,
        "downvote_count": downvotes,
        "user_current_vote_type": (
            current_vote
            if current_vote is not None
            else VoteType.NONE
        ),
    }

@router.get("", response_model=List[IncidentResponse])
def read_incidents(db : Session = Depends(get_db) , limit : int = 10 , skip : int = 0 , search : str | None = "" , current_user = Depends(get_current_user)):
    """Return paginated incidents, optionally filtered by severity.

    Args:
        db: Database session supplied by FastAPI.
        Limit: Maximum number of incidents to return.
        skip: Number of incidents to skip.
        search: Severity text used to filter incidents.

    Returns:
        list[models.Incident]: Matching incidents.
    """

    incidents = db.query(models.Incident).filter(models.Incident.severity.contains(search or ""), models.Incident.published.is_(True)).limit(limit).offset(skip).all()
    return [
        incident_response(db, incident, current_user.user_id)
        for incident in incidents
    ]

@router.get("/{incident_id}", response_model=IncidentResponse)
def read_incident(incident_id : int , db : Session = Depends(get_db), current_user : int = Depends(get_current_user)):
    """Return one incident for an authenticated user.

    Args:
        incident_id: ID of the requested incident.
        db: Database session supplied by FastAPI.
        current_user: Authenticated user supplied by the security dependency.

    Returns:
        models.Incident: The matching incident.

    Raises:
        HTTPException: If no incident has the requested ID.
    """


    matching_incident = (
        db.query(models.Incident)
        .filter(
            models.Incident.incident_id == incident_id,
            models.Incident.published.is_(True),
        )
        .first()
    )

    if not matching_incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No incident found with id : {incident_id}")
    
    return incident_response(
        db, matching_incident, current_user.user_id,
    )


@router.post("", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def post_incident(incident: IncidentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Create an incident owned by the authenticated user.

    Args:
        incident: Validated incident creation data.
        db: Database session supplied by FastAPI.
        current_user: Authenticated incident reporter.

    Returns:
        models.Incident: Newly created incident.
    """

    
    new_incident = models.Incident(reported_by=current_user.user_id ,**incident.model_dump())
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    return incident_response(
        db, new_incident, current_user.user_id,
        )


@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(incident_id: int, updated_incident: IncidentUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Replace an incident when it belongs to the authenticated user.

    Args:
        incident_id: ID of the incident to update.
        updated_incident: Validated replacement data.
        db: Database session supplied by FastAPI.
        current_user: Authenticated user attempting the update.

    Returns:
        models.Incident: Updated incident.

    Raises:
        HTTPException: If the incident is missing or belongs to another user.
    """

    incident_dict = updated_incident.model_dump()

    matching_incident_query = db.query(models.Incident).filter(models.Incident.incident_id == incident_id)

    incident = matching_incident_query.first()

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No incident found with id: {incident_id}",
        )

    if incident.reported_by != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="You do not have permission to update this incident.")
    
    matching_incident_query.update(
        incident_dict,  synchronize_session=False
    )
    db.commit()
    db.refresh(incident)
    return incident_response(
        db, incident, current_user.user_id,
        )

@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: int ,  db : Session = Depends(get_db), current_user : int = Depends(get_current_user)):
    """Delete an incident when it belongs to the authenticated user.

    Args:
        incident_id: ID of the incident to delete.
        db: Database session supplied by FastAPI.
        current_user: Authenticated user attempting the deletion.

    Raises:
        HTTPException: If the incident is missing or belongs to another user.
    """

    matching_incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()

    if not matching_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No incident found with id: {incident_id}",
        )

    if matching_incident.reported_by != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="You do not have permission to delete this incident.")
    
    db.delete(matching_incident)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
