from sqlalchemy.exc import IntegrityError
from typing import List
from fastapi import status , HTTPException , Depends , APIRouter
from backend.app.api.db.database import Session, get_db
from backend.app.api.models import models
from backend.app.api.schemas import schemas
from backend.app.api.services import security

router = APIRouter(
    prefix="/user" , tags=["User"]
)

@router.post("", response_model=schemas.User_response, status_code=status.HTTP_201_CREATED)
def create_user(user : schemas.User , db : Session = Depends(get_db)):
    """Create a user account after checking whether the email already exists."""


    existing_user = db.query(models.User).filter(models.User.user_email == user.user_email).first()

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    new_user = models.User(
        user_email=user.user_email,
        user_password=security.hashed_pass(user.user_password),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        ) from exc

    return new_user

@router.get("", response_model=List[schemas.User_response])
def get_users(db : Session = Depends(get_db)):
    """Return all registered users without exposing password hashes."""

    users = db.query(models.User).all()
    return users


@router.get("/{user_id}" , response_model=schemas.User_response)
def get_user(user_id : int , db : Session = Depends(get_db) ):
    """Return one user by ID or raise a 404 error when it does not exist."""


    matching_user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if not matching_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No user found with id : {user_id}")
    
    return matching_user
