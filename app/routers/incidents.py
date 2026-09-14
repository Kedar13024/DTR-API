from typing import List
from fastapi import Response , status , HTTPException , Depends , APIRouter
from app.database import Session, get_db
from app import models , schemas
from app.routers.oauth2 import get_current_user

router = APIRouter(
    prefix="/incidents" , tags=["Incident"]
)

@router.get("", response_model=List[schemas.IncidentResponse])
def read_incidents(db : Session = Depends(get_db) , Limit : int = 10 , skip : int = 0 , search : str | None = ""):
    incidents = db.query(models.Incident).filter(models.Incident.severity.contains(search)).limit(Limit).offset(skip).all()
    return incidents

@router.get("/{incident_id}" , response_model=schemas.IncidentResponse)
def read_incident(incident_id : int , db : Session = Depends(get_db), current_user : int = Depends(get_current_user)):

    matching_incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()

    if not matching_incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No incident found with id : {incident_id}")
    
    return matching_incident


@router.post("", status_code=status.HTTP_201_CREATED)
def post_incident(incident: schemas.Incident_create ,  db : Session = Depends(get_db) ,current_user : int = Depends(get_current_user)):
    
    new_incident = models.Incident(reported_by=current_user.user_id ,**incident.model_dump())
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    return new_incident


@router.put("/{incident_id}" ,response_model=schemas.IncidentResponse)
def update_incident(incident_id: int, updated_incident: schemas.IncidentUpdate ,  db : Session = Depends(get_db), current_user : int = Depends(get_current_user)):
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
    return matching_incident_query.first()

@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: int ,  db : Session = Depends(get_db), current_user : int = Depends(get_current_user)):
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