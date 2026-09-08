from fastapi import FastAPI , Response , status , HTTPException , Depends
from pydantic import BaseModel, Field , ConfigDict
from datetime import datetime
from .database import Base, Session, engine , get_db
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

class Incident(BaseModel):
    incident_id : int
    type : str
    description : str
    severity : str
    reported_at : datetime = Field(default_factory=datetime.now)
    published : bool
    
class Incident_create(BaseModel):
    type : str
    description : str
    severity : str
    published : bool

class IncidentUpdate(Incident_create):
    pass
class IncidentResponse(Incident):
    incident_id: int
    reported_at: datetime

    model_config = ConfigDict(from_attributes=True)


@app.get("/")
def home():
    return {"msg":"Welcome!"}

@app.get("/incidents")
def read_incidents(db : Session = Depends(get_db)):
    incidents = db.query(models.Incident).all()
    return incidents

@app.get("/incidents/{incident_id}")
def read_incident(incident_id : int , db : Session = Depends(get_db) ):

    matching_incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()

    if not matching_incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No incident found with id : {incident_id}")
    
    return matching_incident


@app.post("/incident", status_code=status.HTTP_201_CREATED)
def post_incident(incident: Incident_create ,  db : Session = Depends(get_db)):

    new_incident = models.Incident(**incident.model_dump())
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    return new_incident


@app.put("/incidents/{incident_id}")
def update_incident(incident_id: int, updated_incident: Incident_create ,  db : Session = Depends(get_db)):
    incident_dict = updated_incident.model_dump()

    matching_incident_query = db.query(models.Incident).filter(models.Incident.incident_id == incident_id)

    incident = matching_incident_query.first()

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No incident found with id: {incident_id}",
        )

    matching_incident_query.update(
        incident_dict,  synchronize_session=False
    )
    db.commit()
    db.refresh(incident)
    return matching_incident_query.first()

@app.delete("/incidents/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: int ,  db : Session = Depends(get_db)):
    matching_incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()

    if not matching_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No incident found with id: {incident_id}",
        )
    db.delete(matching_incident)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
