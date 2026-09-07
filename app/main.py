from fastapi import FastAPI , Response , status , HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, Field
from datetime import datetime

from os import getenv

app = FastAPI()
try :
    conn = psycopg2.connect(host=getenv('hostname') , database=getenv('db_name') , user=getenv('username') , password=getenv('password') , cursor_factory=RealDictCursor)
    cur = conn.cursor()
    print("DB connection successfull!")
except Exception as error:
    print("DB connection failed!")
    print(f"Error:{error}")


class Incident(BaseModel):
    id : int
    type : str
    description : str
    severity : str
    reported_at : datetime = Field(default_factory=datetime.now)
    published : bool
    
class Incident_post(BaseModel):
    type : str
    description : str
    severity : str
    published : bool

@app.get("/")
def home():
    return {"msg":"Welcome!"}

@app.get("/incidents")
def read_incidents():
    cur.execute('''SELECT * FROM incidents''')
    incidents = cur.fetchall()
    return incidents

@app.get("/incidents/{incident_id}")
def read_incident(incident_id : int):
    cur.execute("""SELECT * FROM incidents WHERE incident_id = %s""" , (incident_id ,))
    matching_incident = cur.fetchone()

    if not matching_incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No incident found with id : {incident_id}")
    
    return matching_incident


@app.post("/incident", status_code=status.HTTP_201_CREATED)
def post_incident(incident: Incident_post):
    incident_dict = incident.model_dump()

    cur.execute(
        """
        INSERT INTO incidents (type, description, severity,published)
        VALUES (%s, %s, %s , %s)
        """,
        (
            incident_dict["type"],
            incident_dict["description"],
            incident_dict["severity"],
            incident_dict["published"],
        ),
    )
    conn.commit()

    return incident_dict


@app.put("/incidents/{incident_id}")
def update_incident(incident_id: int, updated_incident: Incident_post):
    incident_dict = updated_incident.model_dump()

    cur.execute(
        """
        UPDATE incidents
        SET type = %s, description = %s, severity = %s, published = %s
        WHERE incident_id = %s
        RETURNING incident_id, type, description, severity, published
        """,
        (
            incident_dict["type"],
            incident_dict["description"],
            incident_dict["severity"],
            incident_dict["published"],
            incident_id,
        )
    )
    updated = cur.fetchone()
    conn.commit()

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No incident found with id: {incident_id}",
        )

    return updated

@app.delete("/incidents/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: int):
    cur.execute(
        "DELETE FROM incidents WHERE incident_id = %s RETURNING incident_id",
        (incident_id,),
    )
    deleted = cur.fetchone()
    conn.commit()

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No incident found with id: {incident_id}",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)