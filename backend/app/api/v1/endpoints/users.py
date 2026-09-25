from sqlalchemy.exc import IntegrityError
from typing import List
from fastapi import status , HTTPException , Depends , APIRouter
from backend.app.api.db.database import Session, get_db
from backend.app.api.models import models
from backend.app.api.schemas import user_schema
from backend.app.api.services import security
from backend.app.api.v1.endpoints.oauth2 import require_admin

router = APIRouter(
    prefix="/user" , tags=["User"]
)



@router.post("", response_model=user_schema.User_response, status_code=status.HTTP_201_CREATED)
def create_user(user : user_schema.User , db : Session = Depends(get_db)):
    """Create a user account after checking whether the email already exists."""


    existing_user = db.query(models.User).filter(models.User.user_email == user.user_email).first()

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    new_user = models.User(
        user_fullname =user.user_fullname,
        user_phoneno=user.user_phoneNo,
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

@router.get("", response_model=List[user_schema.User_response])
def get_users(_admin=Depends(require_admin), db: Session = Depends(get_db)):
    """Return all registered users without exposing password hashes."""
    return db.query(models.User).all()


@router.get("/{user_id}" , response_model=user_schema.User_response)
def get_user(user_id : int , db : Session = Depends(get_db) ):
    """Return one user by ID or raise a 404 error when it does not exist."""


    matching_user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if not matching_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No user found with id : {user_id}")
    
    return matching_user
