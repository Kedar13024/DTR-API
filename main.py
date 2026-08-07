from fastapi import FastAPI , Response , status , HTTPException
from h11 import Event
from pydantic import BaseModel, Field
from datetime import datetime


app = FastAPI()


class Incident(BaseModel):
    id : int
    type : str
    description : str
    severity : str
    reported_at : datetime = Field(default_factory=datetime.now)
    

incidents : list[dict] =[
    {
        "id": 1,
        "type": "Fire",
        "description": "Fire reported at an industrial warehouse.",
        "severity": "urgent",
        "reported_at": "2026-08-05",
    },
    {
        "id": 2,
        "type": "Flood",
        "description": "Rising water has blocked the main road near Riverside.",
        "severity": "high",
        "reported_at": "2026-08-06",
    },
    {
        "id": 3,
        "type": "Medical emergency",
        "description": "A rescue team requested medical supplies at the evacuation center.",
        "severity": "medium",
        "reported_at": "2026-08-06",
    },
]


@app.get("/")
def home():
    return {"msg":"Welcome!"}

@app.get("/incidents")
def read_incident():
    return incidents

@app.get("/incidents/{incident_id}")
def read_incident(incident_id : int):
    matching_incident = [ incident for incident in incidents if incident["id"] == incident_id ]

    if not matching_incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No incident found with id : {incident_id}")
    
    return matching_incident


@app.post("/incidents")
def post_incident(incident : Incident):
    incident_dict = incident.model_dump()
    incidents.append(incident_dict)
    return incident_dict


@app.put("/incidents/{incident_id}")
def update_incident(incident_id : int , updated_incident : Incident):

    matching_incident = [ incident for incident in incidents if incident["id"] == incident_id ]

    if not matching_incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No incident found with id : {incident_id}")

    new_incident = updated_incident.model_dump()
    new_incident['id'] = incident_id
    incidents.append(new_incident)
    
    return new_incident