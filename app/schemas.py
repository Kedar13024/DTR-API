from pydantic import BaseModel
from datetime import datetime

class Incident_base(BaseModel):
    incident_type : str
    description : str
    severity : str
    published : bool = True
    
class Incident_create(Incident_base):
    pass

class IncidentUpdate(Incident_base):
    pass

class IncidentResponse(Incident_base):
    incident_id : int
    reported_at : datetime

    class Config:
        orm_mode = True