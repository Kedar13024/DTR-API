"""FastAPI application entry point."""

from fastapi import FastAPI , Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, incidents, users, vote
from app.routers.oauth2 import get_current_user

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home(current_user = Depends(get_current_user)):
    """Return a simple response confirming that the API is running.

    Returns:
        dict[str, str]: A welcome message.
    """

    return {"msg":f"Welcome! {current_user.user_email}"}

app.include_router(incidents.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
