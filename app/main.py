from fastapi import FastAPI
from app.routers import incidents, users
from app.database import engine
from app import models 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"msg":"Welcome!"}


app.include_router(incidents.router)
app.include_router(users.router)
