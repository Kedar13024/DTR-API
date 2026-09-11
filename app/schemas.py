from pydantic import BaseModel, ConfigDict, EmailStr
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

    model_config=ConfigDict(from_attributes = True)

    incident_id : int
    reported_at : datetime

        
class User(BaseModel):
    user_email : EmailStr
    user_password : str

class User_response(BaseModel):
    
    model_config=ConfigDict(from_attributes = True)

    user_id : int
    created_at : datetime

class User_login(BaseModel):
    email : EmailStr
    password : str