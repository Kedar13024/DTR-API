from fastapi import FastAPI , Response , status , HTTPException , Depends
from typing import List
from .database import Session, engine , get_db
from . import models , schemas , utils

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"msg":"Welcome!"}

@app.get("/incidents", response_model=List[schemas.IncidentResponse])
def read_incidents(db : Session = Depends(get_db)):
    incidents = db.query(models.Incident).all()
    return incidents

@app.get("/incidents/{incident_id}" , response_model=schemas.IncidentResponse)
def read_incident(incident_id : int , db : Session = Depends(get_db) ):

    matching_incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()

    if not matching_incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No incident found with id : {incident_id}")
    
    return matching_incident


@app.post("/incident", status_code=status.HTTP_201_CREATED)
def post_incident(incident: schemas.Incident_create ,  db : Session = Depends(get_db)):

    new_incident = models.Incident(**incident.model_dump())
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    return new_incident


@app.put("/incidents/{incident_id}" ,response_model=schemas.IncidentResponse)
def update_incident(incident_id: int, updated_incident: schemas.IncidentUpdate ,  db : Session = Depends(get_db)):
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

@app.post("/user", response_model=schemas.User_response, status_code=status.HTTP_201_CREATED)
def create_user(user : schemas.User , db : Session = Depends(get_db)):

    hashed_password = utils.hashed_pass(user.user_password)
    user.user_password = hashed_password
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/user", response_model=List[schemas.User_response])
def get_users(db : Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/user/{user_id}" , response_model=schemas.User_response)
def get_user(user_id : int , db : Session = Depends(get_db) ):

    matching_user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if not matching_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No user found with id : {user_id}")
    
    return matching_user